#ifndef COMPLEXMAT_H
#define COMPLEXMAT_H

#include <armadillo>

using namespace arma;

typedef struct complex_mat
{
  mat re;
  mat im;
}complex_mat;

complex_mat init_c_mat(uword, uword);

class ComplexMat
{
public:
  ComplexMat(mat, mat);
  mat Re(complex_mat);
  mat Im(complex_mat);
};

#endif