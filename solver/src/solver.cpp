#include <iostream>
#include <armadillo>

#include "../lib/solver.h"
#include "../lib/complexmat.h"

using namespace arma;

Solver::Solver()
{
	
}

complex_mat Solver::FTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt;

  double dt = dt_vals[0];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  for(uword i = 1; i < nx; ++i)
  {
    for(uword j = 1; j < ny; ++j)
    {
      psi_t_dt.re(i,j) = psi_t.re(i,j) - dt * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * psi_t.im(i,j) + (h_bar/2*m) * ((1/dx*dx) * (psi_t.im(i+1,j) + psi_t.im(i-1,j)) + (1/dy*dy) * (psi_t.im(i,j+1) + psi_t.im(i,j-1))));
      psi_t_dt.im(i,j) = psi_t.im(i,j) + dt * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * psi_t.re(i,j) + (h_bar/2*m) * ((1/dx*dx) * (psi_t.re(i+1,j) + psi_t.re(i-1,j)) + (1/dy*dy) * (psi_t.re(i,j+1) + psi_t.re(i,j-1))));
    }
  }
  return psi_t_dt;
}

complex_mat Solver::BTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt;
  complex_mat new_psi_t_dt;

  double dt = dt_vals[1];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  // We approximate psi_t_dt by psi_t and affinate by the result of each iteration (Euler's method)
  new_psi_t_dt = psi_t;
  while(arma::approx_equal(psi_t_dt.re, new_psi_t_dt.re, "absdiff", epsilon) == false ||
        arma::approx_equal(psi_t_dt.im, new_psi_t_dt.im, "absdiff", epsilon) == false )
  {
    psi_t_dt = new_psi_t_dt;
    for(uword i = 1; i < nx; ++i)
    {
      for(uword j = 1; j < ny; ++j)
      {
        new_psi_t_dt.re(i,j) = psi_t.re(i,j) - dt * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * psi_t_dt.im(i,j) + (h_bar/2*m) * ((1/dx*dx) * (psi_t_dt.im(i+1,j) + psi_t_dt.im(i-1,j)) + (1/dy*dy) * (psi_t_dt.im(i,j+1) + psi_t_dt.im(i,j-1))));
        new_psi_t_dt.im(i,j) = psi_t.im(i,j) + dt * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * psi_t_dt.re(i,j) + (h_bar/2*m) * ((1/dx*dx) * (psi_t_dt.re(i+1,j) + psi_t_dt.re(i-1,j)) + (1/dy*dy) * (psi_t_dt.re(i,j+1) + psi_t_dt.re(i,j-1))));
      }
    }
  }
  return new_psi_t_dt;
}

complex_mat Solver::CTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt;
  complex_mat new_psi_t_dt;

  double dt = dt_vals[2];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  // We approximate psi_t_dt by psi_t and affinate by the result of each iteration (Euler's method)
  new_psi_t_dt = psi_t;
  while(arma::approx_equal(psi_t_dt.re, new_psi_t_dt.re, "absdiff", epsilon) == false ||
        arma::approx_equal(psi_t_dt.im, new_psi_t_dt.im, "absdiff", epsilon) == false )
  {
    psi_t_dt = new_psi_t_dt;
    for(uword i = 1; i < nx; ++i)
    {
      for(uword j = 1; j < ny; ++j)
      {
        new_psi_t_dt.re(i,j) = psi_t.re(i,j) - (dt/2) * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * (psi_t.im(i,j)+psi_t_dt.im(i,j)) + (h_bar/2*m) * ((1/dx*dx) * (psi_t.im(i+1,j) + psi_t.im(i-1,j)) * (psi_t_dt.im(i+1,j) + psi_t_dt.im(i-1,j)) + (1/dy*dy) * (psi_t.im(i,j+1) + psi_t.im(i,j-1)) * (psi_t_dt.im(i,j+1) + psi_t_dt.im(i,j-1))));
        new_psi_t_dt.im(i,j) = psi_t.im(i,j) + (dt/2) * (((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy))) * (psi_t.re(i,j)+psi_t_dt.im(i,j)) + (h_bar/2*m) * ((1/dx*dx) * (psi_t.re(i+1,j) + psi_t.re(i-1,j)) * (psi_t_dt.re(i+1,j) + psi_t_dt.re(i-1,j)) + (1/dy*dy) * (psi_t.re(i,j+1) + psi_t.re(i,j-1)) * (psi_t_dt.re(i,j+1) + psi_t_dt.re(i,j-1))));
      }
    }
  }
  return new_psi_t_dt;
}
