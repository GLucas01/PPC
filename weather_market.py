import sys
from multiprocessing import Process, Array, Value
import re


def update_function(n,v):
    #n.value = 3.1415927
    v[0] = 1/v[0]
 
    
if __name__ == "__main__":
    while True:
        shared_memory = Array('d', range(1))
        
        try:
            x = int(input("Please enter current temperature: "))
            shared_memory[0]=x
            print("Temperature :"+ str(shared_memory[0]))
            weather = Process(target=update_function, args=(x,shared_memory))
            weather.start()
            weather.join()
         
            print("Inverted temperature :"+ str(shared_memory[0]))
           
            
        except ValueError as e:
            error=re.findall("invalid literal for int\(\) with base 10\: \'([^\']+)", str(e))
            if error[0]=="stop":
                break
            print("Oops!  That was not a valid temperature.  Try again...")
            
            




