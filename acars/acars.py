#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Acars
# Generated: Sun Apr 15 15:53:08 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import acars2
import osmosdr
import wx


class acars(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Acars")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.xlate_fir_taps = xlate_fir_taps = firdes.low_pass_2(1, samp_rate, 5e3, 100, 60)
        self.audio_rate = audio_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=131.725e6,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=131.525e6,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(25e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(0, 0)
        self.rtlsdr_source_0.set_if_gain(0, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (xlate_fir_taps), 0, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (xlate_fir_taps), 0, samp_rate)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/djustinf/Git/EE-504-Intro-Project/acars/output_01.txt', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/djustinf/Git/EE-504-Intro-Project/acars/output_00.txt', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.audio_sink_0_0 = audio.sink(audio_rate, 'pulse', True)
        self.acars2_demod_0_0 = acars2.demod(audio_rate, False)
        self.acars2_demod_0 = acars2.demod(audio_rate, False)
        self.acars2_decode_0_0 = acars2.decode()
        self.acars2_decode_0 = acars2.decode()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.acars2_decode_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.acars2_decode_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.acars2_demod_0, 0), (self.acars2_decode_0, 0))
        self.connect((self.acars2_demod_0_0, 0), (self.acars2_decode_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.acars2_demod_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.acars2_demod_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.audio_sink_0_0, 1))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlate_fir_taps(firdes.low_pass_2(1, self.samp_rate, 5e3, 100, 60))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_xlate_fir_taps(self):
        return self.xlate_fir_taps

    def set_xlate_fir_taps(self, xlate_fir_taps):
        self.xlate_fir_taps = xlate_fir_taps
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.xlate_fir_taps))
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.xlate_fir_taps))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate


def main(top_block_cls=acars, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
