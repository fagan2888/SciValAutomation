import os
import sys
import pandas as pd
import numpy as np
from PyAstronomy import pyasl
import datetime

def outliers(df):
	
	fwci = df[['Field-Weighted Citation Impact']].as_matrix()
	r = pyasl.generalizedESD(fwci, 10, 0.05, fullOutput = True)
	df = df.assign(Outliers = 'N/A')
	
	if r[0] > 0:
		for i in range(len(r[1])):
			df.at[r[1][i], 'Outliers'] = fwci[r[1][i]]
	else:
		pass
	return df

	
	
def skip_to(fle, line,**kwargs):
    if os.stat(fle).st_size == 0:
        raise ValueError("File is empty")
    with open(fle) as f:
        pos = 0
        cur_line = f.readline()
        while not cur_line.startswith(line):
            pos = f.tell()
            cur_line = f.readline()
        f.seek(pos)
        return pd.read_csv(f, error_bad_lines = False, encoding = 'ISO-8859-1', nrows = 100, **kwargs)
		
		

def readAll(path, file):

	df = skip_to(path + file, 'Institution')
	if 'Unnamed' in df.columns[-1]:
		df.drop(df.columns[-1,], axis=1, inplace=True)
	df.dropna()
	data_name = skip_to(path + file, 'Entity').iloc[:0].to_string().split(',')[1]
	if ']' in data_name: 
		data_name = data_name.split(']')[0]
	data_year = skip_to(path + file, 'Year range').iloc[:0].to_string().split(',')[1].replace('to', '-')
	if ']' in data_year: 
		data_year = data_year.split(']')[0]
	curr_year = datetime.date.today().strftime("%Y")

	df['Subject'] = data_name
	df['Year range'] = data_year
	df['Analysis year'] = curr_year
	
	return df

	
def readGov(path, file):

	doe_labs = ['Oak Ridge National Laboratory', 'Argonne National Laboratory', 'Lawrence Berkeley National Laboratory', 'Pacific Northwest National Laboratory', 'Brookhaven National Laboratory', 'Los Alamos National Laboratory', 'National Renewable Energy Laboratory', 'Lawrence Livermore National Laboratory', 'Sandia National Laboratories NM', 'Ames Laboratory', 'Sandia National Laboratories CA', 'Idaho National Laboratory', 'Fermi National Accelerator Laboratory', 'Princeton Plasma Physics Laboratory', 'SLAC National Accelerator Laboratory', 'Thomas Jefferson National Accelerator Facility', 'National Energy Technology Laboratory', 'Savannah River National Laboratory']
	
	df = skip_to(path + file, 'Institution')
	if 'Unnamed' in df.columns[-1]:
		df.drop(df.columns[-1,], axis=1, inplace=True)
	df.dropna()
	data_name = skip_to(path + file, 'Entity').iloc[:0].to_string().split(',')[1]
	if ']' in data_name: 
		data_name = data_name.split(']')[0]
	data_year = skip_to(path + file, 'Year range').iloc[:0].to_string().split(',')[1].replace('to', '-')
	if ']' in data_year: 
		data_year = data_year.split(']')[0]
	curr_year = datetime.date.today().strftime("%Y")
	
	df['Subject'] = data_name
	df['Year range'] = data_year
	df['Analysis year'] = curr_year
	
	df = df.loc[df['Institution'].isin(doe_labs)]
	
	return df

def getFiles(area):
	
	df = pd.DataFrame()
	
	apath = '#apath' + '/' + area + '/Raw Data/All/'
	gpath = '#bpath' + '/' + area + '/Raw Data/Gov/'

	afiles = os.listdir(apath)
	gfiles = os.listdir(gpath)
	aFiles = [f for f in afiles if f[-3:] == 'csv']
	gFiles = [f for f in gfiles if f[-3:] == 'csv']

	if len(afiles) == len(gfiles):
		print("All files accounted for")

		for f, g in zip(aFiles, gFiles):
			df_data = readAll(apath, f)
			df_g = readGov(gpath, g)
			dfa = pd.concat([df_data, df_g])
			dfa = dfa.reset_index(drop=True)
			dfa = outliers(dfa)
			dfa = dfa.assign(Median = np.median(dfa[['Scholarly Output']].as_matrix()))
			df = df.append(dfa)
	else:
		print("Please check for missing files")
		
	return df
