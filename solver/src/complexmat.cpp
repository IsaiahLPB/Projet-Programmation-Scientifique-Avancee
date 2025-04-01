#include <armadillo>

#include "../include/complexmat.h"
#include "../include/solver.h"

complex_mat init_c_mat(arma::uword n, arma::uword m)
{
	complex_mat M;
  M.re.zeros(n, m);
  M.im.zeros(n, m);
  return M;
}

ComplexMat::ComplexMat(arma::mat re_val, arma::mat im_val)
{
  complex_mat M;
  M.re = re_val;
  M.im = im_val;
}

arma::mat ComplexMat::Re(complex_mat M)
{
	return M.re;
}

arma::mat ComplexMat::Im(complex_mat M)
{
	return M.im;
}
