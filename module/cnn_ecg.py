import os, sys
#sys.path.append("..")
import pywt
import pywt.data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal


def create_DS(ds_num):
    ds1_files = ['101','106','108','109','112','114','115','116','118','119','122','124','201','203','205','207','208','209','215','220','223','230']
    ds2_files = ['100','103','105','111','113','117','121','123','200','202','210','212','213','214','219','221','222','228','231','232','233','234']
    dfall = {} 
    dfann = {} 
    if (ds_num == "1"):
         ds_list = ds1_files;
    else:
        ds_list = ds2_files;
    
    #load the necessary patient inputs    
    for patient_num in ds_list:
        dfall[patient_num] = pd.read_csv('data/DS'+ds_num+'/'+patient_num+'_ALL_samples.csv', sep=',', header=0, squeeze=False)
        dfann[patient_num] = pd.read_csv('data/DS'+ds_num+'/'+patient_num+'_ALL_ANN.csv', sep=',', header=0, parse_dates=[0], squeeze=False)
   
    # Standardize the beat annotations...  
    vals_to_replace = {'N':'N','L':'N','e':'N','j':'N','R':'N','A':'SVEB','a':'SVEB','J':'SVEB','S':'SVEB','V':'VEB','E':'VEB','F':'F','Q':'Q','P':'Q','f':'Q','U':'Q'}
    for patient_num in ds_list:
        dfann[patient_num]['Type'] = dfann[patient_num]['Type'].map(vals_to_replace)
        
    return dfall, dfann


