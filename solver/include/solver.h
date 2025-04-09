#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>
#include <complex>

const double epsilon = 10e-6;
const int h_bar = 1;
const int m = 1;
const int x_min = -10;
const int x_max = 10;
const int y_min = -10;
const int y_max = 10;
const arma::uword nx = 101;
const arma::uword ny = 101;
const int t_max = 10;

class Solver
{
public:
  Solver(int, arma::mat);
  void FTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag);
  void BTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag);
  void CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag);
  arma::mat V_inner;

  /*
   * dt[0] - FTCS
   * dt[1] - BTCS
   * dt[2] - CTCS 
  */
  double dt_vals[3] = {0.02/800, 0.02/40, 0.02/4};
  double dt;
  double dx;
  double dy;
  arma::mat A;
  double coef_x;
  double coef_y;
};
#endif
