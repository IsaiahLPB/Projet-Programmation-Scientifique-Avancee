#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>

#include "../lib/complexmat.h"

using namespace arma;

class Solver
{
public:
  Solver();
  complex_mat FTCS_derivation(complex_mat);
  complex_mat BTCS_derivation(complex_mat);
  complex_mat CTCS_derivation(complex_mat);
  mat V;

private:
  int h_bar = 1;
  int m = 1;
  int x_min = -10;
  int x_max = 10;
  int y_min = -10;
  int y_max = 10;
  uword nx = 101;
  uword ny = 101;
  int t_max = 10;
  /*
   * dt[0] - FTCS
   * dt[1] - BTCS
   * dt[2] - CTCS 
  */
  double dt_vals[3] = {0.02/800, 0.02/40, 0.02/4};
};
#endif
