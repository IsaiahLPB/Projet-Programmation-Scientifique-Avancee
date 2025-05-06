#include <armadillo>
#include <complex>
#include <string>

#include "../include/json.hpp"
#include "../include/solver.h"
#include "../include/TimeStepInfo.h"

using namespace arma;
using namespace std;

using json = nlohmann::json;

/**
 * @brief Construct a new Solver:: Solver object
 * @details Initializes some variable to not compute them again later
 * 
 * @param V Matrix of the field potential
 * @param path A string representing the path to the JSON file
 */
Solver::Solver(mat V, const char *path)
{
    ifstream fichier(path);
    if (!fichier.is_open()) {
        std::cerr << "Error while opening the JSON file" << std::endl;
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

    method = data["user parameters"]["method"];
    auto dt_json = data["user parameters"]["dt"];

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
                std::cout << "dt valor readed in the JSON: \"" << dt_str << "\"" << std::endl;
                dt = std::stod(dt_str);
            } catch (const std::exception& e) {
                std::cerr << "Error while converting dt: " << e.what() << std::endl;
                throw;
            }
        }
    } else if (dt_json.is_number()) {
        dt = dt_json;
    } else {
        std::cerr << "'dt' field invalid or missing" << std::endl;
        throw std::runtime_error("'dt' field invalid");
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

/**
 * @brief This function uses an Explicit method (FTCS) to compute some iterations of psi(t+dt)
 * 
 * @param psi_real Real part of the matrix
 * @param psi_imag Imaginary part of the matrix
 * @param info Informations about the current time and the number of iteration since the last matrix was given to the python bloc
 */
void Solver::FTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    for (int i = 0; i < 1000; ++i)
    {
        // Update using FTCS
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

        // Swap pointers instead of copying matrixes
        std::swap(psi_real, psi_real_next);
        std::swap(psi_imag, psi_imag_next);

        // Update temporal informations
        info.stepcounter++;
        info.t += dt;
    }
}

/**
 * @brief This function uses an Implicit method (BTCS) to compute some iterations of psi(t+dt)
 * 
 * @param psi_real Real part of the matrix
 * @param psi_imag Imaginary part of the matrix
 * @param info Informations about the current time and the number of iteration since the last matrix was given to the python bloc
 */
void Solver::BTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    for (int i = 0; i < 50; ++i)
    {
        // Initialize values for the iteration
        psi_real_next = psi_real; 
        psi_imag_next = psi_imag;
        
        double max_diff = 1.0;  // Initial value greater than epsilon
        int iter_count = 0;
        
        while (max_diff > epsilon && iter_count < max_iter)
        {
            // Save previous solutions to compute the difference
            psi_real_prev = psi_real_next;
            psi_imag_prev = psi_imag_next;
            
            // BTCS method: use values at t+dt for the Laplacian
            psi_real_next.submat(1, 1, nx_2, ny_2) = 
                psi_real.submat(1, 1, nx_2, ny_2)
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
                
            psi_imag_next.submat(1, 1, nx_2, ny_2) = 
                psi_imag.submat(1, 1, nx_2, ny_2)
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
            
            // Compute the maximum difference to check for convergence
            diff_real = abs(psi_real_next - psi_real_prev);
            diff_imag = abs(psi_imag_next - psi_imag_prev);
            max_diff = std::max(diff_real.max(), diff_imag.max());
            
            iter_count++;
        }
        
        // Once convergence is reached, update the main matrices
        psi_real = psi_real_next;
        psi_imag = psi_imag_next;
        
        // Update time information
        info.stepcounter++;
        info.t += dt;
    }
}

/**
 * @brief This function uses the Crank-Nicolson method (CTCS) to compute some iterations of psi(t+dt)
 * 
 * @param psi_real Real part of the matrix
 * @param psi_imag Imaginary part of the matrix
 * @param info Informations about the current time and the number of iteration since the last matrix was given to the python bloc
 */
void Solver::CTCS_derivation(mat &psi_real, mat &psi_imag, TimeStepInfo &info)
{
    // Temporary matrixes for iterations
    mat psi_real_new = psi_real;
    mat psi_imag_new = psi_imag;
    mat psi_real_next, psi_imag_next;
    
    for (int i = 0; i < 5; ++i)
    {
        psi_real_next = psi_real;
        psi_imag_next = psi_imag;
        
        double max_diff = 1.0;  // Initial value above epsilon
        int iter_count = 0;
        const int max_iter = 100;  // Maximum number of iteration (to prevent infite loop)
        
        while (max_diff > epsilon && iter_count < max_iter)
        {
            // Save previous solutions to compute the difference
            mat psi_real_prev = psi_real_next;
            mat psi_imag_prev = psi_imag_next;
            
            // Using BTCS method to compute values at t+dt
            psi_real_next.submat(1, 1, nx_2, ny_2) = 
                psi_real.submat(1, 1, nx_2, ny_2)
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
                
            psi_imag_next.submat(1, 1, nx_2, ny_2) = 
                psi_imag.submat(1, 1, nx_2, ny_2)
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
            
            // Compute the maximal difference to check convergence
            mat diff_real = abs(psi_real_next - psi_real_prev);
            mat diff_imag = abs(psi_imag_next - psi_imag_prev);
            max_diff = std::max(diff_real.max(), diff_imag.max());
            
            iter_count++;
        }
        
        // Swap pointers instead of copying matrixes
        std::swap(psi_real, psi_real_next);
        std::swap(psi_imag, psi_imag_next);
        
        // Update temporal informations
        info.stepcounter++;
        info.t += dt;
    }
}