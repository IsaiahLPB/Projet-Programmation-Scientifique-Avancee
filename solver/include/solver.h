#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>

#include "../include/complexmat.h"

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
  Solver();
  complex_mat FTCS_derivation(complex_mat);
  complex_mat BTCS_derivation(complex_mat);
  complex_mat CTCS_derivation(complex_mat);
  arma::mat V;

  /*
   * dt[0] - FTCS
   * dt[1] - BTCS
   * dt[2] - CTCS 
  */
  double dt_vals[3] = {0.02/800, 0.02/40, 0.02/4};
};
#endif
