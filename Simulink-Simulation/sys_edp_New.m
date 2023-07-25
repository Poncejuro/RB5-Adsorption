function [sys,x0] = sys_edp_New (~,y,u,flag)
if flag == 0
ns = 40; % numero de estados
ni = 2; % numero de entradas
no = 1; % numero de salidas
sys = [ns 0 no ni 0 0]; % dimension del problema

Cb_0=linspace(0,0,20);
q_0=linspace(0,0,20);
x0=[Cb_0, q_0];

end
if flag == 1 % modelo dinamico
  
    
%Entradas

    U0=u(1);

%Constantes
    Dax=9.531341159968593e-08; %m2/s
    kf=8.7828888154e-10;  %1/s 
    
%     U0=2.55e-4; %m/s
    Cb0=u(2); %97.385;      %mg/L RB5
    L=0.028;  %m
    eps=0.14;   
    rho=1550;     %g/L
    n=20;
    

%Variables 
    Cb=y(1:n);  
    q=y(n+1:2*n);

%Estimación de las derivadas
    dCbdx=dss020(0,L,n,Cb,1);
    dCbdx(1)=-U0*(Cb0-Cb(1))/Dax;
    dCbdx(n)=0;
    d2Cbdx2=dss042(0,L,n,Cb,dCbdx,2,2);

%Ecuaciones auxiliares
    a=2;
    k=396;
    b=1;
    qads=k.*Cb./(1+a.*Cb.^b);

%EDP
    dqdt=-kf*(q-qads);
    dcdt= Dax.*d2Cbdx2'-U0.*dCbdx'/700-(rho/eps).*dqdt;
      
sys=[dcdt;dqdt];
end
if flag == 3  
sys = [y(20)]; % salida del sistema
end
if flag ==9
    sys=[];
end