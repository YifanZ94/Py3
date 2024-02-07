clear; clc
strain_gauge = load('F_test1_slow_30cm.txt');
strain_gauge(:,2) = strain_gauge(:,2) - mean(strain_gauge(1:200,2));

strain_gauge_calib = load('F_static_calib.txt');
mass_bias = mean(strain_gauge_calib(875:1360,2));
m = mass_bias/6e-2;

IMU = load('test1_acc.txt');
IMU_bias = mean(IMU(50:100,:));
g = IMU_bias(1);
% g = 9.81;
IMU_mean_removed = IMU(:,1) - IMU_bias(1);

F = strain_gauge(:,2)*g/6e-2;
a_F = F/m - g;
%%
figure
subplot(211)
plot(F)
title('F(N)')
subplot(212)
plot(IMU_mean_removed)
title('acc')

%%
X1 = 710:910;
X2 = 655:798;
subplot(211)
F_net = F(X1)-m*g;
plot(F_net)
xlabel('sampling')
ylabel('F(N)')
subplot(212)
aX = resample(IMU_mean_removed(X2),size(X1,2),size(X2,2));
plot(aX)
xlabel('sampling')
ylabel('acc(m/s2)')

%%  FFT
X = IMU_mean_removed;
L = size(X,1);

n = 2^nextpow2(L);   % zeros padding

Y = fft(X,n);

Ts = 0.011;
Fs = 1/Ts;
P2 = abs(Y/L);
P1 = P2(1:floor(L/2)+1,:);
P1(2:end-1,:) = 2*P1(2:end-1,:);
f = Fs*(0:(L/2))/L;
plot(f,P1)
% legend('x','y','z')
title('Single-Sided Amplitude Spectrum')
% ylim([0 0.2])
xlabel('f (Hz)')
ylabel('|P1(f)|')

%%  systemIdentification
% figure
% plot(mydatad.u)
% hold on
% plot(F_net - mean(F_net))

%% double integration
Ts = 0.011;
displacement_a = cumtrapz(Ts, cumtrapz(Ts, aX));
displacement_F = cumtrapz(Ts, cumtrapz(Ts, (F_net - 0.31)/m));
figure
plot(displacement_a)
hold on
plot(displacement_F)
% hold on
% plot(displacement_filtered)
legend('acc','F/m')
xlabel('sample')
ylabel('displacement(m)')
