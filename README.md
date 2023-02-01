This project will let us understand how the different inter-process communication and synchronization tools can be used to let multiple processes communicate each other.
The program is designed to let the user interact between different "home" processes and the "market" process.
We assume that a single program simulation is not very interesting as we can't see the process how the processes communicate between them.

--TO START THIS PROGRAM--
1. Make sure your machine installed python3
2. Download all the source code and put in a same directory
3. Open a terminal/Powershell 
4. Make sure you are in the directory where you downloaded the source code
5. Execute first the market process
```
python3 Market.py
```

. Open your terminal/PowerShell and type "python3 program.py" to execute it. In our project, run the market program first before starting any home program. This will ensure an automated socket connection for communication once the home program starts. If the market program is not running, the home program will not be able to find the socket with the defined port number. Next, we can run multiple home programs, but only a maximum of three can transact with the market program simultaneously. There is no limit on communication between the home programs. In addition to the four main functionalities introduced in the home process menu (Donating energy, Requesting energy, Purchasing energy, Selling energy), we added a fifth option to shut down the home program properly. Lastly, to properly shut down the market process, we created a third program named "kill_market" that sends a command via the socket to terminate the market program.

