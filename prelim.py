import os
import sys

def ask_user():
	user_request = input('Please type the code for the area you would like to analyze \n H = High Performance Computing \n M = Materials \n Ne = Neutrons \n Nu = Nuclear \n\n\n')

	if user_request == 'H':
		area = 'High Performance Computing'
	elif user_request == 'M':
		area = 'Materials'
	elif user_request == 'Ne':
		area = 'Neutrons'
	elif user_request == 'Nu':
		area = 'Nuclear'

	print('\nProcessing ' + area + '...')
	
	return area
	

		
