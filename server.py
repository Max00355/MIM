import thread
import socket
import time
import sys

users = {}

class MIM:
    def __init__(self):
        try:
            self.port = int(sys.argv[1])
        except IndexError:
            print "Usage: server.py <port>"
            exit()
        self.sock = socket.socket()
    
    def main(self):
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(5)
        while True:
            try:
                obj, con = self.sock.accept()
            except KeyboardInterrupt:
                for x in users:
                    x.close()
            users[obj] = con
            thread.start_new_thread(self.handle, (obj,))
    def check(self):
        while True:
            time.sleep(10)
            print str(len(users)), "users online."

    def handle(self, obj):
        while True:
            data = obj.recv(1024)
            if not data:
                del users[obj]
                break
           
            if ": /online" in data:
                obj.send(str(len(users))+" users online.")
            else:
                a = time.localtime()
                for x in users:
                    try:
                        x.send(str(a[3])+":"+str(a[4])+":"+str(a[5])+" "+data)
                    except:
                        x.close()
                        del users[x]
if __name__ == "__main__":
    mim = MIM()
    thread.start_new_thread(mim.check, ())
    MIM().main()

