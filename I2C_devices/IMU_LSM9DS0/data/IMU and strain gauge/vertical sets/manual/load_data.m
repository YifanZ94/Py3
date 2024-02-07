clear; clc
strain_gauge_calib = load('static_calib.txt');
mass_bias = mean(strain_gauge_calib(320:557,2));
m = mass_bias/6e-2;
% m = 0.28;

strain_gauge = load('F_test1.txt');
strain_gauge(:,2) = strain_gauge(:,2) - mean(strain_gauge(1:200,2));

IMU = load('test1_acc.txt');
IMU_bias = mean(IMU(60:175,:));
g = IMU_bias(1);
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
X1 = 1389:1721;
X2 = 691:919;   % test 2

subplot(211)
F_net = F(X1)-m*g;
plot(F_net)
title('F(N)')
subplot(212)
aX = resample(IMU_mean_removed(X2),size(X1,2),size(X2,2));
plot(aX)
title('acc(m/s2)')
%  systemIdentification
% plot(mydatad.u)
%% double integration
Ts = 0.011;
displacement_a = cumtrapz(Ts, cumtrapz(Ts, aX));
displacement_F = cumtrapz(Ts, cumtrapz(Ts, (F_net)/m +1.5));
% displacement_F = cumtrapz(Ts, cumtrapz(Ts, (mydatad.u)/m));
figure
plot(displacement_a)
hold on
plot(displacement_F)
% hold on
% plot(displacement_filtered)
legend('acc','F/m')
xlabel('sample')
ylabel('displacement(m)')
