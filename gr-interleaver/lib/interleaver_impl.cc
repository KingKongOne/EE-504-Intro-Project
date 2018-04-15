/* -*- c++ -*- */
/* 
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <math.h>
#include "interleaver_impl.h"

namespace gr {
  namespace interleaver {

    interleaver::sptr
    interleaver::make(size_t itemsize, unsigned int blocksize)
    {
      return gnuradio::get_initial_sptr
        (new interleaver_impl(itemsize, blocksize));
    }

    /*
     * The private constructor
     */
    interleaver_impl::interleaver_impl(size_t itemsize, unsigned int blocksize)
      : gr::block("interleaver",
              gr::io_signature::make(1, io_signature::IO_INFINITE, itemsize),
              gr::io_signature::make(1, 1, itemsize))
    {
      this->size = itemsize;
      this->block = blocksize;
    }

    /*
     * Our virtual destructor.
     */
    interleaver_impl::~interleaver_impl()
    {
    }

    /*
     * Ensures input and output combination is valid
     */
    bool interleaver_impl::check_topology (int ninputs, int noutputs) {
      this->set_output_multiple(this->block * ninputs);
      return true;
    }

    /*
     * Checks if input streams have the correct number of elements to call 'general_work'
     */
    void
    interleaver_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      for (int i = 0; i < ninput_items_required.size(); i++) {
        ninput_items_required[i] = (int) ceil(noutput_items/ninput_items_required.size());
      }
    }

    int
    interleaver_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const uint8_t **in = (const uint8_t **) &input_items[0];
      uint8_t  *out = (uint8_t *) output_items[0];

      for (int i = 0; i < (int) ceil(noutput_items/this->block); i++) {
        for (int j = 0; j < ninput_items.size(); j++) {
          std::memcpy(out, in[j], this->size*this->block);
          out += this->size*this->block;
          in[j] += this->size*this->block;
        }
      }
      
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each ((int) ceil(noutput_items/ninput_items.size()));

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace interleaver */
} /* namespace gr */

