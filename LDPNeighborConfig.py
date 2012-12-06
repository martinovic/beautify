#!/usr/bin/python
# -*- coding: utf-8 *-*
__prj__ = 'intermedia'
__version__ = ''
__license__ = 'GNU General Public License v3'
__author__ = 'Marcelo Martinovic'
__email__ = 'marcelo.martinovic@gmail.com'
__url__ = ''
__date__ = '2012/11/25'

#import pdb
#
#pdb.set_trace()

from api.conection import Conection, Mailbox, Execution, REPLY_TRAP
#from api.interface import Api_Interface
from api.users import *
import wx
from gui import gui, guiWindow, Menu
#from template import Template
from ftplib import FTP
import binascii, md5
##import itertools as i_
from threading import Thread, Timer
from datetime import datetime
import time
import sys
import random
import math
from ini import _iniLoadConfig, _iniAppendConfig
from matplotlib.dates import date2num, strpdate2num, DateFormatter, SecondLocator
#from matplotlib.d import SecondLocator
import numpy as np
from UsuariosModel import UsuariosModel
from usuariosConfig import UsuariosConfig
import Spanish
#from argumentsClass import Arguments
#import collections
from apiConnection import ApiConnClass
# ----------------------------------------------------------
import logging
LOG_FILENAME = 'etera.log'
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG,)


# Compile Version
COMPILE_FOR_310 = False
# Usuario
user = User()
# Listas de Idioma
language = {}
language['Spanish'] = Spanish.language

# Ventana de configuracion de Watchdog


class LDPNeighborConfig(gui):
    '''
    Clase LDPNeighborConfig
    '''
    def __init__(self, _parent, _app, _pclass):
        '''
            Descripcion de la clase o metodo
            @param __VARIABLE__:
            @type __TIPO__:
            @param __VARIABLE__:
            @type __TIPO__:
            @return: void
        '''
        if not int(user['ldp_neighbor_config']):
            return
        self.windows = {}
        self.windows['parent'] = guiWindow(_parent)
        self.app = _app
        self.pclass = _pclass
        self.api = _plcass.api
        self.neighbor = _pclass.neighbor
#        self.yesno_answer      = ['no', 'yes']
        self.truefalse_answer = ['false', 'true']

        self.Add('EditWindow', 'dialog', self['parent'].frame,
            _value=language['Spanish']['ldp_neighbor'],
            _style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER |
            wx.MINIMIZE_BOX |
            wx.MAXIMIZE_BOX))
        self.Add('lblTransport', 'label', 'EditWindow',
            _value=language['Spanish']['transport'])
        self.Add('lblPeer', 'label', 'EditWindow',
            _value=language['Spanish']['peer'])
        self.Add('lblLocalTransport', 'label', 'EditWindow',
            _value=language['Spanish']['local_transport'])
        self.Add('lblAddresses', 'label', 'EditWindow',
            _value=language['Spanish']['addresses'])
        self.Add('txtTransport', 'text', 'EditWindow',
            _value=self.neighbor.get('transport', '0.0.0.0'))
        self.Add('txtPeer', 'text', 'EditWindow',
            _value=self.neighbor.get('peer', '0.0.0.0'))
        self.Add('txtLocalTransport', 'text', 'EditWindow',
            _value=self.neighbor.get('local - transport - peer', '00: 00: 05'))
        self.Add('txtAddresses', 'text', 'EditWindow',
            _value=self.neighbor.get('addresses', ''))
        self.Add('chkSendTargeted', 'check', 'EditWindow',
            _value=language['Spanish']['send_targeted'])

        self['EditWindow']['chkSendTargeted'].SetValue(bool(
            self.truefalse_answer.index(
            self.neighbor.get('send - targeted', 'true'))))

        # Sizers
        mainSiz = wx.BoxSizer(wx.VERTICAL)
        buttonSiz = wx.StdDialogButtonSizer()
        editSiz = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        editSiz.AddGrowableCol(1)

        if int(user['ldp_neighbor_config']) > 0:
            self.Add('btnOK', 'button', 'EditWindow',
                _id=wx.ID_OK,
                _value=language['Spanish']['ok'])
            self.Add('btnCancel', 'button', 'EditWindow',
                _id=wx.ID_CANCEL,
                _value=language['Spanish']['cancel'])
            buttonSiz.AddButton(
                self['EditWindow']['btnOK'])
            buttonSiz.Add((20, 20))
            buttonSiz.AddButton(
                self['EditWindow']['btnCancel'])
            self['EditWindow']['btnOK'].SetDefault()
            buttonSiz.Realize()
        else:
            self.Add('btnCancel', 'button', 'EditWindow',
                _id=wx.ID_CANCEL,
                _value=language['Spanish']['ok'])
            buttonSiz.AddButton(
                self['EditWindow']['btnCancel'])
            self['EditWindow']['btnCancel'].SetDefault()
            buttonSiz.Realize()

        editSiz.Add(
            self['EditWindow']['lblTransport'], 0,
            wx.ALIGN_RIGHT |
            wx.ALIGN_CENTER_VERTICAL)
        editSiz.Add(
            self['EditWindow']['txtTransport'], 0,
            wx.EXPAND)
        editSiz.Add((1, 1))
        editSiz.Add(
            self['EditWindow']['chkSendTargeted'], 0,
            wx.EXPAND)
        editSiz.Add(
            self['EditWindow']['lblPeer'], 0,
            wx.ALIGN_RIGHT |
            wx.ALIGN_CENTER_VERTICAL)
        editSiz.Add(
            self['EditWindow']['txtPeer'], 0,
            wx.EXPAND)
        editSiz.Add(
            self['EditWindow']['lblLocalTransport'], 0,
            wx.ALIGN_RIGHT |
            wx.ALIGN_CENTER_VERTICAL)
        editSiz.Add(
            self['EditWindow']['txtLocalTransport'], 0,
            wx.EXPAND)
        editSiz.Add(
            self['EditWindow']['lblAddresses'], 0,
            wx.ALIGN_RIGHT |
            wx.ALIGN_CENTER_VERTICAL)
        editSiz.Add(
            self['EditWindow']['txtAddresses'], 0,
            wx.EXPAND)

        mainSiz.Add(editSiz, 1, wx.EXPAND |
            wx.ALL, 10)
        mainSiz.Add(buttonSiz, 0,
            wx.ALL |
            wx.ALIGN_CENTER, 10)
        self['EditWindow'].frame.SetSizerAndFit(mainSiz)

        if self['EditWindow'].frame.ShowModal() == wx.ID_OK:
            if len(
                self.neighbor):
                cmd = 'set'
                attrs = {'.id': self.neighbor['.id']}
            else:
                cmd = 'add'
                attrs = {}

            attrs.update({ 'send - targeted': self.truefalse_answer[int(
                self['EditWindow']['chkSendTargeted'].GetValue())],
                            'transport': self['EditWindow']['txtTransport'].GetValue()})
            self.api.command(Execution(' / mpls / ldp / neighbor / %s' % cmd,
                dict([(k, v) for k, v in attrs.iteritems() if v])))
        self['EditWindow'].frame.Destroy()
