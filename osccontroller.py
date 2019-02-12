import OSC
import time, threading
import ledfloor as lf
import threading


def create_osc_server(ip, port):
    receive_address = (ip, port)
    server = OSC.ThreadingOSCServer(receive_address)
    server.addDefaultHandlers() # 'default' handler for unmatched messages 
    server.addMsgHandler("/print", printing_handler) # useful for debugging
    return server


def start_osc_server(server):
    # Start OSCServer
    print "\nStarting OSCServer. Use ctrl-C to quit."
    st = threading.Thread( target = s.serve_forever )
    st.start()

    try :
        while True :
            time.sleep(5)

    except KeyboardInterrupt :
        print "\nClosing OSCServer."
        s.close()
        print "Waiting for Server-thread to finish"
        st.join()
        print "Done"
        


def print_handlers(server):
    """ Which handlers are registered with the server?
    """
    print "Registered Callback-functions are :"
    for addr in s.getOSCAddressSpace():
        print addr



# Some useful handler functions:

def printing_handler(addr, tags, data, source):
""" A useful handler for dbugging. Prints the OSC message
"""
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % data
    print "---"


    


    
 