#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>
#include <complex>
#include <string>

#include "../include/TimeStepInfo.h"

class Solver
{
public:
  Solver(arma::mat);
  void FTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag, TimeStepInfo &info);
  void BTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag);
  void CTCS_derivation(arma::mat &psi_real, arma::mat &psi_imag);
  arma::mat V_inner;

  const double epsilon = 10e-6;
  double h_bar;
  double m;
  int x_min;
  int x_max;
  int y_min;
  int y_max;
  arma::uword nx;
  arma::uword ny;
  int t_max;

  std::string method;
  double dt;
  double dx;
  double dy;
  arma::mat A;
  double coef_x;
  double coef_y;
};
#endif
