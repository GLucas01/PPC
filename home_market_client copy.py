import sys
import socket

def user():
    answer = 5
    while answer not in [1, 2, 3, 4]:
        answer = int(input())
    return answer

HOST = "localhost"
PORT = 1600
remainings=12000
print("1. to buy energy")
print("2. to sell energy")
#print("3. to terminate server")
#print("4. to terminate client")

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        m = user()
        if m == 1:
            client_socket.send(b"1")
            while True:
                try:
                    buy_amount=int(input("How much do you want to buy : "))
                    break
                except ValueError:
                    print("Oops? That was not a valid integer")
            
            client_socket.send(str(buy_amount).encode())
            resp = client_socket.recv(1024)
            #print(resp)
            if not len(resp):
                print("The socket connection has been closed!")
                sys.exit(1)
            response=resp.decode()
            response=response.split("+")
            if response[0]=="OK":
                print("You bought "+str(response[1])+" from market.")
                remainings=remainings+int(response[1])
                print("Remainings : "+str(remainings))
            else:
                print("Server response:", response[0])
                
        if m == 2:
            client_socket.send(b"2")
            while True:
                try:
                    sell_amount=int(input("How much do you want to sell : "))
                    break
                except ValueError:
                    print("Oops? That was not a valid integer")
            
            client_socket.send(str(sell_amount).encode())
            resp = client_socket.recv(1024)
            
            if not len(resp):
                print("The socket connection has been closed!")
                sys.exit(1)
            response=resp.decode()
            response=response.split("+")
            if response[0]=="OK":
                print("You sold "+str(response[1])+" to market.")
                remainings=remainings-int(response[1])
                print("Remainings : "+str(remainings))
            else:
                print("Server response:", response[0])
        if m == 3:
            print("Terminate server")
            client_socket.send(b"3")
            break
        if m == 4:
            print("Terminate program")
            client_socket.send(b"4")
            break
            
    
