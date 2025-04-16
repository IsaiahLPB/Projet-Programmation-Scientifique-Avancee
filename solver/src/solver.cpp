#include <armadillo>
#include <complex>
#include <string>

#include "../include/json.hpp"
#include "../include/solver.h"
#include "../include/TimeStepInfo.h"

using namespace arma;
using namespace std;

using json = nlohmann::json;

Solver::Solver(mat V)
{
    ifstream fichier("../consts.JSON");
    if (!fichier.is_open()) {
        std::cerr << "Erreur d'ouverture du fichier JSON." << std::endl;
        exit(1);
    }

    json data;
    fichier >> data;

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
}

void Solver::FTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    int i = 0;
    mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;
    while(i < 10000)
    {
        // Mise à jour de la fonction d'onde pour les points intérieurs
        psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) - dt * (A % psi_imag.submat(1, 1, nx-2, ny-2) + coef_x * (psi_imag.submat(2, 1, nx-1, ny-2)+psi_imag.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_imag.submat(1, 2, nx-2, ny-1)+psi_imag.submat(1, 0, nx-2, ny-3))) ;
        psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) + dt * (A % psi_real.submat(1, 1, nx-2, ny-2) + coef_x * (psi_real.submat(2, 1, nx-1, ny-2)+psi_real.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_real.submat(1, 2, nx-2, ny-1)+psi_real.submat(1, 0, nx-2, ny-3))) ;
        
        // Mettre à jour les matrices d'origine
        psi_real = psi_real_next;
        psi_imag = psi_imag_next;

        info.stepcounter++;
        info.t += dt;
        i++;
    }
}

void Solver::BTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag)
{
    // Éviter les copies complètes si possible
	mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;

    // Mise à jour de la fonction d'onde pour les points intérieurs
    psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) - dt * (A % psi_imag.submat(1, 1, nx-2, ny-2) + coef_x * (psi_imag.submat(2, 1, nx-1, ny-2)+psi_imag.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_imag.submat(1, 2, nx-2, ny-1)+psi_imag.submat(1, 0, nx-2, ny-3))) ;
    psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) + dt * (A % psi_real.submat(1, 1, nx-2, ny-2) + coef_x * (psi_real.submat(2, 1, nx-1, ny-2)+psi_real.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_real.submat(1, 2, nx-2, ny-1)+psi_real.submat(1, 0, nx-2, ny-3))) ;
    
    // Mettre à jour les matrices d'origine
    psi_real = psi_real_next;
    psi_imag = psi_imag_next;
}

void Solver::CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag)
{
    // Créer des copies temporaires pour stocker les valeurs à t+dt
    mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;
    
    // Mise à jour de la fonction d'onde pour les points intérieurs
    psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) - dt * (A % psi_imag.submat(1, 1, nx-2, ny-2) + coef_x * (psi_imag.submat(2, 1, nx-1, ny-2)+psi_imag.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_imag.submat(1, 2, nx-2, ny-1)+psi_imag.submat(1, 0, nx-2, ny-3))) ;
    psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real.submat(1, 1, nx-2, ny-2) + dt * (A % psi_real.submat(1, 1, nx-2, ny-2) + coef_x * (psi_real.submat(2, 1, nx-1, ny-2)+psi_real.submat(0, 1, nx-3, ny-2)) + coef_y * (psi_real.submat(1, 2, nx-2, ny-1)+psi_real.submat(1, 0, nx-2, ny-3))) ;
    
    // Mettre à jour les matrices d'origine
    psi_real = psi_real_next;
    psi_imag = psi_imag_next;
}
