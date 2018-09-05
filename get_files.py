import os
import sys
import pandas as pd
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


def readAll(path, file):

	df = pd.read_excel(path + file, skiprows = 16, usecols = [0, 1, 2, 3]).dropna()
	df_x = pd.read_excel(path + file)
	data_name = df_x.iloc[0].to_string(name = True).split(',')[1]
	data_year = df_x.iloc[1].to_string(name = True).split(',')[1].replace('to', '-')
	curr_year = datetime.date.today().strftime("%Y")

	df['Subject'] = data_name
	df['Year range'] = data_year
	df['Analysis year'] = curr_year
	
	#add "outliers" column, assign any found outliers
	df = outliers(df)
	
	return df

def readGov(path, file):

	doe_labs = ['Oak Ridge National Laboratory', 'Argonne National Laboratory', 'Lawrence Berkeley National Laboratory', 'Pacific Northwest National Laboratory', 'Brookhaven National Laboratory', 'Los Alamos National Laboratory', 'National Renewable Energy Laboratory', 'Lawrence Livermore National Laboratory', 'Sandia National Laboratories NM', 'Ames Laboratory', 'Sandia National Laboratories CA', 'Idaho National Laboratory', 'Fermi National Accelerator Laboratory', 'Princeton Plasma Physics Laboratory', 'SLAC National Accelerator Laboratory', 'Thomas Jefferson National Accelerator Facility', 'National Energy Technology Laboratory', 'Savannah River National Laboratory']
	
	df = pd.read_excel(path + file, skiprows = 19, usecols = [0, 1, 2, 3]).dropna()
	df_x = pd.read_excel(path + file)
	data_name = df_x.iloc[0].to_string(name = True).split(',')[1]
	data_year = df_x.iloc[1].to_string(name = True).split(',')[1].replace('to', '-')
	data_sector = df_x.iloc[10].to_string(name = True).split(',')[1]
	curr_year = datetime.date.today().strftime("%Y")
	
	df['Subject'] = data_name
	df['Year range'] = data_year
	df['Analysis year'] = curr_year
	
	df = df.loc[df['Institution'].isin(doe_labs)]
	
	return df

def getFiles(area):
	
	df = pd.DataFrame()
	
	apath = '#inputPath' + '/' + area + '/Raw Data/All/'
	gpath = '#inputPath' + '/' + area + '/Raw Data/Gov/'

	afiles = os.listdir(apath)
	gfiles = os.listdir(gpath)
	aFiles = [f for f in afiles if f[-3:] == 'xls']
	gFiles = [f for f in gfiles if f[-3:] == 'xls']

	if len(afiles) == len(gfiles):
		print("All files accounted for")

		for f, g in zip(aFiles, gFiles):
			df_data = readAll(apath, f)
			df_g = readGov(gpath, g)
			dfa = df_data.merge(df_g, left_on = "Institution", right_on = "Institution", how = "outer")
			c = list(dfa)
			dfa.drop(c[8:], axis = 1, inplace = True)
			df = df.append(dfa)
		return df
		
	else:
		print("Please check for missing files")
