import socket 
import sys
import threading

conn_list=[]
addr_list=[]
threads=[]

s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#function defining the utility of server
def utility():
    print("\n")
    print("     command                 :    functions \n")
    print("1)     show                  :  to show connections")
    print("2)    msg_all                :  broadcast message ") 
    print("3) reply connection no.      :  to select connection to reply")
    print("4) disconnect connection no. :  to disconnect any connection")
    print("5)     quit                  :  to quit the server          ")
   

def show_connections():
    for c in range(0,len(addr_list)):
        print str(c+1)+") " + "ip -" + str(addr_list[c][0]) + " port -" + str(addr_list[c][1])

def reply_connection(cmd):
    conn_no =int(cmd[6:])
    conn_no = conn_no - 1
    m=addr_list[conn_no]
    reply=raw_input('msg to '+ str(m[0])+': ' + str(m[1]) + '>')
    conn_list[conn_no].sendall(reply)

def dis_connections(cmd):
    conn_no = int(cmd[11:])
    conn_no = conn_no-1
    conn_list[conn_no].close()
    addr_list.pop(conn_no)
    conn_list.pop(conn_no)

def msg_all():
    msg= raw_input("msg to send to all : ")
    for b in range(0,len(addr_list)):
        conn_list[b].send(msg)

def quit_all():
    for b in range(0,len(addr_list)):
        conn_list[b].close()
    s.shutdown(2)
    s.close()
    sys.exit()

'''function to hendle replies from client'''     
def chat(conn,addr):
    while 1:
        a=conn.recv(1024)
        if len(a)<1:
            break
        print "msg from " + str(addr[0]) + ": " + str(addr[1]) +">" + a
        buff ="msg from " + str(addr[0]) + ": " + str(addr[1]) +">" + a
        for b in range(0,len(addr_list)) :
            if addr_list[b] != addr :
                conn_list[b].send(buff)
    for b in range(0,len(addr_list)):
        if addr_list[b] == addr :
            break
    conn.close()
    addr_list.pop(b)
    conn_list.pop(b)
    
#function to handle server activities
def response():
    while 1:
        cmd=raw_input()
        if 'show' in cmd:
            show_connections()
        elif 'reply' in cmd:
            reply_connection(cmd)
        elif 'disconnect' in cmd:
            dis_connections(cmd)
        elif 'quit' in cmd :
            quit_all()
        elif 'msg_all' in cmd:
            msg_all()
        else :
            utility()


host=''
port=9999
print "Binding socket"
try:
    s.bind((host,port))
except:
    print "error in binding socket"
    sys.exit()
print "listening for connections"
s.listen(10)
print "accepting connections"
utility()
t1=threading.Thread(target=response,args=())
t1.daemon= True
t1.start()
while True:
    conn,add=s.accept()
    conn_list.append(conn)
    addr_list.append(add)
    print "connected to "+str(add[0])+" at port: "+str(add[1])
    t = threading.Thread(target=chat, args=(conn,add,))
    threads.append(t)
    t.daemon= True
    t.start()

for thread in threads:
    thread.join()
t1.join(5)
s.close()
