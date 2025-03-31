#include <armadillo>

#include "../include/solver.h"
#include "../include/complexmat.h"

using namespace arma;

Solver::Solver()
{
	
}

complex_mat Solver::FTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt = init_c_mat(nx, ny);

  double dt = dt_vals[0];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  for(uword i = 1; i < nx-1; ++i)
  {
    for(uword j = 1; j < ny-1; ++j)
    {
      double A = ((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy)));
      double B = (h_bar/2*m);
      double psi_x_im = psi_t.im(i+1,j) + psi_t.im(i-1,j);
      double psi_y_im = psi_t.im(i,j+1) + psi_t.im(i,j-1);
      double psi_x_re = psi_t.re(i+1,j) + psi_t.re(i-1,j);
      double psi_y_re = psi_t.re(i,j+1) + psi_t.re(i,j-1);

      psi_t_dt.re(i,j) = psi_t.re(i,j) - dt * (A * psi_t.im(i,j) + B * ((1/dx*dx) * psi_x_im + (1/dy*dy) * psi_y_im));
      psi_t_dt.im(i,j) = psi_t.im(i,j) + dt * (A * psi_t.re(i,j) + B * ((1/dx*dx) * psi_x_re + (1/dy*dy) * psi_y_re));
    }
  }
  return psi_t_dt;
}

complex_mat Solver::BTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt = init_c_mat(nx, ny);
  complex_mat new_psi_t_dt = init_c_mat(nx, ny);  

  double dt = dt_vals[1];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  // We approximate psi_t_dt by psi_t and affinate by the result of each iteration (Euler's method)
  new_psi_t_dt = psi_t;
  while(arma::approx_equal(psi_t_dt.re, new_psi_t_dt.re, "absdiff", epsilon) == false ||
        arma::approx_equal(psi_t_dt.im, new_psi_t_dt.im, "absdiff", epsilon) == false )
  {
    psi_t_dt = new_psi_t_dt;
    for(uword i = 1; i < nx-1; ++i)
    {
      for(uword j = 1; j < ny-1; ++j)
      {
        double A = ((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy)));
        double B = (h_bar/2*m);
        double psi_x_im = psi_t_dt.im(i+1,j) + psi_t_dt.im(i-1,j);
        double psi_y_im = psi_t_dt.im(i,j+1) + psi_t_dt.im(i,j-1);
        double psi_x_re = psi_t_dt.re(i+1,j) + psi_t_dt.re(i-1,j);
        double psi_y_re = psi_t_dt.re(i,j+1) + psi_t_dt.re(i,j-1);

        new_psi_t_dt.re(i,j) = psi_t.re(i,j) - dt * (A * psi_t_dt.im(i,j) + B * ((1/dx*dx) * psi_x_im + (1/dy*dy) * psi_y_im));
        new_psi_t_dt.im(i,j) = psi_t.im(i,j) + dt * (A * psi_t_dt.re(i,j) + B * ((1/dx*dx) * psi_x_re + (1/dy*dy) * psi_y_re));
      }
    }
  }
  return new_psi_t_dt;
}

complex_mat Solver::CTCS_derivation(complex_mat psi_t)
{
  complex_mat psi_t_dt = init_c_mat(nx, ny);
  complex_mat new_psi_t_dt = init_c_mat(nx, ny);

  double dt = dt_vals[2];
  int dx = (x_max - x_min) / nx;
  int dy = (y_max - y_min) / ny;  

  // We approximate psi_t_dt by psi_t and affinate by the result of each iteration (Euler's method)
  new_psi_t_dt = psi_t;
  while(arma::approx_equal(psi_t_dt.re, new_psi_t_dt.re, "absdiff", epsilon) == false ||
        arma::approx_equal(psi_t_dt.im, new_psi_t_dt.im, "absdiff", epsilon) == false )
  {
    psi_t_dt = new_psi_t_dt;
    for(uword i = 1; i < nx-1; ++i)
    {
      for(uword j = 1; j < ny-1; ++j)
      {
        double A = ((-1/h_bar)*V(i,j) - ((h_bar/m) * (1/dx*dx + 1/dy*dy)));
        double B = (h_bar/2*m);
        double psi_x_im = psi_t.im(i+1,j) + psi_t.im(i-1,j);
        double psi_y_im = psi_t.im(i,j+1) + psi_t.im(i,j-1);
        double psi_x_re = psi_t.re(i+1,j) + psi_t.re(i-1,j);
        double psi_y_re = psi_t.re(i,j+1) + psi_t.re(i,j-1);
        double psi_dt_x_im = psi_t_dt.im(i+1,j) + psi_t_dt.im(i-1,j);
        double psi_dt_y_im = psi_t_dt.im(i,j+1) + psi_t_dt.im(i,j-1);
        double psi_dt_x_re = psi_t_dt.re(i+1,j) + psi_t_dt.re(i-1,j);
        double psi_dt_y_re = psi_t_dt.re(i,j+1) + psi_t_dt.re(i,j-1);

        new_psi_t_dt.re(i,j) = psi_t.re(i,j) - (dt/2) * (A * (psi_t.im(i,j)+psi_t_dt.im(i,j)) + B * ((1/dx*dx) * psi_x_im * psi_dt_x_im + (1/dy*dy) * psi_y_im * psi_dt_y_im));
        new_psi_t_dt.im(i,j) = psi_t.im(i,j) + (dt/2) * (A * (psi_t.re(i,j)+psi_t_dt.im(i,j)) + B * ((1/dx*dx) * psi_x_re * psi_dt_x_re + (1/dy*dy) * psi_y_re * psi_dt_y_re));
      }
    }
  }
  return new_psi_t_dt;
}
