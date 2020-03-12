import sys
sys.path.insert(0, "..")


from opcua import Client

import time

from time import sleep
from pyo import *

import tkinter as tk

import threading

rootTk = tk.Tk()
canvas = tk.Canvas(rootTk, width=400, height=400, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

fileName = 'alerts.log'

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

def sound_alerta():
    server = Server().boot()
    server.start()
    sine = Sine(523.3, mul=0.1).out()
    sleep(0.5)
    server.stop()
    
def modifico_circulo():
    global valor, canvas, root
    while True:
#        time.sleep(1)
        value1 = root.get_children()[0].get_children()[1].get_variables()[0].get_value()
        value2 = root.get_children()[0].get_children()[1].get_variables()[1].get_value()
        value3 = root.get_children()[0].get_children()[1].get_variables()[2].get_value()
        if valor1.get() == 0:
            canvas.create_circle(100, 40, 20, fill="green", outline="")
        
        if valor2.get() == 0:
            canvas.create_circle(200, 40, 20, fill="green", outline="")
            
        if valor3.get() == 0:
            canvas.create_circle(300, 40, 20, fill="green", outline="")
            
        if (value1 == 'Hay un problema'):
            valor1.set(1)
            canvas.create_circle(100, 40, 20, fill="red", outline="")
            sound_alerta()
          
        if (value2 == 'Hay un problema'):
            valor2.set(1)
            canvas.create_circle(200, 40, 20, fill="red", outline="")
            sound_alerta()
            
        if (value3 == 'Hay un problema'):
            valor3.set(1)
            canvas.create_circle(300, 40, 20, fill="red", outline="")
            sound_alerta()
            


if __name__ == "__main__":

    client = Client("opc.tcp://192.168.0.53:4840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
#        myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
#        obj = root.get_child(["0:Objects", "2:MyObject"])
#        print("myvar is: ", myvar)
#        print("myobj is: ", obj)

        # Stacked myvar access
        print(root.get_children()[0])
        
        print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())
#        root.get_children()[0].get_children()[1].get_variables()[0].set_value('Todo ok')
        
        valor1 = tk.IntVar()
        valor2 = tk.IntVar()
        valor3 = tk.IntVar()
        def callback_but1(*args):
            global valor1
            if valor1.get() == 1:
                valor1.set(0)
                root.get_children()[0].get_children()[1].get_variables()[0].set_value('Todo ok')
                with open(fileName, 'a') as fileO:
                    fileO.write('Alarma apagada en variable 1 a las ' + time.asctime(time.localtime()) + '\n')
        def callback_but2(*args):
            global valor2
            if valor2.get() == 1:
                valor2.set(0)
                root.get_children()[0].get_children()[1].get_variables()[1].set_value('Todo ok')
                with open(fileName, 'a') as fileO:
                    fileO.write('Alarma apagada en variable 2 a las ' + time.asctime(time.localtime()) + '\n')
        def callback_but3(*args):
            global valor3
            if valor3.get() == 1:
                valor3.set(0)
                root.get_children()[0].get_children()[1].get_variables()[2].set_value('Todo ok')
                with open(fileName, 'a') as fileO:
                    fileO.write('Alarma apagada en variable 3 a las ' + time.asctime(time.localtime()) + '\n')
        but1 = tk.Button(canvas, text = 'Apagar alarma', command = callback_but1)
        but1.place(x=50,y=100)
        but2 = tk.Button(canvas, text = 'Apagar alarma', command = callback_but2)
        but2.place(x=150,y=100)
        but3 = tk.Button(canvas, text = 'Apagar alarma', command = callback_but3)
        but3.place(x=250,y=100)
        thread = threading.Thread(target=modifico_circulo)
        thread.setDaemon(True)
        thread.start()
#        but.configure(width = 10, activebackground = "#33B5E5")
        rootTk.mainloop()

    finally:
        client.disconnect()
