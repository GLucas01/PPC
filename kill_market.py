import socket

HOST = "localhost" #market process host address
PORT = 9695 #market process host port number

def kill_market(): #function to execute the killing of market
    print("1. to terminate market")
    print("2. to terminate program")
    answer=3
    while answer not in [1,2]: #if the answer given is not in the selection, program will always ask user the same question
        answer = int(input())
        return answer

while True:
    t = kill_market() #t stores the choices of user
            
    if t == 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT)) #connects to market process using socket
            client_socket.send(("5").encode()) #sends message "5" to the market
            break #break the while loop
            
    if t == 2: #quit this own program
        break #break the while loop
        
print("Terminating program") 


