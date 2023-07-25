import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt
from Calculate import Dax_correlation, Experimental_Data
import numpy as np

#Datos experimentales
var = Experimental_Data('E8')
vardx = 800
t_data = var[0]
x_data = var[1]
vars = var[2]
L = vars[2]/100

# Gekko feed
m = GEKKO()
m.time = t_data

#Discretization
tf = t_data[-1]
npt = 100    
npx = 20
time = np.linspace(0,tf,npt)
xpos = np.linspace(0,L,npx)

#Constant assignment
dx = m.Const(value = xpos[1]-xpos[0])
uxn = m.Const(value = 0)
C0i = m.Const(value = vars[1])
rho = m.Const(value = 1550)
eps = m.Const(value = 0.13)
v =  m.Const(value = vars[0]/60)

################################### Control Segment ###################################
#Manipulated variable
kf = m.MV(value=3.57E-09, ub=5.77E-09, lb=2.31E-10)    #Large > Short

Dax_Var = Dax_correlation(vars[0])
Dal = m.Const(value = Dax_Var[0])

# Reference trajectory
traj = m.Param(value=x_data)

#Initial value to EDO
x0 =  np.zeros(npx) 

# Controlled Variable
LV = m.SV(value=0,name='LV')

# Error
e = m.CV(value=0,name='e')

################################### Solve Equations ###################################
# Initial values
q =    [m.Var(value = x0[i]) for i in range(npx)]
C =    [m.Var(value = x0[i]) for i in range(npx)]

#EDO Adorption 
m.Equations([q[i].dt() == -kf*(q[i]-(396*C[i]/(1+2*C[i]))) for i in range(npx)])

#EDO Column 
# first segment
m.Equation(C[0].dt() == \
             -v*(-25*C[0]+48*C[1]-36*C[2]+16*C[3]-3*C[4])/(12*dx)/vardx\
               +Dal*((-7*C[0]+8*C[1]-C[2])/(2*dx**2)-6*(-v/Dal*(C0i-C[0]))/(2*dx)) \
              -(rho/eps)*q[0].dt())

# middle segments
m.Equations([C[i].dt() == \
               -v*(C[i+1]-C[i-1])/(2*dx)/vardx \
             +Dal*(C[i+1]-2*C[i]+C[i-1])/(dx**2) \
             -(rho/eps)*q[i].dt() for i in range(1,npx-1)])

# last segment
m.Equation(C[npx-1].dt() == \
             -v*(3*C[npx-5]-16*C[npx-4]+36*C[npx-3]-48*C[npx-2]+25*C[npx-1])/(12*dx)/vardx+Dal*((-7*C[npx-1]+8*C[npx-2]-C[npx-3])/(2*dx**2) \
            +6*uxn/(2*dx))-(rho/eps)*q[npx-1].dt())

m.Equation(LV == C[npx-1])
m.Equation(e==LV-traj)


################################### Tuning segment ###################################
m.options.IMODE = 6 # control
e.STATUS = 1 #add the CV to the objective
m.options.CV_TYPE = 1 #Dead-band
m.options.MAX_ITER = 1000
e.SPHI = 1 #set point
e.SPLO = -1 #set point
e.TR_INIT = 0 #setpoint trajectory

#MV tuning
kf.STATUS = 1 #allow optimizer to change
kf.DCOST = 1e-16 #smooth out gas pedal movement
kf.DMAX = 0.1e-16 #slow down change of gas pedal


################################### System solve ###################################
m.solve()

import json
with open(m.path+'//results.json') as f:
    results = json.load(f)

np.savetxt("firstarray.csv", [t_data, x_data, LV.value, kf.value], delimiter=",")
################################### Plot Solution ###################################
plt.figure()
plt.title('Adjustment by Machine Learning')

plt.subplot(3,1,1)
plt.plot(m.time,kf.value,'b-',lw=2,label='Velocity trajectory')
plt.legend(loc='best')
plt.ylabel('MV')

plt.subplot(3,1,2)
plt.plot(m.time,x_data,'rx',label='Experimental data')
plt.plot(m.time,LV.value,'b--',lw=2,label='Predictive Model')
plt.legend(loc='best')
plt.ylabel('CV')

plt.subplot(3,1,3)
plt.plot(m.time,results['e.tr_hi'],'k-',label='SPHI')
plt.plot(m.time,results['e.tr_lo'],'k-',label='SPLO')
plt.plot(m.time,e.value,'r--',lw=2,label='Error')
plt.legend(loc=2)
plt.ylabel('Error')

plt.xlabel('time')
plt.show()