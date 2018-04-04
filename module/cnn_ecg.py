import os, sys
#sys.path.append("..")
import pywt
import pywt.data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import tensorflow as tf


def create_DS(ds_num, v_pre, v_post):
    ds1_files = ['101','106','108','109','112','114','115','116','118','119','122','124','201','203','205','207','208','209','215','220','223','230']
    ds2_files = ['100','103','105','111','113','117','121','123','200','202','210','212','213','214','219','221','222','228','231','232','233','234']
    freq = 360
    preX = v_pre
    postX = v_post
    dfall = {} 
    dfann = {} 
    dfseg = {}
    if (ds_num == "1"):
        ds_list = ds1_files;
    else:
        ds_list = ds2_files;
    
    # Load the necessary patient inputs    
    for patient_num in ds_list:
        dfall[patient_num] = pd.read_csv('data/DS'+ds_num+'/'+patient_num+'_ALL_samples.csv', sep=',', header=0, squeeze=False)
        dfann[patient_num] = pd.read_csv('data/DS'+ds_num+'/'+patient_num+'_ALL_ANN.csv', sep=',', header=0, parse_dates=[0], squeeze=False)
   
    # Standardize the beat annotations 
    vals_to_replace = {'N':'N','L':'N','e':'N','j':'N','R':'N','A':'SVEB','a':'SVEB','J':'SVEB','S':'SVEB','V':'VEB','E':'VEB','F':'F','Q':'Q','P':'Q','f':'Q','U':'Q'}
    for patient_num in ds_list:
        dfann[patient_num]['Type'] = dfann[patient_num]['Type'].map(vals_to_replace)    
        dfann[patient_num]['RRI'] = (dfann[patient_num]['sample'] - dfann[patient_num]['sample'].shift(1))/360
        dfann[patient_num] = dfann[patient_num][1:]  
    
    
    for patient_num in ds_list:
        begNList = [];
        endNList = [];
        mixNList = [];
        sliceNList = [];

        for index, row in dfann[patient_num].iterrows():
            Nbegin = row['sample'] - preX;
            Nend = row['sample'] + postX;
            begNList.append(Nbegin);
            endNList.append(Nend);

        mixNList = tuple(zip(begNList,endNList)) 
        
        
        #print(mixNList)
        #TODO
        for x in range(0,7):
            dfseg[patient_num] = dfall[patient_num][(dfall[patient_num]['sample'] >= mixNList[x][0]) & (dfall[patient_num]['sample'] <= mixNList[x][1])]
 
    
    return dfall, dfann, dfseg


