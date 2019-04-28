import csv
import random


class card2():
	worth = 2
	kind=2
class card3():
	worth = 3
	kind=3
class card4():
	worth = 4
	kind=4
class card5():
	worth = 5
	kind=5
class card6():
	worth = 6
	kind=6
class card7():
	worth = 7
	kind=7
class card8():
	worth = 8
	kind=8
class card9():
	worth = 9
	kind=9
class card10():
	worth = 10
	kind=10
class cardjack():
	worth = 11
	kind='Jack'
class cardqueen():
	worth = 12
	kind='Queen'
class cardking():
	worth = 13
	kind="King"
class cardace():
	worth = 14
	kind="Ace"
cardtypes=[card2,card3,card4,card5,card6,card7,card8,card9,card10,cardjack,cardqueen,cardking,cardace]

def playwar(fileoutput="report.csv"):
	#We are going to make a CSV containing all the




	tmp_deck = []
	for i in cardtypes:
		for l in range(0, 4):
			tmp_deck.append(i)
	shuffled_deck = []
	for shufflenumber in range(0, 10):
		while tmp_deck.__len__() != 0:
			index = random.randint(0, len(tmp_deck) - 1)
			selection = tmp_deck[index]
			shuffled_deck.append(tmp_deck[index])
			tmp_deck.remove(selection)
		tmp_deck = shuffled_deck
		shuffled_deck = []
	tmp_deck.reverse()
	shuffled_deck = list(tmp_deck)  # Note, the top of the list is now the last index.
	playerone = shuffled_deck[0:int(len(shuffled_deck) / 2)]
	playertwo = shuffled_deck[int(len(shuffled_deck) / 2):]
	cancontinue = True
	p1wins = False
	p2wins = False
	while (len(playerone) != 0 and len(playertwo) != 0) and cancontinue:
		p1c = playerone.pop()
		p2c = playertwo.pop()
		p1cw = p1c.worth
		p2cw = p2c.worth
		if p1cw > p2cw:
			playerone.insert(0, p1c)
			playerone.insert(0, p2c)
		elif p2cw > p1cw:
			playertwo.insert(0, p2c)
			playertwo.insert(0, p1c)
		elif p2cw == p1cw:
			cardpot = []
			iswinner = False
			while (True != iswinner):
				cardpot.append(p1c)
				cardpot.append(p2c)
				if playerone.__len__() < 4:
					if playertwo.__len__() < 4:
						cancontinue = False
						draws=True
						break
					else:
						p2wins = True
						cancontinue = False
						break
				elif playertwo.__len__() < 4:
					p1wins = True
					cancontinue = False
					break
				else:
					for i in range(0, 3):
						cardpot.append(playerone.pop())
						cardpot.append(playertwo.pop())
					p1c = playerone.pop()
					p2c = playertwo.pop()
					p1cw = p1c.worth
					p2cw = p2c.worth
					if p1cw > p2cw:
						iswinner = True
						playerone.insert(0, p1c)
						playerone.insert(0, p2c)
						for card in cardpot:
							playerone.insert(0, card)
					elif p2cw > p1cw:
						iswinner = True
						playertwo.insert(0, p1c)
						playertwo.insert(0, p2c)
						for card in cardpot:
							playertwo.insert(0, card)

	# CSV Writing
	csvwriteonly = open(fileoutput, 'a')
	data = []
	namedeck = []
	for name in shuffled_deck:
		namedeck.append(name.kind)
	data.append(namedeck)
	data.append(namedeck[0:int(len(namedeck) / 2)])
	data.append(namedeck[int(len(namedeck) / 2):])
	if (playerone.__len__() == 0 and cancontinue == True) or p1wins:
		data.append("Player 1")
	elif playertwo.__len__() == 0  and cancontinue == True or p2wins:
		data.append("Player 2")
	elif draws:
		data.append("DRAW")
	csvwriter = csv.writer(csvwriteonly)
	csvwriter.writerow(data)
	csvwriteonly.close()

	if (playerone.__len__() == 0 and cancontinue == True) or p1wins:
		return 1 #Player one won
	elif playertwo.__len__() == 0  and cancontinue == True or p2wins:
		return 2 #Player two won
	elif draws:
		return 3 #It was a draw
