#include <armadillo>
#include <complex>

#include "../include/solver.h"

using namespace arma;
using namespace std;

Solver::Solver(int alg_id, mat V)
{
	dt = dt_vals[alg_id];
	dx = (x_max - x_min) / (nx - 1);
	dy = (y_max - y_min) / (ny - 1);

	std::cout << "V size: " << V.n_rows << " x " << V.n_cols << std::endl;
	V_inner = V.submat(1, 1, nx-2, ny-2);
	std::cout << "Accessing submat(" << 1 << ", " << 1 << ", " << nx-2 << ", " << ny-2 << ")" << std::endl;

	A = ((-1/h_bar) * V_inner - ((h_bar/m) * (1/dx*dx + 1/dy*dy)));
	coef_x = h_bar / (2 * m * dx * dx);
   	coef_y = h_bar / (2 * m * dy * dy);
}

void Solver::FTCS_derivation(mat &psi_real, mat &psi_imag)
{
    // Créer des copies temporaires pour stocker les valeurs à t+dt
    mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;
    
    // Sous-matrices pour éviter les effets de bord
    // (nous excluons les bords où les différences finies ne sont pas définies)
    mat psi_real_inner = psi_real.submat(1, 1, nx-2, ny-2);
    mat psi_imag_inner = psi_imag.submat(1, 1, nx-2, ny-2);
    
    mat psi_real_x_plus = psi_real.submat(2, 1, nx-1, ny-2);  // psi(x+1, y)
    mat psi_real_x_minus = psi_real.submat(0, 1, nx-3, ny-2); // psi(x-1, y)
    mat psi_imag_x_plus = psi_imag.submat(2, 1, nx-1, ny-2);
    mat psi_imag_x_minus = psi_imag.submat(0, 1, nx-3, ny-2);
    
    mat psi_real_y_plus = psi_real.submat(1, 2, nx-2, ny-1);  // psi(x, y+1)
    mat psi_real_y_minus = psi_real.submat(1, 0, nx-2, ny-3); // psi(x, y-1)
    mat psi_imag_y_plus = psi_imag.submat(1, 2, nx-2, ny-1);
    mat psi_imag_y_minus = psi_imag.submat(1, 0, nx-2, ny-3);
    
    // Mise à jour de la fonction d'onde pour les points intérieurs
    psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real_inner - dt * (A % psi_imag_inner + coef_x * (psi_imag_x_plus+psi_imag_x_minus) + coef_y * (psi_imag_y_plus+psi_imag_y_minus)) ;
    psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real_inner + dt * (A % psi_real_inner + coef_x * (psi_real_x_plus+psi_real_x_minus) + coef_y * (psi_real_y_plus+psi_real_y_minus)) ;
    
    // Mettre à jour les matrices d'origine
    psi_real = psi_real_next;
    psi_imag = psi_imag_next;
}

void Solver::BTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag)
{
	    // Créer des copies temporaires pour stocker les valeurs à t+dt
    mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;
    
    // Sous-matrices pour éviter les effets de bord
    // (nous excluons les bords où les différences finies ne sont pas définies)
    mat psi_real_inner = psi_real.submat(1, 1, nx-2, ny-2);
    mat psi_imag_inner = psi_imag.submat(1, 1, nx-2, ny-2);
    
    mat psi_real_x_plus = psi_real.submat(2, 1, nx-1, ny-2);  // psi(x+1, y)
    mat psi_real_x_minus = psi_real.submat(0, 1, nx-3, ny-2); // psi(x-1, y)
    mat psi_imag_x_plus = psi_imag.submat(2, 1, nx-1, ny-2);
    mat psi_imag_x_minus = psi_imag.submat(0, 1, nx-3, ny-2);
    
    mat psi_real_y_plus = psi_real.submat(1, 2, nx-2, ny-1);  // psi(x, y+1)
    mat psi_real_y_minus = psi_real.submat(1, 0, nx-2, ny-3); // psi(x, y-1)
    mat psi_imag_y_plus = psi_imag.submat(1, 2, nx-2, ny-1);
    mat psi_imag_y_minus = psi_imag.submat(1, 0, nx-2, ny-3);
    
    // Mise à jour de la fonction d'onde pour les points intérieurs
    psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real_inner - dt * (A % psi_imag_inner + coef_x * (psi_imag_x_plus+psi_imag_x_minus) + coef_y * (psi_imag_y_plus+psi_imag_y_minus)) ;
    psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real_inner + dt * (A % psi_real_inner + coef_x * (psi_real_x_plus+psi_real_x_minus) + coef_y * (psi_real_y_plus+psi_real_y_minus)) ;
    
    // Mettre à jour les matrices d'origine
    psi_real = psi_real_next;
    psi_imag = psi_imag_next;
}

void Solver::CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag)
{
    // Créer des copies temporaires pour stocker les valeurs à t+dt
    mat psi_real_next = psi_real;
    mat psi_imag_next = psi_imag;
    
    // Sous-matrices pour éviter les effets de bord
    // (nous excluons les bords où les différences finies ne sont pas définies)
    mat psi_real_inner = psi_real.submat(1, 1, nx-2, ny-2);
    mat psi_imag_inner = psi_imag.submat(1, 1, nx-2, ny-2);
    
    mat psi_real_x_plus = psi_real.submat(2, 1, nx-1, ny-2);  // psi(x+1, y)
    mat psi_real_x_minus = psi_real.submat(0, 1, nx-3, ny-2); // psi(x-1, y)
    mat psi_imag_x_plus = psi_imag.submat(2, 1, nx-1, ny-2);
    mat psi_imag_x_minus = psi_imag.submat(0, 1, nx-3, ny-2);
    
    mat psi_real_y_plus = psi_real.submat(1, 2, nx-2, ny-1);  // psi(x, y+1)
    mat psi_real_y_minus = psi_real.submat(1, 0, nx-2, ny-3); // psi(x, y-1)
    mat psi_imag_y_plus = psi_imag.submat(1, 2, nx-2, ny-1);
    mat psi_imag_y_minus = psi_imag.submat(1, 0, nx-2, ny-3);
    
    // Mise à jour de la fonction d'onde pour les points intérieurs
    psi_real_next.submat(1, 1, nx-2, ny-2) = psi_real_inner - dt * (A % psi_imag_inner + coef_x * (psi_imag_x_plus+psi_imag_x_minus) + coef_y * (psi_imag_y_plus+psi_imag_y_minus)) ;
    psi_imag_next.submat(1, 1, nx-2, ny-2) = psi_real_inner + dt * (A % psi_real_inner + coef_x * (psi_real_x_plus+psi_real_x_minus) + coef_y * (psi_real_y_plus+psi_real_y_minus)) ;
    
    // Mettre à jour les matrices d'origine
    psi_real = psi_real_next;
    psi_imag = psi_imag_next;
}
