import sys
import time
import sysv_ipc
import threading

key = 662
remainings=1234

def worker(mq, m):
    
    message = str(m.decode())
    message = message.split("+")
    amount=message[0]
    pid=int(message[1])
    global remainings
    res="y"
    done= False
    while not done:
        print("PID "+str(pid)+" requested "+str(amount)+" energy, you have " +str(remainings)+" remainings.")
        res=input("Do you want to give away your energy [Y/y] or [N/n] ?")
        if (res=="N" or res=="n"):
            reply="Neighbour do not wish to giveaway their energy. Sorry :("
            #break
            done=True
        elif (res =="Y" or res =="y"):
            while True:
                try:
                    giveaway=int(input("How much do you want to give away : "))
                    if (giveaway > remainings):
                        print("Sorry. Not enough energy to giveaway. You can only giveaway energy less than "+str(remainings))
                    else:
                        print(str(giveaway)+" sent to PID "+str(pid))
                        remainings=remainings-giveaway
                        print("Remainings : "+str(remainings))
                        reply="OK"+"+"+str(giveaway)
                        done=True
                        break
                except ValueError:
                    print("Oops? That was not a valid integer")
                
    t = pid + 3
    mq.send(reply, type=t)


if __name__ == "__main__":
    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    print("Starting server.")


    threads = []
    while True:
        m, t = mq.receive()
        if t == 1:
            p = threading.Thread(target=worker, args=(mq, m))
            p.start()
            threads.append(p)
            
        if t == 2:
            for thread in threads:
                thread.join()
            mq.remove()
            break
    
    print("Terminating server.")
