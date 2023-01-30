import os
import sys
import sysv_ipc
import threading
from multiprocessing import Process
import time
import socket
import random

key = 444 #message queue key
remainings=120000 #energy remaining
HOST = "localhost" #market process host address
PORT = 9695 #market process host port number
quit=False #variable to stop the energy production and consumption process
ok=True #variable to wait for a transaction to complete

#------------------------------------------------------------------------
#function for the user interface menu
def user():
    print("1. to hear request from neighbour")
    print("2. to request energy from neighbour")
    print("3. to buy energy")
    print("4. to sell energy")
    print("5. to terminate program")
    answer=6
    while answer not in [1, 2, 3, 4, 5]:
        answer = int(input())
        return answer

#------------------------------------------------------------------------
#home-home communication serve function
def worker(mq, m):
    message = str(m.decode()) #decode the message from byte form to string form
    message = message.split("+") #split the message by the symbol +
    amount=message[0] #store the amount of energy demanded in variable
    pid=int(message[1]) #process id of the client
    global remainings
    res="y"
    done= False
    while not done:
        print("PID "+str(pid)+" requested "+str(amount)+" energy, you have " +str(remainings)+" remainings.")
        res=input("Do you want to give away your energy [Y/y] or [N/n] ?")
        if (res=="N" or res=="n"): #home server does not agree to donate energy
            reply="Neighbour do not wish to giveaway their energy. Sorry :("
            done=True
        elif (res =="Y" or res =="y"): #home server agree to donate energy
            while True:
                try:
                    giveaway=int(input("How much do you want to give away : "))
                    if (giveaway > remainings): #if the amount to giveaway is superior than the remaings energy of home
                        print("Sorry. Not enough energy to giveaway. You can only giveaway energy less than "+str(remainings))
                    else:
                        print(str(giveaway)+" sent to PID "+str(pid))
                        remainings=remainings-giveaway #update the energy remainings
                        reply="OK"+"+"+str(giveaway)
                        done=True
                        break
                except ValueError:
                    print("Oops? That was not a valid integer")
                
    t = pid + 3
    mq.send(reply, type=t)
    global ok
    ok=True
#------------------------------------------------------------------------
def prod_cons():
    while True:
        global change
        global remainings
        produce=random.randint(100, 1000)
        consume=random.randint(100, 1000)
        change=produce-consume
        remainings+=change
        #print(change)
        time.sleep(2)
        if quit==True:
            sys.exit()


p = threading.Thread(target=prod_cons, args=())
p.start()
while True:
    
    #remainings+=change
    #print(remainings)
    if ok == True :
        print("You have "+str(remainings)+" remainings")
        ok=False
        t = user()
        if t == 1:
            if __name__ == "__main__":
                try:
                    #mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
                    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
                except sysv_ipc.ExistentialError:
                    print("Message queue", key, "already exsits, terminating.")
                    sys.exit(1)

                print("Starting server.")
                print("My key is "+str(key))
                    
                threads = []
                    
                    
                        
                m, index = mq.receive()
                if index == 1:
                    p = threading.Thread(target=worker, args=(mq, m))
                    p.start()
                    threads.append(p)
                            
                if index == 2:
                    mq.remove()
                    print("Test")
                    break
                    
                    
                    
        if t == 2:
            #print("You have "+str(remainings)+" remainings")
            key_neighbour = int(input("Enter key of the neighbour you wish to communicate : "))
            try:
                mq = sysv_ipc.MessageQueue(key_neighbour)
                while True:
                    try:
                        amount=int(input("How many energy to request : "))
                        break
                    except ValueError:
                        print("Oops? That was not a valid integer")
                pid = os.getpid()
                messages=str(amount)+"+"+str(pid)
                    
                mq.send(messages.encode())
                m, t = mq.receive(type =(pid + 3))
                dt = m.decode()
                response=dt.split("+")
                if response[0]=="OK":
                    print("Neighbour gave you "+str(response[1]))
                    remainings=remainings+int(response[1])
                    #print("Remainings : "+str(remainings))
                else:
                    print("Server response:", response[0])
            except sysv_ipc.ExistentialError:
                print("Cannot connect to message queue", key_neighbour, ", terminating.")
                #sys.exit(1)
            
            ok=True
                
        if t == 3:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                while True:
                    try:
                        buy_amount=int(input("How much do you want to buy : "))
                        break
                    except ValueError:
                        print("Oops? That was not a valid integer")
                client_socket.send(("1+"+str(buy_amount)).encode())
                resp = client_socket.recv(1024)
                #print(resp)
                if not len(resp):
                    print("The socket connection has been closed!")
                    sys.exit(1)
                response=resp.decode()
                response=response.split("+")
                if response[0]=="OK":
                    if response[1]=="N/A":
                        print("Server response:", response[2])
                    else:
                        print("You bought "+str(response[1])+" from market.")
                        remainings=remainings+int(response[1])
                        #print("Remainings : "+str(remainings))
                elif response[0]=="KO":
                    if response[1]=="N/A":
                        print("Server response:", response[2])
                    else:
                        print("You bought "+str(response[1])+" from market.")
                        remainings=remainings+int(response[1])
                        #print("Remainings : "+str(remainings))
                    #break
                ok=True
                    
        if t == 4:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                while True:
                    try:
                        sell_amount=int(input("How much do you want to sell : "))
                        if sell_amount>remainings:
                            print("Sorry. Not enough energy to sell. You can only sell energy less than "+str(remainings))
                        else:
                            break
                    except ValueError:
                        print("Oops? That was not a valid integer")
                client_socket.send(("2+"+str(sell_amount)).encode())
                resp = client_socket.recv(1024)
                
                if not len(resp):
                    print("The socket connection has been closed!")
                    sys.exit(1)
                response=resp.decode()
                response=response.split("+")
                if response[0]=="OK":
                    print("You sold "+str(response[1])+" to market.")
                    remainings=remainings-int(response[1])
                    #print("Remainings : "+str(remainings))
                                
                elif response[0]=="KO":
                    print("You sold "+str(response[1])+" to market.")
                    remainings=remainings-int(response[1])
                    #print("Remainings : "+str(remainings))
                    #break
                ok=True
            
        if t == 5:
            quit=True
            #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
             #   client_socket.connect((HOST, PORT))
              #  client_socket.send(("3").encode())
            break
    else:
        pass
print("Terminating program")
p.join()
if t==1:
    mq.remove()
