import os
import names
import string
import random

def gen_fakedata():
	email = 'fakeAccount'
	fortniteName = ''
	accountId = 'fakeAccount'
	score = 0
	duoRating = 0
	squadRating = 0

	f = open("fakedata.csv", "w+")

	inc = 0
	while inc < 5000:
		fortniteName = names.get_first_name() + '_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
		score = random.randint(1000, 4500000)
		squadRating = random.randint(500, 4500)

		print '%s,%s,%s,%i,%i,%i\n' % (email, fortniteName, accountId, score, duoRating, squadRating)
		f.write('%s,%s,%s,%i,%i,%i\n' % (email, fortniteName, accountId, score, duoRating, squadRating))
		inc = inc + 1

	f.close()

gen_fakedata()