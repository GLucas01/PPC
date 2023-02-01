This project will let us understand how the different inter-process communication and synchronization tools can be used to let multiple processes communicate each other.
The program is designed to let the user interact between different "home" processes and the "market" process.
We assume that a single program simulation is not very interesting as we can't see the process how the processes communicate between them.

--TO START THIS PROGRAM--
1. Make sure your machine installed python3
2. Download all the source code and put in a same directory
3. Open a terminal/Powershell 
4. Make sure you are in the directory where you downloaded the source code
5. Execute first the market process (ensure an automated socket connection for communication with home)
```
python3 Market.py
```
6. Execute all the home processes
```
python3 Home.py
python3 Home2.py
python3 Home3.py
python3 Home4.py
```

--PLAY WITH THE PROGRAM--
1. Now you should have 5 windows opened
2. You will have 5 choices for each home process
```
1. to hear request from neighbour
2. to request energy from neighbour
3. to buy energy
4. to sell energy
5. to terminate program
```
 + **to hear request from neighbour** : Become a message queue server and waiting connection from other home process to giveaway the energy.     
 + **to request energy from neighbour** : Connect to a message queue server using a key and asking for an amount of energy.      
 + **to buy energy** : Home user can connect to the market process using socket to buy an amount of energy.      
 + **to sell energy** : Home user can connect to the market process using socket to sell an amount of energy.      
 + **to terminate program** : Home user ends the program.      
  
We can run multiple home programs, but only a maximum of three can transact with the market program simultaneously. There is no limit on communication between the home programs.

--END THE PROGRAM--
1. Execute the kill_market program
```
python3 kill_market.py
```
The program sends a command via the socket to terminate the market program.

