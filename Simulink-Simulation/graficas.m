figure(1)
plot(PID_zigler.Time,PID_zigler.Data)
title('Respuesta del sistema')
xlabel('Tiempo [min]')
ylabel('Concentración [mg/L]')
legend('Respuesta del controlador','Sistema estable')
grid on

% figure(1)
% plot(Perturb.Time,Perturb.Data)
% xlabel('Tiempo [min]')
% ylabel('Concentración [mg/L]')
% legend('Concentarción de alimentación')
% grid on
% 
% figure(1)
% plot(PID_comparation.Time,PID_comparation.Data)
% title('Comparación entre controladores')
% ylabel('v [m/min]')
% xlabel('Tiempo [min]')
% legend('P','PI','Cambio escalón','PID')
% grid on
% 
% figure(2)
% plot(Report_signal.Time,Report_signal.Data*100)
% title('Comportamiento de la variable manipulada')
% xlabel('Tiempo [min]')
% ylabel('v [m/min]')
% grid on

%  figure(1)
% plot(Oscilacion.Time,Oscilacion.Data)
% title('Oscilación')
% xlabel('Time [m]')
% ylabel('v [m/min]')
% grid on

% plot(PID_zigler.Time,PID_zigler.Data)
% title('Respuesta del sistema')
% xlabel('Tiempo [min]')
% ylabel('Concentración [mg/L]')
% legend('Respuesta del controlador','Sistema estable')
% grid on

figure(2)
plot(Comp_entre_pc.Time,Comp_entre_pc.Data)
title('Respuesta del sistema')
xlabel('Tiempo [min]')
ylabel('Concentración [mg/L]')
legend('Sintonización por Ziegler-Nichols',...
    'Sistema estable','Sintonización asistida')
grid on

% yh=y_hum.Data;
% ypc=y_pc.Data;
% 
% RMSE1=sum((yh-y).^2)/length(y)
% RMSE1=sum((ypc-y).^2)/length(y)
% 
% num1=(sum((yh-y).^2)).^0.5;
% den1=(sum(yh.^2)).^0.5 + (sum(y.^2)).^0.5;
% TIC1=num1/den1
% 
% num2=(sum((ypc-y).^2)).^0.5;
% den2=(sum(ypc.^2)).^0.5 + (sum(y.^2)).^0.5;
% TIC2=num2/den2

% %Properties
% Dff=[5e-14 6.e-16 2.7e-8];
% rho=1000; 
% eps=0.13;
% mu=0.000891;
% As=50000;  %https://sci-hub.se/https://doi.org/10.1002/jccs.200200096
% U=0.055;
% 
% %Surface Area
% d=4*eps/(As*(1-eps));  %https://sci-hub.se/https://doi.org/10.1016/0923-0467(96)03073-4
% 
% %Axial dispersion
% Re=d*U*rho/mu/eps;   %10^-3 < Re < 10^3
% Sc=mu./Dff/rho;
% var=0.72./Re./Sc + 0.52./(1+0.9./Re./Sc);
% Pe=1./var;
% DL=2*U*(d/2)./Pe