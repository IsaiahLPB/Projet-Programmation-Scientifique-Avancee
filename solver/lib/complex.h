#ifndef COMPLEX_H
#define COMPLEX_H

typedef struct complex
{
  float re;
  float im;
}complex;

class Complex
{
public:
  Complex(float, float);
  float Re(complex);
  float Im(complex);
};

#endif