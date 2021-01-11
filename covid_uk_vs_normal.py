#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:05:53 2021

@author: christoffer
"""

import numpy as np
import matplotlib.pyplot as plt

# Forskellige sceneriar er for R til test
R0s = [.96, .85, .8, .7]

# Antagelser
n0 = 2000                       # Total start
UK_andel0 = 0.025               # UK andel start
n_normal0 = (1-UK_andel0) * n0  # Normal strain start
n_UK0     = UK_andel0 * n0      # UK strain start
G = 4.7                         # Generationstid
UK_R_factor = 1.5               # Øget smitsomhed UK strain

t = np.arange(0,101)            # Varighed

# Gem data her
n_normals = np.zeros((len(R0s), len(t)))
n_UKs     = np.zeros((len(R0s), len(t)))
n_totals  = np.zeros((len(R0s), len(t)))

f, ax = plt.subplots(nrows=2, ncols=2) # Figur til alle data
for i, R0 in enumerate(R0s):
    
    # R i givent scenarie
    R_normal = R0
    R_UK     = UK_R_factor * R0
    
    # Antal normal og UK som funktion af tid
    n_normal = n_normal0 * R_normal**(t/G)
    n_UK     = n_UK0     * R_UK**(t/G)
    
    # Total antal
    n_total = n_normal + n_UK
    
    # Plot
    ax[i//2, i % 2].plot(t, n_normal, color='C%d' % i, ls=':')
    ax[i//2, i % 2].plot(t, n_UK    , color='C%d' % i, ls='-.')
    
    ax[i//2, i % 2].plot(t, n_total, color='C%d' % i, label='R_ref = %.2f' % R0s[i])
    
    ax[i//2, i % 2].legend(loc='upper left')
    ax[i//2, i % 2].set_ylim(0, 4000)
    
    # Gem data
    n_normals[i, :] = n_normal
    n_UKs[i, :]     = n_UK
    n_totals[i, :]  = n_total    

f.tight_layout()

# Plot kun totaler
plt.figure()
for i in range(len(R0s)):
    plt.plot(t, n_totals[i], color='C%d' % i, label='R_ref = %.2f' % R0s[i])
    
plt.legend()
plt.ylim(0,4000)
plt.tight_layout()

import xlsxwriter
workbook = xlsxwriter.Workbook('COVID-beregning.xlsx')
for i in range(len(R0s)):
    worksheet = workbook.add_worksheet(name='R_ref = %.2f' % R0s[i])
    worksheet.write(0,0,'tid [dage]')
    worksheet.write(0,1,'n_normal')
    worksheet.write(0,2,'n_UK')
    worksheet.write(0,3,'n_total')
    for j in range(len(t)):
        worksheet.write(j+1,0,t[j])
        worksheet.write(j+1,1,n_normals[i,j])
        worksheet.write(j+1,2,n_UKs[i,j])
        worksheet.write(j+1,3,n_totals[i,j])
        
workbook.close()
