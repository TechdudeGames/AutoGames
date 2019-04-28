import multiprocessing
import os
import signal
import sys
import time

import WarBackend as War
from blessings import Terminal


def cleanexit(sig, frame):
	if os.system("clear") != 0:
		os.system("cls")
	print("\nStopping...")
	sys.exit()


signal.signal(signal.SIGINT, cleanexit)  # Catches ^c and stops





term = Terminal()
global needscreenclear
needscreenclear = False
os.system("clear")
starttime = time.time()  # Statement to allow time to be kept on the amount of time the program has been running.
# Todo add some terminal configuring options
options = {
	"avthreads": 0,
	"numberofgames": 5,
	"createouput": False,
	"outputfilename": ""
}
passed_arguments = sys.argv[1:]
continuetorun = True
if '-h' in passed_arguments:
	print(''
		  '-h | prints this help thing :)\n'
		  '-t | Number of threads\n'
		  '-g | Number of games to play')
	continuetorun = False
else:
	if '-c' in passed_arguments:
		threadarg = passed_arguments.index('-c')
		try:
			threadarg_perm = passed_arguments[threadarg + 1]
			options["avthreads"] = float(threadarg_perm)
		except IndexError or ValueError:
			print('Invalid perameter')
			continuetorun = False
	else:
		options["avthreads"] = multiprocessing.cpu_count() - 1
	if '-g' in passed_arguments:
		gamesarg = passed_arguments.index('-g')
		try:
			gamesarg_perm = passed_arguments[gamesarg + 1]
			options["numberofgames"] = int(gamesarg_perm)
		except IndexError or ValueError:
			print('Invalid perameter')
			continuetorun = False
	else:
		options["numberofgames"] = 1000000









# Playing functions
def warthread(numgames, threadnum, statlist):

	if os.path.isfile(os.path.join(".",str(threadnum)+"-drawreport.csv")):
		os.remove(os.path.join(".",str(threadnum)+"-drawreport.csv"))
		tmpfile = open(os.path.join(".",str(threadnum)+"-drawreport.csv"),'w')
		tmpfile.close()
	else:
		tmpfile = open(os.path.join(".", str(threadnum) + "-drawreport.csv"), 'w')
		tmpfile.close()


	for i in range(0, numgames):
		result = War.playwar(fileoutput=os.path.join(".",str(threadnum)+"-drawreport.csv"))
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
	outputstlist = []
	for i in range(0, 4):
		outputstlist.append(0)  # Putting in values that way we can add to them
	for dive in statlist:
		for subdive in range(0, 4):
			outputstlist[subdive] += dive[subdive]
	return outputstlist




# Main Event
last_run = False
if (options["numberofgames"] > 0) and(continuetorun):

	print("Playing %i games." % (options["numberofgames"]))

	rtstatlist = []
	for loops in range(0, options["avthreads"]):
		stat = multiprocessing.Array('i', range(4))  # creating a statistic list for a thread to utalize
		for kount in range(0, 4):
			stat[kount] = 0
		rtstatlist.append(stat)


	# Creating the thread list and spawning the threads
	threads = []
	if options["avthreads"] == 1:
		wthread = multiprocessing.Process(target=warthread, args=(options["numberofgames"], 0, rtstatlist))
		threads.append(wthread)
	else:
		tmpgames_playing = options["numberofgames"]
		for count in range(0, options["avthreads"] - 1):
			wthread = multiprocessing.Process(target=warthread, args=(
			options["numberofgames"] // options["avthreads"], count, rtstatlist))
			tmpgames_playing -= options["numberofgames"] // options["avthreads"]
			threads.append(wthread)
			threads[count].start()
		wthread = multiprocessing.Process(target=warthread, args=((tmpgames_playing, count + 1, rtstatlist)))
		threads.append(wthread)
		threads[count + 1].start()
	while (totalup(rtstatlist))[3] != options["numberofgames"]:
		statlist = totalup(rtstatlist)
		# Minimizes a bug from occuring if a thread modified the rtstatlist before the print code finshed processing the first totalup
		if statlist[0] > 0:  # Prevents divide by zero error if the display code was run before any of the threads had a chance to play a game
			if needscreenclear:
				os.system("clear")
				needscreenclear = False
			with term.location(0, 5):
				print("Press Esc to clear the screen (Just in case you accidentally typed garbage)")
				print("Player One has won %f percent of the time.	   " % float(statlist[0] * 100 / statlist[3]))
				print("Player Two has won %f percent of the time.	   " % float(statlist[1] * 100 / statlist[3]))
				print("There has been a draw %f percent of the time.	 \n" % float(statlist[2] / statlist[3]))
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


