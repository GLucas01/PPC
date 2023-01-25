import socket
import threading
import time
import select
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

market_amount=100000

serve = True
ok=False

def handle_client(client_socket):
    global serve
    global ok
    global market_amount
    request = client_socket.recv(1024)
    #print("Received: %s" % request)
    m = request.decode()
    m = m.split("+")
    if str(m[0]) == "1":
        print("Sold " + str(m[1]))
        #print(add + " bought " + str(m[1]))
        market_amount=market_amount-int(m[1])
        print("Remainings : "+str(market_amount))
        #print(m)
        message="OK+"+str(m[1])
        client_socket.send(message.encode())
        ok=True
    if str(m[0]) == "2":
        print("Bought " + str(m[1]))
        market_amount=market_amount+int(m[1])
        print("Remainings : "+str(market_amount))
        #print(m)
        message="OK+"+str(m[1])
        client_socket.send(message.encode())
        ok=True
    if str(m[0]) == "3":
        print("Terminating server!")
        serve = False
        ok=True
    if str(m[0]) == "4":
        print("Terminating client")
        ok=True
        #client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setblocking(False)
    server_socket.bind(("localhost", 1604))
    server_socket.listen(5)
    print("[*] Listening on localhost:1600...")
    
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[*] Accepted connection from {addr}")
            executor.submit(handle_client, client_socket)


start_server()


        #while serve:
            
         #   while not ok:
          #      pass
           # ok=False
