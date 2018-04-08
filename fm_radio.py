#!/usr/bin/env python2

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio import filter
from gnuradio import analog
from gnuradio import audio
from gnuradio.wxgui import fftsink2
import osmosdr
import argparse

class fm_radio(gr.top_block):

  def __init__(self, freq=99.1):

    gr.top_block.__init__(self)

    # Variables
    freq *= 1000000
    self.sample_rate = 250000
    self.gain = 40
    self.audio_rate = 48000
    self.audio_interp = 4

    # Blocks

    # RTLSDR Source Block
    self.rtl_src = osmosdr.source( args= 'numchan=1 ' )
    self.rtl_src.set_sample_rate(self.sample_rate)
    self.rtl_src.set_center_freq(freq, 0)
    self.rtl_src.set_freq_corr(0, 0)
    self.rtl_src.set_dc_offset_mode(0, 0)
    self.rtl_src.set_iq_balance_mode(0, 0)
    self.rtl_src.set_gain_mode(True, 0)
    self.rtl_src.set_gain(self.gain, 0)
    self.rtl_src.set_if_gain(20, 0)
    self.rtl_src.set_bb_gain(20, 0)
    self.rtl_src.set_antenna('TX/RX', 0)
    self.rtl_src.set_bandwidth(0, 0)

    # Low pass filter
    self.low_pass = filter.fir_filter_ccf(int(self.sample_rate),
      firdes.low_pass(
        self.gain,
        self.sample_rate,
        20000,
        1000,
        firdes.WIN_HAMMING,
        6.76
      )
    )

    # Resampler
    self.resampler = filter.rational_resampler_ccc(
      interpolation=self.audio_rate*self.audio_interp,
      decimation=int(self.sample_rate),
      taps=None,
      fractional_bw=None,
    )

    # Rcv
    self.wfm_rcv = analog.wfm_rcv(
      quad_rate=self.audio_rate*self.audio_interp,
      audio_decimation=self.audio_interp
    )

    # Sink
    self.audio_sink = audio.sink(self.audio_rate, '', True)

    # Connections
    self.connect((self.rtl_src, 0), (self.resampler, 0))
    self.connect((self.resampler, 0), (self.low_pass, 0))
    self.connect((self.low_pass, 0), (self.wfm_rcv, 0))
    self.connect((self.wfm_rcv, 0), (self.audio_sink, 0))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Enter a frequency')
  parser.add_argument('-f', '--frequency', type=float, required=True)
  args = parser.parse_args()
  fm_radio(args.frequency).run()
