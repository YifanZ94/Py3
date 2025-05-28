clear; clc;
data = load('motor_30.txt');  % acc x,y,z gyro x,y,z

%%
% plot(data(:,1:3))
% legend('aX','aY','aZ')
% figure
% plot(data(:,4:6))
% legend('wX','wY','wZ')
%%
L = size(data,1);

% T = 19.74;
% Fs = L/T;

Fs = 50;

Ts = 1/Fs;
t = (0:L)/Fs;

%%  FFT
X = data(:,1);
Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:floor(L/2)+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')
hold on
%%  bandpass
band_cut = [7 10];
Y_LP = bandpass(X,band_cut,Fs);
figure
bandpass(X,band_cut,Fs)

%% acc/double integral
Y_int = cumtrapz(Ts,cumtrapz(Ts,Y_LP));
figure
plot(t(2:end),Y_int)
hold on
Y_raw = cumtrapz(Ts,cumtrapz(Ts, X));
plot(t(2:end),Y_raw)
legend('low pass filtered','raw data')
xlabel('time(s)')
ylabel('displacement(m)')