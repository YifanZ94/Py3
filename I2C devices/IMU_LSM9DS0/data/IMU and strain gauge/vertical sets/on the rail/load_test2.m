clear; clc
strain_gauge = load('F_test2_fast_30cm.txt');
strain_gauge(:,2) = strain_gauge(:,2) - mean(strain_gauge(1:200,2));

strain_gauge_calib = load('F_static_calib.txt');
mass_bias = mean(strain_gauge_calib(875:1360,2));
m = mass_bias/6e-2;

IMU = load('test2_acc.txt');
IMU_bias = mean(IMU(47:117,:));
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

X1 = 878:1037;
X2 = 463:576;  

%%
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

%%  systemIdentification  %% to remove means
subplot(211)
plot(means_removed.u)
xlabel('sampling')
ylabel('F(N)')
subplot(212)
aX = resample(IMU_mean_removed(X2),size(X1,2),size(X2,2));
plot(aX)
xlabel('sampling')
ylabel('acc(m/s2)')

%% double integration
Ts = 0.011;
displacement_a = cumtrapz(Ts, cumtrapz(Ts, aX));
displacement_F = cumtrapz(Ts, cumtrapz(Ts, means_removed.u/m));
% displacement_filtered = cumtrapz(Ts, -cumtrapz(Ts, out_filtered));
figure
plot(displacement_a)
hold on
plot(displacement_F)
% hold on
% plot(displacement_filtered)
legend('acc','F/m')
xlabel('sample')
ylabel('displacement(m)')
