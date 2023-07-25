clear all
clc

u(1)=0.0153;
u(2)=97.385;

Cb_0=linspace(0,0,20);
q_0=linspace(0,0,20);
x=[Cb_0, q_0];
 
[A,B,C,D] = linmod('sistemap',x,u); % linearizacion
[numv,denv] = ss2tf (A,B,C,D,1);
[numC,denC] = ss2tf (A,B,C,D,2);
Gp = tf(numv,denv);

load('RedMod.mat','AR','BR','CR','DR');
[numvR,denvR] = ss2tf (AR,BR,CR,DR,1);
%load('SST.mat','ts','c0');


% figure(1)
% plot(DataSS.Time,DataSS.Data,ts,c0,'x')
% title('Comparación')
% xlabel('Time [m]')
% ylabel('C [mg/L]')
