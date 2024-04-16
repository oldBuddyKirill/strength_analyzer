#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Strength Analizer
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from channel_spectrum_writer import channel_spectrum_writer  # grc-generated hier_block
from datetime import datetime
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time
import sip



class strength_analyzer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Strength Analizer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Strength Analizer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "strength_analyzer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.input_decimation = input_decimation = 50
        self.transition_width = transition_width = 5e3
        self.main_sample_rate = main_sample_rate = samp_rate / input_decimation
        self.if_gain = if_gain = 24
        self.data_dir = data_dir = "data/"
        self.cutoff_freq = cutoff_freq = 50e3
        self.channel_9 = channel_9 = 93.3e6
        self.channel_8 = channel_8 = 92.9e6
        self.channel_7 = channel_7 = 90.6e6
        self.channel_6 = channel_6 = 90.1e6
        self.channel_5 = channel_5 = 89.7e6
        self.channel_4 = channel_4 = 89.3e6
        self.channel_3 = channel_3 = 88.4e6
        self.channel_2 = channel_2 = 88e6
        self.channel_12 = channel_12 = 95.5e6
        self.channel_11 = channel_11 = 95e6
        self.channel_10 = channel_10 = 94.1e6
        self.channel_1 = channel_1 = 87.5e6
        self.center_freq = center_freq = 91e6
        self.bb_gain = bb_gain = 30

        ##################################################
        # Blocks
        ##################################################

        self._if_gain_range = Range(0, 40, 8, 24, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "'if_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._if_gain_win)
        self._center_freq_range = Range(80e6, 120e6, 0.1e6, 91e6, 200)
        self._center_freq_win = RangeWidget(self._center_freq_range, self.set_center_freq, "Center Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_freq_win)
        self._bb_gain_range = Range(0, 62, 2, 30, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "'bb_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bb_gain_win)
        self.qtgui_sink_x_0_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Spectrum analizer", #name
            True, #plotfreq
            True, #plotwaterfall
            False, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(30, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.channel_spectrum_writer_0_5 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_7,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_4_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_12,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_4 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_6,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_3_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_11,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_3 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_5,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_2_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_10,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_2 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_4,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_1_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_9,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_1 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_3,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_0_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_8,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_2,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.channel_spectrum_writer_0 = channel_spectrum_writer(
            center_freq=center_freq,
            channel_freq=channel_1,
            cutoff_freq=cutoff_freq,
            file_dir=data_dir,
            input_decimation=input_decimation,
            samp_rate=samp_rate,
            transition_width=transition_width,
        )
        self.blocks_throttle2_2 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_0_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_1, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_1_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_2, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_2_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_3, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_3_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_4, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_4_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.channel_spectrum_writer_0_5, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.qtgui_sink_x_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_throttle2_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "strength_analyzer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_main_sample_rate(self.samp_rate / self.input_decimation)
        self.blocks_throttle2_2.set_sample_rate(self.samp_rate)
        self.channel_spectrum_writer_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_0_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_1.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_1_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_2.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_2_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_3.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_3_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_4.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_4_0.set_samp_rate(self.samp_rate)
        self.channel_spectrum_writer_0_5.set_samp_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0_0_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_input_decimation(self):
        return self.input_decimation

    def set_input_decimation(self, input_decimation):
        self.input_decimation = input_decimation
        self.set_main_sample_rate(self.samp_rate / self.input_decimation)
        self.channel_spectrum_writer_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_0_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_1.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_1_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_2.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_2_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_3.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_3_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_4.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_4_0.set_input_decimation(self.input_decimation)
        self.channel_spectrum_writer_0_5.set_input_decimation(self.input_decimation)

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.channel_spectrum_writer_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_0_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_1.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_1_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_2.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_2_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_3.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_3_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_4.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_4_0.set_transition_width(self.transition_width)
        self.channel_spectrum_writer_0_5.set_transition_width(self.transition_width)

    def get_main_sample_rate(self):
        return self.main_sample_rate

    def set_main_sample_rate(self, main_sample_rate):
        self.main_sample_rate = main_sample_rate

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_data_dir(self):
        return self.data_dir

    def set_data_dir(self, data_dir):
        self.data_dir = data_dir
        self.channel_spectrum_writer_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_0_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_1.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_1_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_2.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_2_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_3.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_3_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_4.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_4_0.set_file_dir(self.data_dir)
        self.channel_spectrum_writer_0_5.set_file_dir(self.data_dir)

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.channel_spectrum_writer_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_0_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_1.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_1_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_2.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_2_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_3.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_3_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_4.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_4_0.set_cutoff_freq(self.cutoff_freq)
        self.channel_spectrum_writer_0_5.set_cutoff_freq(self.cutoff_freq)

    def get_channel_9(self):
        return self.channel_9

    def set_channel_9(self, channel_9):
        self.channel_9 = channel_9
        self.channel_spectrum_writer_0_1_0.set_channel_freq(self.channel_9)

    def get_channel_8(self):
        return self.channel_8

    def set_channel_8(self, channel_8):
        self.channel_8 = channel_8
        self.channel_spectrum_writer_0_0_0.set_channel_freq(self.channel_8)

    def get_channel_7(self):
        return self.channel_7

    def set_channel_7(self, channel_7):
        self.channel_7 = channel_7
        self.channel_spectrum_writer_0_5.set_channel_freq(self.channel_7)

    def get_channel_6(self):
        return self.channel_6

    def set_channel_6(self, channel_6):
        self.channel_6 = channel_6
        self.channel_spectrum_writer_0_4.set_channel_freq(self.channel_6)

    def get_channel_5(self):
        return self.channel_5

    def set_channel_5(self, channel_5):
        self.channel_5 = channel_5
        self.channel_spectrum_writer_0_3.set_channel_freq(self.channel_5)

    def get_channel_4(self):
        return self.channel_4

    def set_channel_4(self, channel_4):
        self.channel_4 = channel_4
        self.channel_spectrum_writer_0_2.set_channel_freq(self.channel_4)

    def get_channel_3(self):
        return self.channel_3

    def set_channel_3(self, channel_3):
        self.channel_3 = channel_3
        self.channel_spectrum_writer_0_1.set_channel_freq(self.channel_3)

    def get_channel_2(self):
        return self.channel_2

    def set_channel_2(self, channel_2):
        self.channel_2 = channel_2
        self.channel_spectrum_writer_0_0.set_channel_freq(self.channel_2)

    def get_channel_12(self):
        return self.channel_12

    def set_channel_12(self, channel_12):
        self.channel_12 = channel_12
        self.channel_spectrum_writer_0_4_0.set_channel_freq(self.channel_12)

    def get_channel_11(self):
        return self.channel_11

    def set_channel_11(self, channel_11):
        self.channel_11 = channel_11
        self.channel_spectrum_writer_0_3_0.set_channel_freq(self.channel_11)

    def get_channel_10(self):
        return self.channel_10

    def set_channel_10(self, channel_10):
        self.channel_10 = channel_10
        self.channel_spectrum_writer_0_2_0.set_channel_freq(self.channel_10)

    def get_channel_1(self):
        return self.channel_1

    def set_channel_1(self, channel_1):
        self.channel_1 = channel_1
        self.channel_spectrum_writer_0.set_channel_freq(self.channel_1)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.channel_spectrum_writer_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_0_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_1.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_1_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_2.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_2_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_3.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_3_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_4.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_4_0.set_center_freq(self.center_freq)
        self.channel_spectrum_writer_0_5.set_center_freq(self.center_freq)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.qtgui_sink_x_0_0_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)




def main(top_block_cls=strength_analyzer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
