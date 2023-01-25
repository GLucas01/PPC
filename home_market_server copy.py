import socket
import threading
import time
import select
import concurrent.futures

market_amount=100000

serve = True
ok=False
def handle_client(client_socket,add):
    global serve
    global ok
    global market_amount
    request = client_socket.recv(1024)
    print("Received: %s" % request)
    m = request.decode()[0]
    if m == "1":
        request = client_socket.recv(1024)
        m = str(request.decode())
        print(add+" bought "+m)
        market_amount=market_amount-int(m)
        print("Remainings : "+str(market_amount))
        #print(m)
        message="OK+"+str(m)
        client_socket.send(message.encode())
        ok=True
    if m == "2":
        request = client_socket.recv(1024)
        m = str(request.decode())
        print(add+" sold "+m)
        market_amount=market_amount+int(m)
        print("Remainings : "+str(market_amount))
        #print(m)
        message="OK+"+str(m)
        client_socket.send(message.encode())
        ok=True
    if m == "3":
        print("Terminating time server!")
        #client_socket.close()
        serve = False
        ok=True
    if m == "4":
        print("Terminating "+add)
        ok=True
        #client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 1600))
server_socket.listen(5)

while serve:
    client_socket, address = server_socket.accept()
    print("Connection from: %s" % str(address))
    client_handler = threading.Thread(target=handle_client, args=(client_socket,str(address)))
    client_handler.start()
    while not ok:
        pass
    ok=False
