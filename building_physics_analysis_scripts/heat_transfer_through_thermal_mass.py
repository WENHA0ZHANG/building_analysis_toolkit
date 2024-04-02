# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:24:51 2022

@author: wenha
"""

import pandas as pd
import numpy as np
import math

data = pd.read_csv('C:/Users/wenha/Desktop/0084_cw2/weather.csv',sep=',')
ODT = np.array(data.iloc[:,3]) # Outdoor Dry-blub Temperature
S_dif = np.array(data.iloc[:,1]) # Site Diffuse Solar Radiation Rate per Area
S_dir = np.array(data.iloc[:,2]) # Site Direct Solar Radiation Rate per Area
S_Alt = np.array(data.iloc[:,4]) # Site Solar Altitude Angle
S_Azi = np.array(data.iloc[:,5])-180 # Site Solar Azimuth Angle
datetime = list(data.iloc[:,0])

#initial condition of floor
f_r1 = 0.071
f_r2 = 25.175
FTC_lst = [] # temperature of effective thermal mass
FTC_lst.append(10)
FQIN_lst = []

#initial condition of wall
r1 = 0.196
r2 = 1.601
c1 = 1000 * 1400 * 0.08525
c2 = 1000 * 1400 * 0.08
tc0 = 10
L = 3600
IOT = 19
A = 70 #area of wall
g = 0.9
r3 = 0.034

w_TC_lst = [] # temperature of effective thermal mass
w_TC_lst.append(tc0)
s_TC_lst = [] # temperature of effective thermal mass
s_TC_lst.append(tc0)
e_TC_lst = [] # temperature of effective thermal mass
e_TC_lst.append(tc0)
n_TC_lst = [] # temperature of effective thermal mass
n_TC_lst.append(tc0)
N_tilt = 90
N_ori = 180
W_tilt = 90
W_ori = 90
E_tilt = 90
E_ori = 270
S_tilt = 90
S_ori = 0
r_W_tilt = math.radians(W_tilt)
r_W_ori = math.radians(W_ori)
r_S_tilt = math.radians(S_tilt)
r_S_ori = math.radians(S_ori)
r_E_tilt = math.radians(E_tilt)
r_E_ori = math.radians(E_ori)
r_N_tilt = math.radians(N_tilt)
r_N_ori = math.radians(N_ori)
wQ_sun = []
wQ_sun.append(0)
eQ_sun = []
eQ_sun.append(0)
sQ_sun = []
sQ_sun.append(0)
nQ_sun = []
nQ_sun.append(0)
QIN_lst = []

# window solar heat gain
G_value = 0.789
A_window = 12 #area
U_win = 3
QS_win = [] # window solar heat gain

# solar heat gain of roof
U_roof = 0.318
ac = 0.9 # absorption coefficient
r_tilt = 0
r_ori = 0
r_r_tilt = math.radians(r_tilt)
r_r_ori = math.radians(r_ori)
rQ_sun = []

def cos_i1(z,tilt,azi,ori):
    cos = math.sin(z) * math.sin(tilt) * math.cos(math.radians(azi-ori)) + math.cos(z) *math.cos(tilt)
    return cos

def darkTC(IOT,r1,ODT1,ODT2,r2,c1,L,TC_lst):
    TC = (((IOT+IOT)/r1) + ((ODT1+ODT2)/r2) + (((2*c1)/L)-1/r1-1/r2)*TC_lst)/(((2*c1)/L)+1/r1+1/r2)
    return TC

# thermal mass, roof, window solar heat gain calculation

for x in range(len(S_Alt)):
    if S_Alt[x] <= 0:
        TCn = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,n_TC_lst[-1])
        TCw = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,w_TC_lst[-1])
        TCs = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,s_TC_lst[-1])
        TCe = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,e_TC_lst[-1])
        n_TC_lst.append(TCn)
        w_TC_lst.append(TCw)
        s_TC_lst.append(TCs)
        e_TC_lst.append(TCe)
        wQ_sun.append(0)
        eQ_sun.append(0)
        sQ_sun.append(0)
        nQ_sun.append(0)

        #print(TC_lst[0:3])
        wQIN = ((IOT-TCw)/r1)*15
        sQIN = ((IOT-TCs)/r1)*20
        nQIN = ((IOT-TCn)/r1)*20
        eQIN = ((IOT-TCe)/r1)*15
        QIN = wQIN + sQIN + nQIN + eQIN
        QIN_lst.append(QIN)
        # window
        QS_win.append(0)
        #roof
        QRoof = U_roof * (ODT[x]-IOT) * 48
        rQ_sun.append(QRoof)
        #floor
        TCf = darkTC(IOT,f_r1,12,12,f_r2,c2,L,FTC_lst[-1])      
        FTC_lst.append(TCf)
        FQIN = ((IOT-TCf)/f_r1)*48
        FQIN_lst.append(FQIN)

    else:
        if S_Azi[x] > -180 and S_Azi[x] < -90:
            sz = 90 - S_Alt[x]
            r_sz = math.radians(sz)
            #n
            n_cos_i1 = cos_i1(r_sz,r_N_tilt,S_Azi[x],N_ori)
            nQsun_temp = S_dir[x] * n_cos_i1 + S_dif[x] * ((1 + math.cos(r_N_tilt))/2)
            nQ_sun.append(nQsun_temp)
            
            #w_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*w_TC_lst[-1] + (ODT[x]-ODT[x-1])/(r2+r3) + g*r3/(r2+r3))/((2*c1)/L+1/r1+1/(r2+r3))
            n_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*n_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(nQ_sun[x-1]+nQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
          
            n_TC_lst.append(n_TC)
            nQIN = ((IOT-n_TC)/r1)*20
            #e
            e_cos_i1 = cos_i1(r_sz,r_E_tilt,S_Azi[x],E_ori)
            eQsun_temp = S_dir[x]  * e_cos_i1 + S_dif[x] * ((1 + math.cos(r_E_tilt))/2)
            eQ_sun.append(eQsun_temp)
            e_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*e_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(eQ_sun[x-1]+eQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
            e_TC_lst.append(e_TC)
            eQIN = ((IOT-e_TC)/r1)*15
            #s
            sQ_sun.append(0)
            s_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,s_TC_lst[-1])
            s_TC_lst.append(s_TC)
            sQIN = ((IOT-s_TC)/r1)*20
            #w
            wQ_sun.append(0)
            w_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,w_TC_lst[-1])
            w_TC_lst.append(w_TC)
            wQIN = ((IOT-w_TC)/r1)*15
            #sum
            QIN = wQIN + sQIN + nQIN + eQIN
            QIN_lst.append(QIN)
            #window solar heat gain
            QS_win.append(0)
            #roof 
            r_cos_i1 = math.cos(r_sz)
            rQsun_temp = S_dir[x] * r_cos_i1 + S_dif[x] * ((1 + math.cos(r_r_tilt))/2)
            sat = ODT[x] + (ac * rQsun_temp)/25
            QS_Roof = U_roof * (sat - IOT) * 48
            rQ_sun.append(QS_Roof)
            #floor
            TCf = darkTC(IOT,f_r1,12,12,f_r2,c2,L,FTC_lst[-1])      
            FTC_lst.append(TCf)
            FQIN = ((IOT-TCf)/f_r1)*48
            FQIN_lst.append(FQIN)
         
            
        elif S_Azi[x] < 0 and S_Azi[x] > -90:
            sz = 90 - S_Alt[x]
            r_sz = math.radians(sz)
            #e
            e_cos_i1 = cos_i1(r_sz,r_E_tilt,S_Azi[x],E_ori)
            eQsun_temp = S_dir[x] * e_cos_i1 + S_dif[x] * ((1 + math.cos(r_E_tilt))/2)
            eQ_sun.append(eQsun_temp)
            e_TC = ((IOT+IOT)/r1 + (((2*c1)/L)-1/r1-1/(r2+r3))*e_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(eQ_sun[x-1]+eQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
            e_TC_lst.append(e_TC)
            eQIN = ((IOT-e_TC)/r1)*15
            #s
            s_cos_i1 = cos_i1(r_sz,r_S_tilt,S_Azi[x],S_ori)
            sQsun_temp = S_dir[x]  * s_cos_i1 + S_dif[x] * ((1 + math.cos(r_S_tilt))/2)
            sQ_sun.append(sQsun_temp)
            s_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*s_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(sQ_sun[x-1]+sQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
            s_TC_lst.append(s_TC)
            sQIN = ((IOT-s_TC)/r1)*20
            #w
            wQ_sun.append(0)
            w_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,w_TC_lst[-1])
            w_TC_lst.append(w_TC)
            wQIN = ((IOT-w_TC)/r1)*15
            #n
            nQ_sun.append(0)
            n_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,n_TC_lst[-1])
            n_TC_lst.append(n_TC)
            nQIN = ((IOT-n_TC)/r1)*20
            #sum
            QIN = wQIN + sQIN + nQIN + eQIN
            QIN_lst.append(QIN)
            #window solar heat gain
            
            SolarHeatGainWindow = G_value * A_window * sQsun_temp
            QS_win.append(SolarHeatGainWindow)
            #roof 
            r_cos_i1 = math.cos(r_sz)
            rQsun_temp = S_dir[x] * r_cos_i1 + S_dif[x] * ((1 + math.cos(r_r_tilt))/2)
            sat = ODT[x] + (ac * rQsun_temp)/25
            QS_Roof = U_roof * (sat - IOT)* 48
            rQ_sun.append(QS_Roof)
            #floor
            TCf = darkTC(IOT,f_r1,12,12,f_r2,c2,L,FTC_lst[-1])      
            FTC_lst.append(TCf)
            FQIN = ((IOT-TCf)/f_r1)*48
            FQIN_lst.append(FQIN)
            
        elif S_Azi[x] > 0 and S_Azi[x] < 90:
            sz = 90 - S_Alt[x]
            r_sz = math.radians(sz)
            #w
            w_cos_i1 = cos_i1(r_sz,r_W_tilt,S_Azi[x],W_ori)
            wQsun_temp = S_dir[x] * w_cos_i1 + S_dif[x] * ((1 + math.cos(r_W_tilt))/2)
            wQ_sun.append(wQsun_temp)
            
            #w_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*w_TC_lst[-1] + (ODT[x]-ODT[x-1])/(r2+r3) + g*r3/(r2+r3))/((2*c1)/L+1/r1+1/(r2+r3))
            w_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*w_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(wQ_sun[x-1]+wQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
          
            w_TC_lst.append(w_TC)
            wQIN = ((IOT-w_TC)/r1)*15
            #s
            s_cos_i1 = cos_i1(r_sz,r_S_tilt,S_Azi[x],S_ori)
            sQsun_temp = S_dir[x]  * s_cos_i1 + S_dif[x] * ((1 + math.cos(r_S_tilt))/2)
            sQ_sun.append(sQsun_temp)
            s_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*s_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(sQ_sun[x-1]+sQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
            s_TC_lst.append(s_TC)
            sQIN = ((IOT-s_TC)/r1)*20
            #e
            eQ_sun.append(0)
            e_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,e_TC_lst[-1])
            e_TC_lst.append(e_TC)
            eQIN = ((IOT-e_TC)/r1)*15
            #n
            nQ_sun.append(0)
            n_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,n_TC_lst[-1])
            n_TC_lst.append(n_TC)
            nQIN = ((IOT-n_TC)/r1)*20
            #sum
            QIN = wQIN + sQIN + nQIN + eQIN
            QIN_lst.append(QIN)
            #window solar heat gain
            
            SolarHeatGainWindow = G_value * A_window * sQsun_temp
            QS_win.append(SolarHeatGainWindow)
            #roof 
            r_cos_i1 = math.cos(r_sz)
            rQsun_temp = S_dir[x] * r_cos_i1 + S_dif[x] * ((1 + math.cos(r_r_tilt))/2)
            sat = ODT[x] + (ac * rQsun_temp)/25
            QS_Roof = U_roof * (sat - IOT)*48
            rQ_sun.append(QS_Roof)
            #floor
            TCf = darkTC(IOT,f_r1,12,12,f_r2,c2,L,FTC_lst[-1])      
            FTC_lst.append(TCf)
            FQIN = ((IOT-TCf)/f_r1)*48
            FQIN_lst.append(FQIN)
            
        elif S_Azi[x] > 90 and S_Azi[x] < 180:
            sz = 90 - S_Alt[x]
            r_sz = math.radians(sz)
            #w
            w_cos_i1 = cos_i1(r_sz,r_W_tilt,S_Azi[x],W_ori)
            wQsun_temp = S_dir[x] * w_cos_i1 + S_dif[x] * ((1 + math.cos(r_W_tilt))/2)
            wQ_sun.append(wQsun_temp)
            
            #w_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*w_TC_lst[-1] + (ODT[x]-ODT[x-1])/(r2+r3) + g*r3/(r2+r3))/((2*c1)/L+1/r1+1/(r2+r3))
            w_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*w_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(wQ_sun[x-1]+wQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
          
            w_TC_lst.append(w_TC)
            wQIN = ((IOT-w_TC)/r1)*15
            #n
            n_cos_i1 = cos_i1(r_sz,r_N_tilt,S_Azi[x],N_ori)
            nQsun_temp = S_dir[x]  * n_cos_i1 + S_dif[x] * ((1 + math.cos(r_N_tilt))/2)
            nQ_sun.append(nQsun_temp)
            n_TC = ((IOT+IOT)/r1 + ((2/L*c1)-1/r1-1/(r2+r3))*n_TC_lst[-1] + (ODT[x]+ODT[x-1])/(r2+r3) + g*r3/(r2+r3)*(nQ_sun[x-1]+nQ_sun[x]))/((2*c1)/L+1/r1+1/(r2+r3))
            n_TC_lst.append(n_TC)
            nQIN = ((IOT-n_TC)/r1)*20
            #e
            eQ_sun.append(0)
            e_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,e_TC_lst[-1])
            e_TC_lst.append(e_TC)
            eQIN = ((IOT-e_TC)/r1)*15
            #s
            sQ_sun.append(0)
            s_TC = darkTC(IOT,r1,ODT[x],ODT[x-1],r2,c1,L,s_TC_lst[-1])
            s_TC_lst.append(s_TC)
            sQIN = ((IOT-s_TC)/r1)*20
            #sum
            QIN = wQIN + sQIN + nQIN + eQIN
            QIN_lst.append(QIN)
            #window solar heat gain
            QS_win.append(0)
            #roof 
            r_cos_i1 = math.cos(r_sz)
            rQsun_temp = S_dir[x] * r_cos_i1 + S_dif[x] * ((1 + math.cos(r_r_tilt))/2)
            sat = ODT[x] + (ac * rQsun_temp)/25
            QS_Roof = U_roof * (sat - IOT)*48
            rQ_sun.append(QS_Roof)
            #floor
            TCf = darkTC(IOT,f_r1,12,12,f_r2,c2,L,FTC_lst[-1])      
            FTC_lst.append(TCf)
            FQIN = ((IOT-TCf)/f_r1)*48
            FQIN_lst.append(FQIN)

# window heat loss
win_HL = []
for x in range(len(S_Alt)):
    winhl = U_win * (ODT[x]-IOT) * A_window
    win_HL.append(winhl)

# ventilation heat loss
vent_HL = []
for x in range(len(S_Alt)):
    venthl = 1020 * 1.2 * 0.06 *(ODT[x]-IOT)
    vent_HL.append(venthl)


# infiltration heat loss
inf_HL = []
for x in range(len(S_Alt)):
    infhl = (0.5 * 2.5 * 8 * 6 *(ODT[x]-IOT))/3
    inf_HL.append(infhl)



#write to csv
csv = {'datetime':datetime,'Wall_QIN':QIN_lst,'Roof_Heatloss':rQ_sun, 'Solar heat gain of window':QS_win,'Heat loss of window':win_HL,'Heat loss of ventilation':vent_HL,'Heat loss of infiltration':inf_HL,'Heat loss of floor':FQIN_lst}
#print(type(csv))
test =  pd.DataFrame(csv)

test.to_csv('C:/Users/wenha/Desktop/0084_cw2/HW_Baseline.csv',index = False, sep = ',')


#write to csv
csv2 = {'e_TC_lst':e_TC_lst,'n_TC_lst':n_TC_lst,'s_TC_lst':s_TC_lst, 'w_TC_lst':w_TC_lst, 'nQ_sun':nQ_sun, 'wQ_sun':wQ_sun, 'sQ_sun':sQ_sun, 'eQ_sun':eQ_sun, 'FTC_lst':FTC_lst}
#print(type(csv))
test2 =  pd.DataFrame(csv2)

test2.to_csv('C:/Users/wenha/Desktop/0084_cw2/HW_Baseline_Raw.csv',index = False, sep = ',')

