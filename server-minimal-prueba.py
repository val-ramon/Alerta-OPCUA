import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server
import numpy as np


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar1 = myobj.add_variable(idx, "MyVariable1", 6.7)
    myvar1.set_writable()    # Set MyVariable to be writable by clients
    myvar2 = myobj.add_variable(idx, "MyVariable2", 6.7)
    myvar2.set_writable()    # Set MyVariable to be writable by clients
    myvar3 = myobj.add_variable(idx, "MyVariable3", 6.7)
    myvar3.set_writable()    # Set MyVariable to be writable by clients
    # starting!
    server.start()
    
    try:
        count = 0
        myvar1.set_value('Todo ok')
        myvar2.set_value('Todo ok')
        myvar3.set_value('Todo ok')
        while True:
            time.sleep(5)
            count += 0.1
#            myvar.set_value(count)
            value1 = np.random.randint(1, 20)
            value2 = np.random.randint(1, 20)
            value3 = np.random.randint(1, 20)
            if value1 == 1:
                myvar1.set_value('Hay un problema')
            if value2 == 2:
                myvar2.set_value('Hay un problema')
            if value3 == 3:
                myvar3.set_value('Hay un problema')
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
