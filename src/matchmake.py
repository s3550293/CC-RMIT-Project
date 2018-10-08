# import webapp2
import requests
import time

def matchmake(players):
	for i in range(len(players)):
		resp = requests.get('https://api.fortnitetracker.com/v1/profile/pc/'+players[i], headers={'TRN-Api-Key' : 'e5d4ace5-28ae-4579-a6d4-fad7b8ad556d'})
		data = resp.json()
		print data["epicUserHandle"]
		print data["accountId"]
		print data["platformNameLong"]
		print data["lifeTimeStats"]
		return


players = ['aox_', 'Ninja', 'GassyKraken', 'Soul-Cake', 'Muselk', 'SleazyJo']
matchmake(players)