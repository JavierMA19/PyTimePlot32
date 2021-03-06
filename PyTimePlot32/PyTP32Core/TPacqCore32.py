#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:13:45 2019

@author: aguimera
"""
import PyqtTools.DaqInterface as DaqInt
import numpy as np


# Daq card connections mapping 'Chname':(DCout, ACout)
aiChannels = {'Ch01': 'ai8',
              'Ch11': 'ai12',
              'Ch03': 'ai9',
              'Ch09': 'ai15',
              'Ch05': 'ai10',
              'Ch15': 'ai14',
              'Ch07': 'ai11',
              'Ch13': 'ai13',
              'Ch02': 'ai0',
              'Ch12': 'ai4',
              'Ch04': 'ai1',
              'Ch10': 'ai7',
              'Ch06': 'ai2',
              'Ch16': 'ai6',
              'Ch08': 'ai3',
              'Ch14': 'ai5',
              'Ch27': 'ai27',
              'Ch17': 'ai29',
              'Ch25': 'ai26',
              'Ch19': 'ai30',
              'Ch31': 'ai25',
              'Ch21': 'ai31',
              'Ch29': 'ai24',
              'Ch23': 'ai28',
              'Ch28': 'ai19',
              'Ch18': 'ai21',
              'Ch26': 'ai18',
              'Ch20': 'ai22',
              'Ch32': 'ai17',
              'Ch22': 'ai23',
              'Ch30': 'ai16',
              'Ch24': 'ai20'}

DOChannels = ['port0/line0:15', ]

DOChannels = ['port0/line0:9', ]
Decoder = ['port0/line10:15', ]

##############################################################################


class ChannelsConfig():

    ChannelIndex = None
    ChNamesList = None
    AnalogInputs = None
    DigitalOutputs = None
    SwitchOut = None
    Dec = None
    DCSwitch = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, ], dtype=np.uint8)
    ACSwitch = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8)
    DecDigital = np.array([0, 1, 0, 1, 1], dtype=np.uint8) # Ouput should be: P26
    # Events list
    DataEveryNEvent = None
    DataDoneEvent = None

    def _InitAnalogInputs(self):
        self.ChannelIndex = {}
        InChans = []

        index = 0
        for ch in self.ChNamesList:
            InChans.append(aiChannels[ch])
            self.ChannelIndex[ch] = (index)
            index += 1

        self.AnalogInputs = DaqInt.ReadAnalog(InChans=InChans)
        # events linking
        self.AnalogInputs.EveryNEvent = self.EveryNEventCallBack
        self.AnalogInputs.DoneEvent = self.DoneEventCallBack

    def _InitAnalogOutputs(self, ChVds, ChVs):
        print('ChVds ->', ChVds)
        print('ChVs ->', ChVs)
        self.VsOut = DaqInt.WriteAnalog((ChVs,))
        self.VdsOut = DaqInt.WriteAnalog((ChVds,))

    def __init__(self, Channels,
                 AcqDC=True, AcqAC=True,
                 ChVds='ao0', ChVs='ao1',
                 ACGain=1e6, DCGain=10e3):
        print('InitChannels')
        self._InitAnalogOutputs(ChVds=ChVds, ChVs=ChVs)

        self.ChNamesList = sorted(Channels)
        self.AcqAC = AcqAC
        self.AcqDC = AcqDC
        self.ACGain = ACGain
        self.DCGain = DCGain
        self._InitAnalogInputs()

        self.SwitchOut = DaqInt.WriteDigital(Channels=DOChannels)
        self.Dec = DaqInt.WriteDigital(Channels=Decoder)

    def StartAcquisition(self, Fs, Refresh, Vgs, Vds, **kwargs):
        self.SetBias(Vgs=Vgs, Vds=Vds)
        if self.AcqDC:
            print('DC')
            self.SetDigitalSignal(Signal=self.DCSwitch)
        if self.AcqAC:
            print('AC')
            self.SetDigitalSignal(Signal=self.ACSwitch)

        EveryN = Refresh*Fs # TODO check this
        self.AnalogInputs.ReadContData(Fs=Fs,
                                       EverySamps=EveryN)

    def SetBias(self, Vgs, Vds):
        print('ChannelsConfig SetBias Vgs ->', Vgs, 'Vds ->', Vds)
        self.VdsOut.SetVal(Vds)
        self.VsOut.SetVal(-Vgs)
        self.BiasVd = Vds-Vgs
        self.Vgs = Vgs
        self.Vds = Vds

    def SetDigitalSignal(self, Signal):
        if not self.SwitchOut:
            self.SwitchOut = DaqInt.WriteDigital(Channels=DOChannels)
        self.SwitchOut.SetDigitalSignal(Signal)
        self.Dec.SetDigitalSignal(self.DecDigital)

    def _SortChannels(self, data, SortDict):
        (samps, inch) = data.shape
        sData = np.zeros((samps, len(SortDict)))
        for chn, inds in sorted(SortDict.items()):
            sData[:, inds] = data[:, inds]

        return sData

    def EveryNEventCallBack(self, Data):
        _DataEveryNEvent = self.DataEveryNEvent

        if _DataEveryNEvent is not None:
            if self.AcqDC:
                aiDataDC = self._SortChannels(Data, self.ChannelIndex)
                aiDataDC = (aiDataDC-self.BiasVd) / self.DCGain

            if self.AcqAC:
                aiDataAC = self._SortChannels(Data, self.ChannelIndex)
                aiDataAC = aiDataAC / self.ACGain

            if self.AcqAC and self.AcqDC:
                print('ERROR')
                aiData = np.hstack((aiDataDC, aiDataAC))
                _DataEveryNEvent(aiData)
            elif self.AcqAC:
                _DataEveryNEvent(aiDataAC)
            elif self.AcqDC:
                _DataEveryNEvent(aiDataDC)

    def DoneEventCallBack(self, Data):
        print('Done callback')

    def Stop(self):
        print('Stopppp')
        self.SetBias(Vgs=0, Vds=0)
        self.AnalogInputs.StopContData()
        if self.SwitchOut is not None:
            print('Clear Digital')
            self.SwitchOut.ClearTask()
            self.SwitchOut = None




