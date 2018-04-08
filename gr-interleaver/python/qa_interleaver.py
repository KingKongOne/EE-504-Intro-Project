#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import interleaver_swig as interleaver

class qa_interleaver (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_interleave_ints (self):
        # set up fg
        src1 = (1, 2, 3, 4)
        src2 = (5, 6, 7, 8)
        res_exp = (1, 5, 2, 6, 3, 7, 4, 8)
        src1_blk = blocks.vector_source_i(src1)
        src2_blk = blocks.vector_source_i(src2)
        inter_blk = interleaver.interleaver(4, 1)
        dst_blk = blocks.vector_sink_i()
        self.tb.connect((src1_blk, 0), (inter_blk, 0))
        self.tb.connect((src2_blk, 0), (inter_blk, 1))
        self.tb.connect(inter_blk, dst_blk)
        self.tb.run ()
        # check data
        res_act = dst_blk.data()
        self.assertEqual(res_exp, res_act)


if __name__ == '__main__':
    gr_unittest.run(qa_interleaver, "qa_interleaver.xml")
