# from google.cloud import bigquery
# from google.cloud.bigquery import dataset
# import webapp2
import requests
import json
import time



def matchmake(players):
	for i in range(len(players)):
		resp = requests.get('https://api.fortnitetracker.com/v1/profile/pc/'+players[i], headers={'TRN-Api-Key' : 'e5d4ace5-28ae-4579-a6d4-fad7b8ad556d'})
		data = resp.json()
		
		print "EpicName: " + data["epicUserHandle"]
		print "AccountId: " + data["accountId"]
		print "Platform: " + data["platformName"]
		print "Solo Rating: " + str(data["stats"]["p2"]["trnRating"]["valueInt"])
		print "Squads Rating: " + str(data["stats"]["p9"]["trnRating"]["valueInt"])
		print "Duo Rating: " + str(data["stats"]["p10"]["trnRating"]["valueInt"])
		print "Score: " + str(data["lifeTimeStats"][6].get('value'))
		print "Matches Played: " + str(data["lifeTimeStats"][7].get('value'))
		print "Wins: " + str(data["lifeTimeStats"][8].get('value'))
		print "Win%: " + str(data["lifeTimeStats"][9].get('value'))
		print "Kills: " + str(data["lifeTimeStats"][10].get('value'))
		print "K/d: " + str(data["lifeTimeStats"][11].get('value'))
		print "\n"
		time.sleep(2)
		# return

def search():
	print "We are searching"
	
	return

players = ['Ninja', 'Dark', 'Not Tfue', 'Symfuhny', 'TSM_Myth', 'C9 ZOOF', 'YamatoN_jp']
matchmake(players)