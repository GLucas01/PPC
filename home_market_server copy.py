import socket
import threading
import time
import select
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import sys

market_amount=100000

serve = True

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
    server_socket.bind(("localhost", 2225))
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
            
start_server()


        #while serve:

