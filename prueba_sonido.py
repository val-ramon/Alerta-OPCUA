# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 09:59:35 2020

@author: edomene
"""

from time import sleep
from pyo import *
server = Server().boot()
server.start()
sine = Sine(261.63, mul=0.1).out()
sleep(3)
server.stop()