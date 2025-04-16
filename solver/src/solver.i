%module solver
%include "exception.i"

%exception
{
  try
  {
    $action
  }
  catch (const std::runtime_error& e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
  }
  catch (const std::logic_error& e) {
    SWIG_exception(SWIG_IndexError, e.what());
  }
  catch (const std::string s) {
    SWIG_exception(SWIG_RuntimeError, s.c_str());
  }
}

%{
#define SWIG_FILE_WITH_INIT
#include "../include/solver.h"
#include "../include/TimeStepInfo.h"
%}

%include "armanpy.i"

%include "../include/solver.h"
%include "../include/TimeStepInfo.h"