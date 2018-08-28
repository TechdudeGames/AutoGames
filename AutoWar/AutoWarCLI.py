from blessings import Terminal
from pynput.keyboard import Key, Controller #Lib to help clear screen garbage
from pynput import keyboard
term = Terminal()
import os
import sys
import time
import WarBackend as War
import multiprocessing
os.system("clear")
starttime=time.time()
#Some terminal option configuations
#Todo add some terminal configuring options
avcores = multiprocessing.cpu_count() - 1
number_of_total_games= 33000 # 33 million
print("Playing %i games." %(number_of_total_games//avcores * avcores))

rtstatlist = []
for loops in range(0, avcores):
    stat = multiprocessing.Array('i', range(4)) #creating a statistic list for a thread to utalize
    for kount in range(0,4):
        stat[kount] = 0
    rtstatlist.append(stat)


#Playing functions
def warthread(numgames,threadnum,statlist):
    print("Thread %i online" %threadnum)
    for i in range (0,numgames):
        result=War.playwar()
        if result==1:
            statlist[threadnum][0] += 1
        elif result==2:
            statlist[threadnum][1] += 1
        elif result==3:
            statlist[threadnum][2] += 1
        statlist[threadnum][3] += 1

def totalup(statlist,dataindex,numbcores):
    """
    :param statlist: The collective thread statistics lists
    :param dataindex: The data from each list to add up
    0-Player one wins
    1-Player two wins
    2-Draws
    3-Total games played
    :param numbcores: The number of threads (Used for a for statement to correctly add up the data)
    :return: The total value of each threads statistics combines
    """
    returnresult = 0
    internalcount = numbcores
    for dive in range(0,numbcores):
        returnresult += statlist[dive][dataindex] #Dive is used as an index into the realtime list of lists.
    return returnresult

def clearscreen(key):
    """
    :param key
    Clear the screen of any entered garbage
    :return: Nothing really
    """
    if key == Key.esc:
        os.system("clear")
    time.sleep(1)


#Creating the thread list and spawning the threads
threads = []
if avcores == 1:
    wthread=multiprocessing.Process(target=warthread, args=(number_of_total_games//avcores,0,rtstatlist))
    threads.append(wthread)
else:
    for count in range(0, avcores):
        wthread=multiprocessing.Process(target=warthread, args=(number_of_total_games//avcores,count,rtstatlist))
        threads.append(wthread)
        threads[count].start()


#Main Event
last_run = False
with keyboard.Listener(on_press=clearscreen) as listener:
	while totalup(rtstatlist, 3, avcores) != number_of_total_games // avcores * avcores:
		statlist = [totalup(rtstatlist, 0, avcores), totalup(rtstatlist, 1, avcores), totalup(rtstatlist, 2, avcores),
		            totalup(rtstatlist, 3, avcores)]
		# Prevents a bug from occuring if a thread modified the rtstatlist before the print code finshed processing the first totalup
		if totalup(rtstatlist, 3,
		           avcores) != 0:  # Prevents divide by zero error if the display code was run before any of the threads had a chance to play a game
			with term.location(0, 10):
				print("Player One has won %f percent of the time       " % float(statlist[0] * 100 / statlist[3]))
				print("Player Two has won %f percent of the time       " % float(statlist[1] * 100 / statlist[3]))
				print("There has been a draw %f percent of the time     \n" % float(statlist[2] / statlist[3]))
				print("Player One has won %i times" % statlist[0])
				print("Player Two has won %i times" % statlist[1])
				print("There have been %i draws" % statlist[2])
				print("The game has been played %i times" % statlist[3])
				elapsted_seconds = time.time() - starttime
				# elapsted_seconds = 602263 #Debug time amount. Should be 6 days, 23 hours, 17 minutes, and 43 seconds
				days = int(elapsted_seconds // 86400)
				hours = int(elapsted_seconds // 3600 - (days * 24))
				minutes = int(elapsted_seconds // 60 - (hours * 60) - (days * 1440))
				seconds = int(elapsted_seconds - (minutes * 60) - (hours * 3600) - (days * 86400))
				print("Time Elapsed: ", days, ":", hours, ":", minutes, ":", seconds)
	os.system("clear")

with term.location(0, 10):
    print("Player One has won %f percent of the time       " % float(statlist[0] * 100 / statlist[3]))
    print("Player Two has won %f percent of the time       " % float(statlist[1] * 100 / statlist[3]))
    print("There has been a draw %f percent of the time     \n" % float(statlist[2] / statlist[3]))
    print("Player One has won %i times" % statlist[0])
    print("Player Two has won %i times" % statlist[1])
    print("There have been %i draws" % statlist[2])
    print("The game has been played %i times" % statlist[3])
    elapsted_seconds = time.time() - starttime
    # elapsted_seconds = 602263 #Debug time amount. Should be 6 days, 23 hours, 17 minutes, and 43 seconds
    days = int(elapsted_seconds // 86400)
    hours = int(elapsted_seconds // 3600 - (days * 24))
    minutes = int(elapsted_seconds // 60 - (hours * 60) - (days * 1440))
    seconds = int(elapsted_seconds - (minutes * 60) - (hours * 3600) - (days * 86400))
    print("Time Elapsed: ", days, ":", hours, ":", minutes, ":", seconds)


