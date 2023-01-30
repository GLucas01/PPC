import os
import sys
import time
import signal
from multiprocessing import Process, Array, Value
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import random
import re
import socket
import threading
import select
import concurrent.futures

MAX_TEMPERATURE=35 #maximum temperature constant
PORT=9695 #market process host port number
market_amount=100000 #energy amount in market
serve = True #variable to stop the socket upon message from kill_market program
semaphore = threading.Semaphore(3) #maximum 3 clients transact with market simultaneously
#average_market_amount=100000

#------------------------------------------------------------------------
#function to handle the signal sent from factor process
def handler(sig, frame):
    global u1 #variable to store the absence/presence of a given external circumstance
    if sig == signal.SIGUSR1: #presence of external factor
        print("External factor: True ")
        u1=1
    if sig == signal.SIGUSR2: #absence of external factor
        print("External factor: False ")
        u1=0
    os.kill(exFactorProcess.pid, signal.SIGKILL) #kill the factor process

#------------------------------------------------------------------------
#factor process
def ex_factor():
    inp=random.randint(0, 1) #randomly generate value 0/1 and store into variable inp
    if inp==0 :
        os.kill(os.getppid(), signal.SIGUSR2) #send signal indicate absence of ex. factor
    if inp==1 :
        os.kill(os.getppid(), signal.SIGUSR1) #send signal indicate presence of ex. factor
    
#------------------------------------------------------------------------
#weather process
def weather(n,v):
    inp=random.uniform(0.1, n) #generate a random temperature between 0.1 and MAX_TEMPERATURE
    inp=("%.2f" % inp) #temperature to two decimal places
    print("Current temperature: "+str(inp)+" °c") #print out the current temperature
    v[0]=1/float(inp) #store the inverse of the current temperature in the shared memory array v[]

#------------------------------------------------------------------------
# ∑ α[i]*f[i,t]
def sum_a_f(a,f,i) :
    sum=0 #initialize sum to 0
    for x in range(i):
        sum+=a[x]*f[x]
    return sum
    
#------------------------------------------------------------------------
# ∑ β[j]*u[j,t]
def sum_B_u(B,u,j) :
    sum=0 #initialize sum to 0
    for x in range(j):
        sum+=B[x]*u[x]
    return sum

#------------------------------------------------------------------------
#function to handle the home process socket client
def handle_client(client_socket):
    global serve #make the variable known in other process/function
    global market_amount #make the variable known in other process/function
    request = client_socket.recv(1024) #receive the message sent by the client and store in the variable request
    m = request.decode() #decode the message from byte form to string form
    m = m.split("+") #split the message by the symbol +
    
    if str(m[0]) == "1": #client request to buy energy
        if market_amount<int(m[1]): #if market energy amount less than energy request
            message="Market not enough "+str(int(m[1]))+" for sale. Sorry"
            client_socket.send(message.encode()) #send the message back to the client
        else:
            print("Sold " + str(m[1]))
            market_amount=market_amount-int(m[1]) #update the energy amount in market
            message="OK+"
            message+=str(m[1]) #append the amount of energy client bought in the message
            client_socket.send(message.encode())#send the message back to the client
        client_socket.close() #close the client socket connection
        
        
    if str(m[0]) == "2": #client request to sell energy
        print("Bought " + str(m[1]))
        market_amount=market_amount+int(m[1]) #update the energy amount in market
        message="OK+"
        message+=str(m[1]) #append the amount of energy client sold in the message
        client_socket.send(message.encode())#send the message back to the client
        client_socket.close()#close the client socket connection
        
    if str(m[0]) == "4":
        print("Terminating server!")
        client_socket.close() #close the client socket connection
        serve=False
        
    if str(m[0]) == "5": #to call another socket connection to end the market server
        client_socket.close() #close the client socket connection
        serve=False
        call_stop() #call the function call_stop()
        sys.exit(0) #exit the program
    
    semaphore.release() #release the semaphore
#------------------------------------------------------------------------
#function to call another socket connection to end the market server
def call_stop():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(("localhost", PORT))
            client_socket.send(("4").encode()) #sending message "4" to the socket
            
#------------------------------------------------------------------------
#function to start the socket server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a TCP/IP socket
    server_socket.bind(("localhost", PORT)) #binds the socket to the localhost address on the specified port number
    server_socket.listen(5) #sets the maximum number of queued connections to 5
    print("[*] Listening on localhost:1600...")
    global serve
    
    while serve: #loop while the server is not shuting down
            semaphore.acquire() #acquires a lock on a semaphore
            print("Listening")
            client_socket, addr = server_socket.accept() #wait for the socket client connection and accept the connection
            print(f"[*] Accepted connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start() #call the handle_client function in a seperate thread
 
#------------------------------------------------------------------------
Pt_1=0.145 #initialize P(t-1)
if __name__ == "__main__": #to determine if a file is being run as the main program
    p = threading.Thread(target=start_server, args=()) #call the start_server function in a seperate thread
    p.start()
    while serve:
        produce=random.randint(100, 1000) #produce a random number of energy between 100 and 1000
        market_amount+=produce #update the energy produce in the market_amount variable
        print("market_amount : "+str(market_amount))
        
        ###################################################################
        #ex factor
        signal.signal(signal.SIGUSR1, handler) #market wait for the signal 1 to execute handler function
        signal.signal(signal.SIGUSR2, handler) #market wait for the signal 2 to execute handler function
        exFactorProcess = Process(target=ex_factor, args=()) #call the ex_factor function as the child process
        exFactorProcess.start()
        exFactorProcess.join()

        ###################################################################
        #weather
        shared_memory = Array('d', range(1)) #create a shared memory
        weatherProcess = Process(target=weather, args=(MAX_TEMPERATURE,shared_memory)) #call the weather function as the child process
        weatherProcess.start()
        weatherProcess.join()
          
        ###################################################################
        #date & time
        date_time_full=datetime.now().isoformat(timespec='seconds')
        date_time =date_time_full.split("T")
        
        ###################################################################
        #calculation
        #-internal factor
        a=[0.0001,100] #modulating coefficcient
        f=[shared_memory[0],(1/market_amount)] #inverse of temperature and energy amount
        #-external factor
        B=[0.01] #modulating coefficcient
        u=[u1] #presence of external factor
        #-long-term atteenuation coefficcient
        y=0.967
        
        
        Pt = (y*Pt_1)+sum_a_f(a,f,len(a))+sum_B_u(B,u,len(u))
        print("Price at "+str(date_time[0])+" "+str(date_time[1])+" : "+ str(Pt)+" €/kWh")
        Pt_1=Pt
        print("--------------------------------------")
        time.sleep(1.5)


