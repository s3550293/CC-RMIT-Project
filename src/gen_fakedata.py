import os
import names
import string
import random

def gen_fakedata():
	fortniteName = 'fa-'
	accountId = 'fakeaccount'
	score = 0
	squadRating = 0

	inc = 0
	while inc < 5000:
		print names.get_first_name() 
		inc = inc + 1

gen_fakedata()