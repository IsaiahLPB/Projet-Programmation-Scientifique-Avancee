#include "../lib/complex.h"

Complex::Complex(float re_val, float im_val)
{
  complex z;
  z.re = re_val;
  z.im = im_val;
}

float Complex::Re(complex z)
{
	return z.re;
}

float Complex::Im(complex z)
{
	return z.im;
}
