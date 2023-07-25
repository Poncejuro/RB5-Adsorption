import pickle
import matplotlib.pyplot as plt
from Calculate import Dax_correlation

"""
with open("Data_Adjustment1.pickle", "rb") as f:
    obj1 = pickle.load(f)
t_data1 = obj1[0]
C_sim1 = obj1[1]
C_data1 = obj1[3]

with open("Data_Adjustment2.pickle", "rb") as f:
    obj2 = pickle.load(f)
t_data2 = obj2[0]
C_sim2 = obj2[1]
C_data2 = obj2[3]

with open("Data_Adjustment3.pickle", "rb") as f:
    obj3 = pickle.load(f)
t_data3 = obj3[0]
C_sim3 = obj3[1]
C_data3 = obj3[3]



plt.figure(1)
plt.plot(t_data1,C_sim1,'k', label='$S1')
plt.plot(t_data1,C_data1,'kx', label='$D1')

plt.plot(t_data2,C_sim2,'r', label='$S2')
plt.plot(t_data2,C_data2,'rx', label='$D2')

plt.plot(t_data3,C_sim3,'b', label='$S3')
plt.plot(t_data3,C_data3,'bx', label='$D3')

plt.title("Datos experimentales vs Ajustes")
plt.ylabel('Concentration [mg/L]')
plt.xlabel('Time [s]')
plt.legend(loc=4)
plt.show()
"""
##########################################################################################################
"""
with open("Velocity_profile1.pickle", "rb") as f:
    obj1 = pickle.load(f)
time1 = obj1[0]
vp1 = obj1[1]
C_sim1 = obj1[2]
x_data1 = obj1[3]

with open("Velocity_profile2.pickle", "rb") as f:
    obj2 = pickle.load(f)
time2 = obj2[0]
vp2 = obj2[1]
C_sim2 = obj2[2]
x_data2 = obj2[3]

with open("Velocity_profile3.pickle", "rb") as f:
    obj3 = pickle.load(f)
time3 = obj3[0]
vp3 = obj3[1]
C_sim3 = obj3[2]
x_data3 = obj3[3]


plt.figure(1)
plt.subplot(2,1,1)
plt.plot(time1,vp1,'k', label='Trayectoria 1')
plt.plot(time2,vp2,'r', label='Trayectoria 2')
plt.plot(time3,vp3,'b', label='Trayectoria 3')
plt.legend(loc='best')
plt.ylabel('Velocidad [m/s]')
plt.title("Perfiles de velocidad")

plt.subplot(2,1,2)
plt.plot(time1,C_sim1,'k-', label='S1')
plt.plot(time1,x_data1,'kx', label='D1')
plt.plot(time2,C_sim2,'r-', label='S2')
plt.plot(time2,x_data2,'rx', label='D2')
plt.plot(time3,C_sim3,'b-', label='S3')
plt.plot(time3,x_data3,'bx', label='D3')
plt.legend(loc='best')
plt.ylabel('Concentración [mg/L]')
plt.title("Datos experimentales vs Ajustes")

plt.xlabel('Time [s]')
plt.legend(loc=4)
plt.show()
"""

#########################################################################################################
with open("Velocity_profile1.pickle", "rb") as f:
    obj1 = pickle.load(f)
time1 = obj1[0]
vp1 = obj1[1]



with open("Velocity_profile2.pickle", "rb") as f:
    obj2 = pickle.load(f)
time2 = obj2[0]
vp2 = obj2[1]


with open("Velocity_profile3.pickle", "rb") as f:
    obj3 = pickle.load(f)
time3 = obj3[0]
vp3 = obj3[1]

p1 = []
for i in vp1:
  p1.append(i/vp1[0])

p2 = []
for i in vp2:
  p2.append(i/vp2[0])

p3 = []
for i in vp3:
  p3.append(i/vp3[0])


plt.figure(1)
plt.plot(time1,p1,'k', label='Trayectoria 1')
plt.plot(time2,p2,'r', label='Trayectoria 2')
plt.plot(time3,p3,'b', label='Trayectoria 3')
plt.legend(loc='best')
plt.ylabel('Velocidad [m/s]')
plt.title("Perfiles de velocidad")


plt.xlabel('Time [s]')
plt.legend(loc=4)
plt.show()