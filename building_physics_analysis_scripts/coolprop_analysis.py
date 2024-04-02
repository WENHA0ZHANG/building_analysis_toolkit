# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 06:34:23 2023

@author: wenha
"""

import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
import numpy as np

fl1 = 'R236fa'
fl2 = 'R40'
fl3 = 'R1233zdE'
tc_h = 50 + 273.15 # Higher ondenser temperature
te_l = -25 + 273.15 # Lower evaporator temperature
tin = 10 + 273.15


def cop_function(tc_h, te_l, tin, fl1, fl2):
    # COP = (h1 - h4) / (h2 - h1) + (h6 - h5)
    q_l = 20000

    h1_l = cp.PropsSI('H', 'T', te_l, 'Q', 1, fl1)

    s1_l = cp.PropsSI('S', 'T', te_l, 'Q', 1, fl1)
    s2_l = s1_l
    pc_l = cp.PropsSI('P', 'T', tin, 'Q', 1, fl1)
    h2_l = cp.PropsSI('H', 'P', pc_l, 'S', s2_l, fl1)

    win_l = h2_l - h1_l
    print(h2_l, h1_l)

    h3_l = cp.PropsSI('H', 'T', tin, 'Q', 0, fl1)
    h4_l = h3_l

    h_l = h1_l - h4_l
    m_l = q_l / h_l
    
    q23 = (h3_l - h2_l) * m_l
    q58 = -q23
    
    h5_h = cp.PropsSI('H', 'T', tin, 'Q', 1, fl2)

    s5_h = cp.PropsSI('S', 'T', tin, 'Q', 1, fl2)
    s6_h = s5_h
    pc_h = cp.PropsSI('P', 'T', tc_h, 'Q', 1, fl2)
    h6_h = cp.PropsSI('H', 'P', pc_h, 'S', s6_h, fl2)
    
    h7 = cp.PropsSI('H', 'T', tc_h, 'Q', 0, fl2)
    h8 = h7
    h58 = h5_h - h8
    
    m_h = q58 / h58

    win_h = h6_h - h5_h
    print(h6_h, h5_h)
    cop = (h_l * m_l) / (win_l * m_l + win_h * m_h)
    print('COP:', cop)
    return cop


tin_list = list(np.linspace(-25+273,50+273,100))
cop_list = list()

for tin in tin_list:
    cop = cop_function(tc_h, te_l, tin, fl3, fl2)
    # print('new_cop', cop)
    cop_list.append(cop)
# print(cop_list)
copMax = max(cop_list)
maxIndex = cop_list.index(max(cop_list))
print("The highest COP is",copMax," when temperature is", tin_list[maxIndex])
plt.plot(tin_list, cop_list)
plt.xlabel("Temperature (K)")
plt.ylabel("COP")
plt.title("COP - Low_R1233zd(E) and High_R40")
plt.show()

plt.plot(tin_list, cop_list, 'ro')
plt.xlabel("Temperature (K)")
plt.ylabel("COP")
plt.title("COP - Low_R1233zd(E) and High_R40")
plt.show()




