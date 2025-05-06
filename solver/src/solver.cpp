#include <armadillo>
#include <complex>
#include <string>

#include "../include/json.hpp"
#include "../include/solver.h"
#include "../include/TimeStepInfo.h"

using namespace arma;
using namespace std;

using json = nlohmann::json;

Solver::Solver(mat V, const char *path)
{
    ifstream fichier(path);
    if (!fichier.is_open()) {
        std::cerr << "Erreur d'ouverture du fichier JSON." << std::endl;
        exit(1);
    }

    json data;
    fichier >> data;

    error = 1.0;
    h_bar = data["constantes"]["h"];
    m     = data["constantes"]["m"];
    nx    = data["constantes"]["n_x"];
    ny    = data["constantes"]["n_y"];
    x_min = data["constantes"]["x_min"];
    x_max = data["constantes"]["x_max"];
    y_min = data["constantes"]["y_min"];
    y_max = data["constantes"]["y_max"];

    method = data["paramètres utilisateurs"]["method"];
    auto dt_json = data["paramètres utilisateurs"]["dt"];

    if (dt_json.is_string()) {
        std::string dt_str = dt_json;
        if (dt_str == "default") {
            if (method == "FTCS") {
                dt = 0.02 / 800;
            } else if (method == "BTCS") {
                dt = 0.02 / 40;
            } else if (method == "CTCS") {
                dt = 0.02 / 4;
            } else {
                std::cerr << "Unknown method: " << method << std::endl;
            }
        } else {
            try {
                std::cout << "Valeur de dt dans le JSON: \"" << dt_str << "\"" << std::endl;
                dt = std::stod(dt_str);
            } catch (const std::exception& e) {
                std::cerr << "Erreur de conversion de dt: " << e.what() << std::endl;
                throw;
            }
        }
    } else if (dt_json.is_number()) {
        dt = dt_json;
    } else {
        std::cerr << "Champ 'dt' invalide ou manquant" << std::endl;
        throw std::runtime_error("Champ 'dt' invalide");
    }

	dx = (x_max - x_min) / (nx - 1);
	dy = (y_max - y_min) / (ny - 1);

	//std::cout << "V size: " << V.n_rows << " x " << V.n_cols << std::endl;
	V_inner = V.submat(1, 1, nx-2, ny-2);
	//std::cout << "Accessing submat(" << 1 << ", " << 1 << ", " << nx-2 << ", " << ny-2 << ")" << std::endl;

	A = ((-1/h_bar) * V_inner - ((h_bar/m) * (1/dx*dx + 1/dy*dy)));
	coef_x = h_bar / (2 * m * dx * dx);
   	coef_y = h_bar / (2 * m * dy * dy);

    nx_1 = nx-1;
    ny_1 = ny-1;
    nx_2 = nx-2;
    ny_2 = ny-2;
    nx_3 = nx-3;
    ny_3 = ny-3;

    psi_real_next.zeros(nx, ny);
    psi_imag_next.zeros(nx, ny);
}

void Solver::FTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    for (int i = 0; i < 1000; ++i)
    {
        // Mise à jour intérieure selon FTCS
        psi_real_next.submat(1, 1, nx_2, ny_2) =
            psi_real.submat(1, 1, nx_2, ny_2)
            - dt * (
                A % psi_imag.submat(1, 1, nx_2, ny_2)
                + coef_x * (
                    psi_imag.submat(2, 1, nx_1, ny_2) +
                    psi_imag.submat(0, 1, nx_3, ny_2)
                )
                + coef_y * (
                    psi_imag.submat(1, 2, nx_2, ny_1) +
                    psi_imag.submat(1, 0, nx_2, ny_3)
                )
            );

        psi_imag_next.submat(1, 1, nx_2, ny_2) =
            psi_imag.submat(1, 1, nx_2, ny_2)
            + dt * (
                A % psi_real.submat(1, 1, nx_2, ny_2)
                + coef_x * (
                    psi_real.submat(2, 1, nx_1, ny_2) +
                    psi_real.submat(0, 1, nx_3, ny_2)
                )
                + coef_y * (
                    psi_real.submat(1, 2, nx_2, ny_1) +
                    psi_real.submat(1, 0, nx_2, ny_3)
                )
            );

        // Échange les pointeurs au lieu de copier les matrices
        std::swap(psi_real, psi_real_next);
        std::swap(psi_imag, psi_imag_next);

        info.stepcounter++;
        info.t += dt;
    }
}


