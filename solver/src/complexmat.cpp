#include <armadillo>

#include "../lib/complexmat.h"

using namespace arma;

ComplexMat::ComplexMat(mat re_val, mat im_val)
{
  complex_mat M;
  M.re = re_val;
  M.im = im_val;
}

mat ComplexMat::Re(complex_mat z)
{
	return z.re;
}

mat ComplexMat::Im(complex_mat z)
{
	return z.im;
}
