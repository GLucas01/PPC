import os
import sys
import time
import signal
from multiprocessing import Process
from datetime import datetime


def handler(sig, frame):
    if sig == signal.SIGUSR1:
        print("External factor: True " +str(datetime.now()))
        os.kill(ex_factor1_Process.pid, signal.SIGKILL)
    if sig == signal.SIGUSR2:
        print("External factor: False " +str(datetime.now()))
        os.kill(ex_factor2_Process.pid, signal.SIGKILL)
        
def ex_factor1():
    #time.sleep(5)
    os.kill(os.getppid(), signal.SIGUSR1)
    #print("child 1 sent: " +str(datetime.now()))

def ex_factor2():
    #time.sleep(5)
    os.kill(os.getppid(), signal.SIGUSR2)
    #print("child 2 sent: " +str(datetime.now()))
    
    
if __name__ == "__main__":
    while True:
        signal.signal(signal.SIGUSR1, handler) #market wait for the signal 1
        signal.signal(signal.SIGUSR2, handler) #market wait for the signal 2
        inp = input("Type \"1\" if there is external factor, \"0\" if there isn't : ")
        if inp=="1" :
            ex_factor1_Process = Process(target=ex_factor1, args=())
            ex_factor1_Process.start()
            ex_factor1_Process.join()
            
        if inp=="0" :
            ex_factor2_Process = Process(target=ex_factor2, args=())
            ex_factor2_Process.start()
            ex_factor2_Process.join()

        if inp=="stop":
            break




