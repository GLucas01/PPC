import os
import sys
import time
import sysv_ipc

key = 123
remainings=1000

def user():
    answer = 4
    while answer not in [1, 2, 3]:
        answer = int(input())
    return answer


key = int(input("Enter key of the neighbour you wish to communicate : "))

try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)

print("1. to request energy from neighbour")
print("2. to terminate time server")
print("3. to terminate time client")
while True:
    t = user()
    
    if t == 1:
        print("You have "+str(remainings)+" remainings")
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
            print("Remainings : "+str(remainings))
        else:
            print("Server response:", response[0])
            
    if t == 2:
        m = b""
        mq.send(m, type = 2)

    if t == 3:
        break
        
    print("Terminating time client.")
