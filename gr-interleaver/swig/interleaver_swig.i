/* -*- c++ -*- */

#define INTERLEAVER_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "interleaver_swig_doc.i"

%{
#include "interleaver/interleaver.h"
%}


%include "interleaver/interleaver.h"
GR_SWIG_BLOCK_MAGIC2(interleaver, interleaver);
