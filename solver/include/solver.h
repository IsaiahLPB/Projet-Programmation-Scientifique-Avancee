#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>
#include <complex>
#include <string>

#include "../include/TimeStepInfo.h"

class Solver
{
public:
  Solver(arma::mat V, const char *path);
  void FTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag, TimeStepInfo &info);
  void BTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag, TimeStepInfo &info);
  void CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag, TimeStepInfo &info);
  double Calc_norm(arma::mat &psi_real, arma::mat &psi_imag);
  arma::mat V_inner;

  const double epsilon = 10e-6;
  const int max_iter = 100; // Maximum number of iteration (to prevent infite loop)

  arma::mat diff_real;
  arma::mat diff_imag;

  arma::mat psi_real_prev;
  arma::mat psi_imag_prev;

  double h_bar;
  double m;
  double x_min;
  double x_max;
  double y_min;
  double y_max;
  arma::uword nx;
  arma::uword ny;
  int nx_1;
  int ny_1;
  int nx_2;
  int ny_2;
  int nx_3;
  int ny_3;
  double dt_2;
  int t_max;

  std::string method;
  double dt;
  double dx;
  double dy;
  arma::mat A;
  double coef_x;
  double coef_y;

  arma::mat psi_real_next;
  arma::mat psi_imag_next;
};
#endif
