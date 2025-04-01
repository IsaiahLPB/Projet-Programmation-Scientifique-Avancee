#ifndef COMPLEXMAT_H
#define COMPLEXMAT_H

#include <armadillo>

typedef struct complex_mat
{
  arma::mat re;
  arma::mat im;
}complex_mat;

complex_mat init_c_mat(arma::uword, arma::uword);

class ComplexMat
{
public:
  ComplexMat(arma::mat, arma::mat);
  arma::mat Re(complex_mat);
  arma::mat Im(complex_mat);
};

#endif