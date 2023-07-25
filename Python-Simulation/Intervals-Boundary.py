import numpy as np
from scipy . optimize import curve_fit
import pylab as plt
from scipy.integrate import odeint
from lmfit import Model
from Calculate import Dax_correlation, Experimental_Data

#Datos experimentales
var = Experimental_Data('E9') #'Hoja6','2','56'    #'Hoja4','2','68'   #'Hoja1','2','65'
vardx = 800
t_data = var[0]
x_data = var[1]
vars = var[2]
L = vars[2]/100

npx = 20
xpos = np.linspace(0,L,npx)
# Asignación de constantes
dx = xpos[1]-xpos[0]

def modelo(Z,t,kf,Dal):
    #q , C = Z
    npx = 20
    q = Z[0:npx]
    C = Z[npx:2*npx]
    
    dCdt = np.empty(npx)
    dqdt = np.empty(npx)
    f = np.empty(2*npx)
    v = vars[0]/60
    #Dal = 1.67e-4
    uxn = 0
    C0i = vars[1]   
    rho = 1550
    eps = 0.13
    
    #EDO Adorption 
    for i in range(0, npx):
        dqdt[i]= -kf*(q[i]-(396*C[i]/(1+2*C[i]))) 

    dCdt[0]= \
             -v*(-25*C[0]+48*C[1]-36*C[2]+16*C[3]-3*C[4])/(12*dx)/vardx\
               +Dal*((-7*C[0]+8*C[1]-C[2])/(2*dx**2)-6*(-v/Dal*(C0i-C[0]))/(2*dx)) \
              -(rho/eps)*dqdt[0]
    # middle segments
    for i in range(1, npx-1):
        dCdt[i] = \
               -v*(C[i+1]-C[i-1])/(2*dx)/vardx \
             +Dal*(C[i+1]-2*C[i]+C[i-1])/(dx**2) \
             -(rho/eps)*dqdt[i]    
    
    dCdt[npx-1]= \
             -v*(3*C[npx-5]-16*C[npx-4]+36*C[npx-3]-48*C[npx-2]+25*C[npx-1])/(12*dx)/vardx+Dal*((-7*C[npx-1]+8*C[npx-2]-C[npx-3])/(2*dx**2) \
            +6*uxn/(2*dx))-(rho/eps)*dqdt[npx-1]
    f[0:npx]= dqdt
    f[npx:2*npx] =dCdt
    return f

def f1(x, kf, Dal):
    npx = 20
    t = x
    IC = np.zeros(2*npx)

    
    Cas=odeint(modelo,IC,t, args= (kf,Dal) )
    
    
    return Cas[:,2*npx-1]

# data 
x =np.array(t_data)

yi = np.array(x_data)


# call curve fit function to get the best values of kf
kfi = 3.65E-09 #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
daxi = 6.216092117823004e-08
init_vals = [kfi, daxi]
popt1, pcov1 = curve_fit(f1, x, yi, p0=init_vals,bounds=([kfi*.99, daxi*.99], [kfi*1.01, daxi*1.01]))#


k1,k2 = popt1
full_output = 1
print (" Optimal parameter are kf=%g, Dal=%g" % (k1,  k2))



# plotting
yfitted1 = f1(x, * popt1 ) # equivalent to f(x, popt [0] , popt [1] , popt [2])

np.savetxt("firstarray.csv", [x, yi, yfitted1], delimiter=",")

plt . plot (x, yi , 'o', label ='data $y_i$ ')
plt . plot (x, yfitted1 , '*', label ='fit $f(x_i)$')
plt . xlabel ('time')
plt . legend ()
plt . show ()
modelPredictions = f1(x, * popt1 ) 

absError = modelPredictions - yi

SE = np.square(absError) # squared errors
MSE = np.mean(SE) # mean squared errors
RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
Rsquared = 1.0 - (np.var(absError) / np.var(yi))
#print(SE)
#print('squared errors: ',SE)
print('mean squared errors: ',MSE)
print('Root Mean Squared Error: ',RMSE)
print('Rsquared: ',Rsquared)
gmodel1 = Model(f1)
result1 = gmodel1.fit(yi, x=x, kf=kfi, Dal=daxi)
print(result1.fit_report())





TIC = (sum(absError**2))**0.5/((sum([n**2 for n in yi]))**0.5 + (sum([n**2 for n in yfitted1]))**0.5)
print(TIC)