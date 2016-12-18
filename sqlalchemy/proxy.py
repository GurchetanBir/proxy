import socket
import select
import time
import sys
import redis
from cb import circuitbreak


cb1 = circuitbreak()
cb2 = circuitbreak()
cb3 = circuitbreak()
cb1.set_close_state()
cb2.set_close_state()
cb3.set_close_state()

array = [1,2,3]
redarray=[]
servernotrunning= []
redarray.append(1)
def getPort():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    value = int(r.get(redarray[0]))
    if redarray[0] == 1:
        del redarray[0]
        redarray.append(2)
    elif redarray[0]==2:
        del redarray[0]
        redarray.append(3)
    elif redarray[0] == 3:
        del redarray[0]
        redarray.append(1)
    newvalue = isWorking(value)

    return newvalue


def getPosition(port):
    length  = len(servernotrunning)
    if (length == 1):
        return 0
    elif length ==2:
        if(servernotrunning[0]==port):
            return 0
        elif(servernotrunning[1]==port):
            return 1
    elif length == 3:
        if (servernotrunning[0] == port):
            return 0
        elif (servernotrunning[1] == port):
            return 1
        elif (servernotrunning[2] == port):
            return 2


def isWorking(port):
    if (port in servernotrunning):
        if (port == 5001):
            cb1.check_state()
            if (cb1.getState() == 2):
                position = getPosition(5001)

                del servernotrunning[position]
                newport = port

            else:
                newport = getPort()

        if(port == 5002):

            cb2.check_state()
            if (cb2.getState() == 2):
                position = getPosition(5002)
                del servernotrunning[position]
                newport=port

            else:
                newport = getPort()


        if(port == 5003):
            cb3.check_state()
            if (cb3.getState() == 2):
                position = getPosition(5003)
                del servernotrunning[position]
                newport = port

            else:
                newport = getPort()


    else:
        newport = port
    return newport






buffer_size = 4096
delay = 0.0001
host = '127.0.0.1'
forward_to = (host,getPort())


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    print "First Connection"
                    self.on_accept()
                    break
                print "Dooja Connection"
                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):

        a=getPort()

        forward = Forward().start('', a)
        clientsock, clientaddr = self.server.accept()
        if forward:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock

        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr

            if(a == 5001):
                cb1.handle_failure()
                state1 = cb1.getState()
                if (state1 == 0):
                    servernotrunning.append(a)

            elif(a == 5002):
                cb2.handle_failure()
                state2 = cb2.getState()
                if (state2 == 0):
                    servernotrunning.append(a)

            elif(a==5003):
                cb3.handle_failure()
                state3 = cb3.getState()
                if (state3 == 0):
                    servernotrunning.append(a)




            clientsock.close()

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        print data
        self.channel[self.s].send(data)

if __name__ == '__main__':
        server = TheServer('', 9091)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            sys.exit(1)