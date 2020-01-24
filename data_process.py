# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:12:52 2020

@author: Oliver
"""

import os
from tabula import read_pdf
import pandas as pd
import numpy as np
import pickle

FOLDER = "2018"
filename = "201801N.pdf"


def clean_crime_data(folder, filename):
    file_path = os.path.join(FOLDER, filename)
    df = read_pdf(file_path)
    df = df[0]
    COLUMNS = ["Sex Offences", "Assaults", "Robbery",
               "B&E", "Theft of MV", "Theft from Auto", "Theft<>5k",
               "Arson", "Mischief", "Offensive Weapons"]
    
    df.index = df.iloc[:,0]

    df = df.iloc[:,1:]
    df = df.replace(np.nan, '', regex=True)
    
    if FOLDER == "2019":
        # b&E and theft of mv are linked together
        be = df.iloc[:,3].map(lambda x: x.split()[0] if x.split() else x)
        theft_of_mv = df.iloc[:,3].map(lambda x: x.split()[1] if x.split() else x)
        
        be = pd.DataFrame({"B&E":be})
        theft_of_mv = pd.DataFrame({"Theft of MV": theft_of_mv})
        df = pd.concat((df.iloc[:,:3],be,theft_of_mv, df.iloc[:,4:]), axis=1)
    
    column_replace = {k:v for k,v in zip(df.columns, COLUMNS)}
    
    df = df.rename(column_replace, axis=1)
    df.index.name = "Neighborhood"
    if FOLDER == "2019":
        df = df.iloc[2:,:]
    elif FOLDER == "2018":
        df = df.iloc[1:,:]
    
    df = df.astype('int32')
    new_index = []
    ord45 = '-'
    ord8208 = '‐'
    for idx in df.index:
        temp = idx.strip().split()
        if ord45 in temp or ord8208 in temp: # first has ord() 45, second has ord() 8208
            placeholder = ''.join(temp)
            if ord8208 in temp:
                placeholder = placeholder.replace(ord8208, ord45)
            new_index.append(placeholder)
        else:
            new_index.append(' '.join(temp))
    df.index = new_index
    return df

all_cleaned_data = {}
for filename in os.listdir(FOLDER):
    all_cleaned_data[filename] = clean_crime_data(FOLDER, filename)
    
    
with open(os.path.join(FOLDER+"_cleaned_data.pickle"), 'wb') as f:
    pickle.dump(all_cleaned_data, f)