void Solver::BTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    for (int i = 0; i < 50; ++i)
    {
        // Variables temporaires pour stocker les anciennes valeurs au début du pas de temps
        mat psi_real_old = psi_real;
        mat psi_imag_old = psi_imag;
        
        // Initialisation des matrices "next" avec les valeurs actuelles
        psi_real_next = psi_real;
        psi_imag_next = psi_imag;
        
        // Méthode itérative d'Euler pour approximer la solution implicite
        iter = 0;
        
        // Boucle de convergence
        while (error > epsilon && iter < max_iter)
        {
            // Sauvegarde des valeurs avant la mise à jour pour calculer l'erreur
            mat psi_real_prev = psi_real_next;
            mat psi_imag_prev = psi_imag_next;
            
            // Mise à jour implicite (BTCS) pour la partie réelle
            psi_real_next.submat(1, 1, nx_2, ny_2) =
                psi_real_old.submat(1, 1, nx_2, ny_2)
                - dt * (
                    A % psi_imag_next.submat(1, 1, nx_2, ny_2)
                    + coef_x * (
                        psi_imag_next.submat(2, 1, nx_1, ny_2) +
                        psi_imag_next.submat(0, 1, nx_3, ny_2)
                    )
                    + coef_y * (
                        psi_imag_next.submat(1, 2, nx_2, ny_1) +
                        psi_imag_next.submat(1, 0, nx_2, ny_3)
                    )
                );
            
            // Mise à jour implicite (BTCS) pour la partie imaginaire
            psi_imag_next.submat(1, 1, nx_2, ny_2) =
                psi_imag_old.submat(1, 1, nx_2, ny_2)
                + dt * (
                    A % psi_real_next.submat(1, 1, nx_2, ny_2)
                    + coef_x * (
                        psi_real_next.submat(2, 1, nx_1, ny_2) +
                        psi_real_next.submat(0, 1, nx_3, ny_2)
                    )
                    + coef_y * (
                        psi_real_next.submat(1, 2, nx_2, ny_1) +
                        psi_real_next.submat(1, 0, nx_2, ny_3)
                    )
                );
            
            // Calcul de l'erreur entre deux itérations successives
            error = norm(psi_real_next - psi_real_prev, "fro") + 
                    norm(psi_imag_next - psi_imag_prev, "fro");
            
            iter++;
        }
        
        // Une fois la convergence atteinte, on met à jour psi_real et psi_imag pour le prochain pas de temps
        std::swap(psi_real, psi_real_next);
        std::swap(psi_imag, psi_imag_next);
        
        info.stepcounter++;
        info.t += dt;
    }
}

void Solver::CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag, TimeStepInfo &info)
{
    for (int i = 0; i < 5; ++i)
    {
        // Mise à jour intérieure selon CTCS
        psi_real_next.submat(1, 1, nx_2, ny_2) =
            psi_real.submat(1, 1, nx_2, ny_2)
            - dt * (
                A % psi_imag.submat(1, 1, nx_2, ny_2)
                + coef_x * (
                    psi_imag.submat(2, 1, nx_1, ny_2) +
                    psi_imag.submat(0, 1, nx_3, ny_2)
                )
                + coef_y * (
                    psi_imag.submat(1, 2, nx_2, ny_1) +
                    psi_imag.submat(1, 0, nx_2, ny_3)
                )
            );

        psi_imag_next.submat(1, 1, nx_2, ny_2) =
            psi_imag.submat(1, 1, nx_2, ny_2)
            + dt * (
                A % psi_real.submat(1, 1, nx_2, ny_2)
                + coef_x * (
                    psi_real.submat(2, 1, nx_1, ny_2) +
                    psi_real.submat(0, 1, nx_3, ny_2)
                )
                + coef_y * (
                    psi_real.submat(1, 2, nx_2, ny_1) +
                    psi_real.submat(1, 0, nx_2, ny_3)
                )
            );

        // Échange les pointeurs au lieu de copier les matrices
        std::swap(psi_real, psi_real_next);
        std::swap(psi_imag, psi_imag_next);

        info.stepcounter++;
        info.t += dt;
    }
}
