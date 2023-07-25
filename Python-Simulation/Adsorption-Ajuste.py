import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt
from Calculate import Dax_correlation, Experimental_Data
import numpy as np

#Datos experimentales
var = Experimental_Data('E1') #"e2,"
vardx = 800
t_data = var[0]
x_data = var[1]
vars = var[2]
L = vars[2]/100

#ingresamos a gekko x & y
m = GEKKO(remote=False)
m.time = t_data

# Discretización del tiempo y espacio con n nodos
tf = t_data[-1]
npt = 100    
npx = 20
time = np.linspace(0,tf,npt)
xpos = np.linspace(0,L,npx)

# Especificación de constantes a gekko
dx = m.Const(value = xpos[1]-xpos[0])
v = m.Const(value = vars[0]/60)
Dax_Var = Dax_correlation(vars[0])
Dal = m.Const(value = Dax_Var[0])
uxn = m.Const(value = 0)
C0i = m.Const(value = vars[1])
rho = m.Const(value = 1550)
eps = m.Const(value = 0.13)

#Variable ajustada
kf = m.FV(); kf.STATUS = 1 # adjustable parameter


kf.LOWER = 1.0996520354e-14
kf.UPPER = 10e-7
kf.DMAX = 3.654e-7

################################### Ecuaciones a resolver ###################################
#Valores iniciales de la EDO
x0 =  np.zeros(npx) 

# Especificación de constantes a gekko
q =    [m.Var(value = x0[i]) for i in range(npx)]
C =    [m.Var(value = x0[i]) for i in range(npx)]

# Variable to match with data
LV = m.CV(value=npx-1)

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

#Final node estimation
m.Equation(LV == C[npx-1])

#Instrcciones para resolver
m.options.IMODE = 8   # dynamic estimation
m.options.NODES = 5   # collocation nodes
m.options.TIME_SHIFT = 0 #don't timeshift on new solve
m.options.EV_TYPE = 2 #least squares
m.options.COLDSTART = 2
m.options.SOLVER = 1
m.options.MAX_ITER = 1000

m.solve(disp=False)   # display solver output

LV.FSTATUS = 1 #receive measurements to fit
LV.STATUS = 1 #build objective function to match data and prediction
LV.value = x_data # data

m.solve()
kf = kf.value[0]
print('el valor estimado de Dal es: ',Dax_Var[0])
print('el valor estimado de kf es: ',kf)


np.savetxt("firstarray.csv", [t_data, x_data, C[-1].value], delimiter=",")

# Plot results
import matplotlib.pyplot as plt
plt.figure(1)
plt.plot(t_data,C[-1].value,'k--', label='Ajuste')
plt.plot(t_data,x_data,'rx', label='Datos experimentales')
plt.xlabel('Tiempo [S] ')
plt.ylabel('Concentración [mg/L]')
plt.legend(loc=4)
plt.show()