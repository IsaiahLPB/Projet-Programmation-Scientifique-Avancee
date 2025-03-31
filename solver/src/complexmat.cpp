#include <armadillo>

#include "../include/complexmat.h"
#include "../include/solver.h"

using namespace arma;

complex_mat init_c_mat(uword n, uword m)
{
	complex_mat M;
  M.re.zeros(n, m);
  M.im.zeros(n, m);
  return M;
}

ComplexMat::ComplexMat(mat re_val, mat im_val)
{
  complex_mat M;
  M.re = re_val;
  M.im = im_val;
}

mat ComplexMat::Re(complex_mat M)
{
	return M.re;
}

mat ComplexMat::Im(complex_mat M)
{
	return M.im;
}
