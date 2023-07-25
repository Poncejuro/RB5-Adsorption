import pickle
import matplotlib.pyplot as plt
import numpy as np
from gekko import GEKKO
from Calculate import Dax_correlation, Experimental_Data

#Datos experimentales
var = Experimental_Data('E2')
vardx = 800
T_ex = var[0]
C_ex = var[1]
vars = var[2]
L = vars[2]/100

# Discretización del tiempo y espacio con n nodos
tf = T_ex[-1]
npt = 100    
npx = 20
time = np.linspace(0,tf,npt)
xpos = np.linspace(0,L,npx)

# Especificación del tiempo a gekko
m = GEKKO()
m.time = time

# Especificación de constantes a gekko
dx = m.Const(value = xpos[1]-xpos[0])
v = m.Const(value = vars[0]/60)
kf = m.Const(value = 4.10E-9)  #3.65E-09
Dax_Var = Dax_correlation(vars[0])
Dal = m.Const(value = Dax_Var[0])
uxn = m.Const(value = 0)
C0i = m.Const(value = vars[1])
rho = m.Const(value = 1550)
eps = m.Const(value = 0.14)

#Valores iniciales de la EDO
x0 =  np.zeros(npx) 

# Especificación de constantes a gekko
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

# simulation
m.options.imode = 7 #4
m.options.solver = 1
m.options.nodes = 5
m.solve()

#Save data

# plot results
plt.figure()
plt.plot(T_ex,C_ex,'rx', label='$Experimental$')
plt.plot(m.time,C[-1].value,'k--', label='$Simulation$')
plt.ylabel('$Concentration$')
plt.xlabel('Time (min)')
plt.legend(loc=4)
plt.show()
L = vars[2]/100
