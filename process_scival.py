import pandas as pd

import os
import sys

import prelim, get_files

def main():

######
	area = prelim.ask_user()
	df = get_files.getFiles(area)

	out_path = '#outputPath' + '/' + area + '/Processed Data/'
	
	data_year = "fix this"
	
	writer = pd.ExcelWriter(out_path + area + '_' + data_year + '.xlsx', engine = 'xlsxwriter')
	df.to_excel(writer, index = False, encoding ='ISO-8859-1')
	writer.save()

main()
