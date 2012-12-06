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
