import os
import sys
import time
import signal
from multiprocessing import Process
import random
import time
from multiprocessing import Process, Array, Value
import re
from datetime import datetime
import socket
import threading
import select
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

PORT=9695
MAX_TEMPERATURE=35
market_amount=100000
serve = True

def handler(sig, frame):
    global u1
    if sig == signal.SIGUSR1:
        print("External factor: True ")
        u1=1
    if sig == signal.SIGUSR2:
        print("External factor: False ")
        u1=0
    os.kill(exFactorProcess.pid, signal.SIGKILL)
        
def weather(n,v):
    inp=random.uniform(0.1, n)
    inp=("%.2f" % inp)
    print("Current temperature: "+str(inp)+" °c")
    v[0]=1/float(inp)

def ex_factor():
    inp=random.randint(0, 1)
    if inp==1 :
        os.kill(os.getppid(), signal.SIGUSR2)
            
    if inp==0 :
        os.kill(os.getppid(), signal.SIGUSR1)
    

def sum_a_f(a,f,i) :
    sum=0
    for x in range(i+1):
        sum+=a[x]*f[x]
    return sum
    
    
def sum_B_u(B,u,i) :
    sum=0
    for x in range(i+1):
        sum+=B[x]*u[x]
    return sum



def handle_client(client_socket):
    global serve
    global market_amount
    request = client_socket.recv(1024)
    #print("Received: %s" % request)
    m = request.decode()
    m = m.split("+")
    
    if serve == False:
        message="KO+"
    else:
        message="OK+"
        
    if str(m[0]) == "1":
        if market_amount<int(m[1]):
            message+="N/A+Market not enough "+str(int(m[1]))+" for sale. Sorry"
            client_socket.send(message.encode())
        else:
            print("Sold " + str(m[1]))
            #print(add + " bought " + str(m[1]))
            market_amount=market_amount-int(m[1])
            print("Remainings : "+str(market_amount))
            #print(m)
            message+=str(m[1])
            client_socket.send(message.encode())
        
        
    if str(m[0]) == "2":
    
        print("Bought " + str(m[1]))
        market_amount=market_amount+int(m[1])
        print("Remainings : "+str(market_amount))
        #print(m)
        message+=str(m[1])
        client_socket.send(message.encode())
    if str(m[0]) == "3":
        print("Terminating client")
    #if str(m[0]) == "4":
     #   print("Terminating server!")
       # serve = False
        #client_socket.close()


def start_server():
    input_thread = threading.Thread(target=check_input)
    input_thread.start()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setblocking(False)
    server_socket.bind(("localhost", PORT))
    server_socket.listen(5)
    print("[*] Listening on localhost:1600...")
    global serve
    with ThreadPoolExecutor(max_workers=4) as executor:
        while serve:
            print("Listening")
            client_socket, addr = server_socket.accept()
            print(f"[*] Accepted connection from {addr}")
            executor.submit(handle_client, client_socket)
    input_thread.join()
    
    
def check_input():
    while True:
        user_input = input()
        if user_input == "quit":
            print("Terminating server!")
            
            #print("hello")
            global serve
            serve=False
            exit()
            #print(serve)
            break
            



Pt_1=0.145
if __name__ == "__main__":
    p = threading.Thread(target=start_server, args=())
    p.start()
    while True:
        
        print("market_amount : "+str(market_amount))
        #ex factor
        signal.signal(signal.SIGUSR1, handler) #market wait for the signal 1
        signal.signal(signal.SIGUSR2, handler) #market wait for the signal 2
        exFactorProcess = Process(target=ex_factor, args=())
        exFactorProcess.start()
        exFactorProcess.join()

        #weather
        shared_memory = Array('d', range(1))
        weatherProcess = Process(target=weather, args=(MAX_TEMPERATURE,shared_memory))
        weatherProcess.start()
        weatherProcess.join()
          
          
        #date & time
        date_time_full=datetime.now().isoformat(timespec='seconds')
        date_time =date_time_full.split("T")
        
        
        #calculation
        #-temperature
        a=[0.001] #modulating coefficcient
        f=[shared_memory[0]] #inverse of temperature
        #-external factor
        B=[0.01] #modulating coefficcient
        u=[u1] #presence of external factor
        #-long-term atteenuation coefficcient
        y=0.99
        
        Pt = (y*Pt_1)+sum_a_f(a,f,0)+sum_B_u(B,u,0)
        print("Price at "+str(date_time[0])+" "+str(date_time[1])+" : "+ str(Pt)+" €/kWh")
        Pt_1=Pt
        print("--------------------------------------")
        time.sleep(1.5)


