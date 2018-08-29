from blessings import Terminal
from pynput.keyboard import Key  # Lib to help clear screen garbage
from pynput import keyboard
import WarBackend as War
import multiprocessing
import os
import sys
import time

term = Terminal()
global needscreenclear
needscreenclear = False
os.system("clear")
starttime = time.time()  # Statement to allow time to be kept on the amount of time the program has been running.
# Todo add some terminal configuring options
options = {
	"avthreads": 0,
	"numberofgames": 100000,
	"createouput": False,
	"outputfilename": ""
}
passed_arguments = sys.argv

options["avthreads"] = multiprocessing.cpu_count() - 1
print("Playing %i games." % (options["numberofgames"]))

rtstatlist = []
for loops in range(0, options["avthreads"]):
	stat = multiprocessing.Array('i', range(4))  # creating a statistic list for a thread to utalize
	for kount in range(0, 4):
		stat[kount] = 0
	rtstatlist.append(stat)


# Playing functions
def warthread(numgames, threadnum, statlist):
	print("Thread %i online" % threadnum)
	for i in range(0, numgames):
		result = War.playwar()
		if result == 1:
			statlist[threadnum][0] += 1
		elif result == 2:
			statlist[threadnum][1] += 1
		elif result == 3:
			statlist[threadnum][2] += 1
		statlist[threadnum][3] += 1


def totalup(statlist):
	'''
	:param statlist: The current real time statistic list
	:return: A list of totaled data from this rt list
	'''
	numberoflists = statlist.__len__()
	outputstlist = []
	for i in range(0, 4):
		outputstlist.append(0)  # Putting in values that way we can add to them
	for dive in statlist:
		for subdive in range(0, 4):
			outputstlist[subdive] += dive[subdive]
	return outputstlist


def clearscreen(key):
	"""
	:param key
	Clear the screen of any entered garbage
	:return: Nothing really
	"""
	global needscreenclear
	if key == Key.esc:
		needscreenclear = True


# Creating the thread list and spawning the threads
threads = []
if options["avthreads"] == 1:
	wthread = multiprocessing.Process(target=warthread, args=(options["numberofgames"], 0, rtstatlist))
	threads.append(wthread)
else:
	tmpgames_playing = options["numberofgames"]
	for count in range(0, options["avthreads"] - 1):
		wthread = multiprocessing.Process(target=warthread,args=(options["numberofgames"] // options["avthreads"], count, rtstatlist))
		tmpgames_playing -= options["numberofgames"] // options["avthreads"]
		threads.append(wthread)
		threads[count].start()
	wthread = multiprocessing.Process(target=warthread, args=((tmpgames_playing, count + 1,rtstatlist)))
	threads.append(wthread)
	threads[count + 1].start()

# Main Event
last_run = False
if options["numberofgames"] > 0:
	with keyboard.Listener(on_press=clearscreen) as listener:
		while (totalup(rtstatlist))[3] != options["numberofgames"]:
			statlist = totalup(rtstatlist)
			# Minimizes a bug from occuring if a thread modified the rtstatlist before the print code finshed processing the first totalup
			if statlist[0] > 0:  # Prevents divide by zero error if the display code was run before any of the threads had a chance to play a game
				if needscreenclear:
					os.system("clear")
					needscreenclear = False
				with term.location(0, 5):
					print("Press Esc to clear the screen (Just in case you accidentally typed garbage)")
					print("Player One has won %f percent of the time.	   " % (statlist[0] * 100 / statlist[3]))
					print("Player Two has won %f percent of the time.	   " % (statlist[1] * 100 / statlist[3]))
					print("There has been a draw %f percent of the time.	 \n" % (statlist[2] / statlist[3]))
					print("Player One has won %i time(s)." % statlist[0])
					print("Player Two has won %i time(s)." % statlist[1])
					print("There have been %i draws" % statlist[2])
					print("The game has been played %i time(s)." % statlist[3])
					print("We are %f percent done." % (statlist[3] * 100 / options["numberofgames"]))
					elapsted_seconds = time.time() - starttime
					# elapsted_seconds = 602263 #Debug time amount. Should be 6 days, 23 hours, 17 minutes, and 43 seconds
					days = int(elapsted_seconds // 86400)
					hours = int(elapsted_seconds // 3600 - (days * 24))
					minutes = int(elapsted_seconds // 60 - (hours * 60) - (days * 1440))
					seconds = int(elapsted_seconds - (minutes * 60) - (hours * 3600) - (days * 86400))
					print("Time Elapsed: ", days, "  ", ":", hours, "  ", ":", minutes, "  ", ":", seconds, "  ")
					adverage_games_per_second = statlist[3] / elapsted_seconds
					tremaining = (options["numberofgames"] - statlist[3]) / adverage_games_per_second
					advdays = int(tremaining // 86400)
					advhours = int(tremaining // 3600 - (advdays * 24))
					advminutes = int(tremaining // 60 - (advhours * 60) - (advdays * 1440))
					advseconds = int(tremaining - (advminutes * 60) - (advhours * 3600) - (advdays * 86400))
					print("Time Remaining: ", advdays, "  ", ":", advhours, "  ", ":", advminutes, "  ", ":",
					      advseconds, "  ")
		
		os.system("clear")
		statlist = totalup(rtstatlist)
		with term.location(0, 10):
			print("Player One has won %f percent of the time.	   " % float(statlist[0] * 100 / statlist[3]))
			print("Player Two has won %f percent of the time.	   " % float(statlist[1] * 100 / statlist[3]))
			print("There has been a draw %f percent of the time.	 \n" % float(statlist[2] / statlist[3]))
			print("Player One has won %i times." % statlist[0])
			print("Player Two has won %i times." % statlist[1])
			print("There have been %i draws" % statlist[2])
			print("The game has been played %i time(s)" % statlist[3])
			elapsted_seconds = time.time() - starttime
			# elapsted_seconds = 602263 #Debug time amount. Should be 6 days, 23 hours, 17 minutes, and 43 seconds
			days = int(elapsted_seconds // 86400)
			hours = int(elapsted_seconds // 3600 - (days * 24))
			minutes = int(elapsted_seconds // 60 - (hours * 60) - (days * 1440))
			seconds = int(elapsted_seconds - (minutes * 60) - (hours * 3600) - (days * 86400))
			print("Time Elapsed: ", days, "  ", ":", hours, "  ", ":", minutes, "  ", ":", seconds, "  ")


