import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

data=pd.read_csv("/home/valeria/TSA_stuff/TSA_lin_stand/data_stand.csv",header=None,sep=";")
data=data.to_numpy()

time=data[:,0]
target_pos=data[:,1]
real_pos=data[:,4]
ee_pos=data[:,5]

pos=real_pos
turns=pos*0
turn=0
for i in range(1,len(pos)):
    if math.fabs(pos[i]-pos[i-1])>50:
        if pos[i]-pos[i-1]<0:
            turn+=1
        else:
            turn-=1
    turns[i]=turn

# plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
# plt.grid(True)
# plt.plot(time,target_pos,'b',linewidth=2.0)
# plt.plot(time,real_pos,'r',linewidth=2.0)
# # plt.plot(time,turns*20,'g',linewidth=2.0)
# plt.show()

# plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
# plt.grid(True)
# plt.plot(time,real_pos-target_pos,'r',linewidth=2.0)
# plt.show()

plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
plt.grid(True)
plt.plot(time,ee_pos,'r',linewidth=2.0)
plt.show()