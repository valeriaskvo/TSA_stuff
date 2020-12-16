import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

# def trajectory_2(time_v):
#     A=15
#     t=20
#     t_v=time_v-(time_v//t)*t

#     target_position=0
#     label=0


#     if (t_v<= t/4):
#         target_position=A*360.*4.*t_v/t
#         label=1
#     elif ((t_v>=t/4.) and (t_v<=2.*t/4.)):
#         target_position=A*360.
#     elif ((t_v>=2.*t/4.) and (t_v<=3.*t/4.)):
#         target_position=A*360.*(-4.*t_v/t+3)
#         label=2

#     print(t_v,target_position,label)

#     return target_position

# time_v=np.arange(0,60,0.1)
# f=np.zeros(len(time_v))
# for i in range(len(time_v)):
#     f[i]=trajectory_2(time_v[i])


# plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
# plt.grid(True)
# plt.plot(time_v,f,'r',linewidth=2.0)
# plt.show()




data=pd.read_csv("/home/valeria/TSA_stuff/TSA_lin_stand/data_stand_1.csv",header=None,sep=";")
data=data.to_numpy()

time=data[:,0]
target_pos=data[:,1]
real_pos=data[:,4]
ee_pos=data[:,5]

# pos=real_pos
# turns=pos*0
# turn=0
# for i in range(1,len(pos)):
#     if math.fabs(pos[i]-pos[i-1])>50:
#         if pos[i]-pos[i-1]<0:
#             turn+=1
#         else:
#             turn-=1
#     turns[i]=turn

plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
plt.grid(True)
plt.plot(time,target_pos,'b',linewidth=2.0)
plt.plot(time,real_pos,'r',linewidth=2.0)
plt.show()

# # shift=1
# # n=len(time)
# # plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
# # plt.grid(True)
# # plt.plot(time[0:n-shift],target_pos[0:n-shift],'b',linewidth=2.0)
# # plt.plot(time[0:n-shift],real_pos[shift:n],'k',linestyle='dashed',linewidth=2.0)
# # plt.plot(time[0:n-shift],real_pos[shift:n]-target_pos[0:n-shift],'r',linewidth=2.0)
# # plt.show()

# plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
# plt.grid(True)
# plt.plot(time,ee_pos,'r',linewidth=2.0)
# plt.show()