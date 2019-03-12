from PyQt5 import QtGui  
from PyQt5 import QtCore  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from util.qt_util import *
from util.pyqtgraph_util import *


class Plotter():
    def __init__(self,w):
        layout_main = QVBoxLayout()
        fig = create_fig()
        fig.setTitle('Raw PPG')
        addLabels(fig,'time','intensity','-','sec')
        self.plt_r = plot(fig,np.arange(0,5),np.arange(0,5),[255,0,0])
       layout_main.addWidget(fig)

        w.setLayout(layout_main)
    
        
    def update_data(self):
        
        num_frames = self.sensor.rppg.shape[1]
        start = max([num_frames-100,0])
        t = np.arange(num_frames)/self.processor.fs
        rPPG = self.sensor.rppg
        if self.update_id == 0:
            self.plt_r.setData(t[start:num_frames],rPPG[0,start:num_frames])
            self.plt_g.setData(t[start:num_frames],rPPG[1,start:num_frames])
            self.plt_b.setData(t[start:num_frames],rPPG[2,start:num_frames])
        
        if self.processor.enough_samples:
            if self.update_id == 1:
                self.plt_x.setData(t[-300:],self.processor.x_stride_method)
            elif self.update_id == 2:
                snr = self.evaluator.snr
                self.plt_snr.setData(t[-min(100,len(snr)):],snr[-min(100,len(snr)):])
            elif self.update_id == 3:
                self.plt_bpm.setData(self.f,self.processor.normalized_amplitude)
            elif self.update_id == 4:
                bpm_movavg = self.evaluator.bpm
                #bpm_movavg = np.convolve(self.evaluator.bpm, np.ones((100,))/100, mode='valid')
                self.plt_bpmdt.setData(t[-min(200,len(bpm_movavg)):],bpm_movavg[-min(200,len(bpm_movavg)):])

        self.update_id+=1
        if self.update_id == 5:
            self.update_id = 0
        
