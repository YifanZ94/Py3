clear; clc;
data = load('manual_17.83s.txt');  % acc x,y,z gyro x,y,z

%%
% plot(data(:,1:3))
% legend('aX','aY','aZ')
% figure
% plot(data(:,4:6))
% legend('wX','wY','wZ')
%%
L = size(data,1);

T = 17.83;
Fs = L/T;

% Fs = 50;

Ts = 1/Fs;
t = (0:L)/Fs;

%%  FFT
X = data(:,1);    % angular (4:6)
Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:floor(L/2)+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum')
xlabel('f (Hz)')
ylabel('|P1(f)|')

%%  lowpass
% f_cut = 5;
% Y_LP = lowpass(X,f_cut,Fs);
% figure
% lowpass(X,f_cut,Fs)

%%  bandpass
band_cut = [3 100];
Y_LP = bandpass(X,band_cut,Fs);
figure
bandpass(X,band_cut,Fs)

%% angular/single integral
% Y_int = cumtrapz(Ts,Y_LP);
% figure
% plot(t(2:end),Y_int)
% hold on
% Y_raw = cumtrapz(Ts, X);
% plot(t(2:end),Y_raw)
% legend('filtered','raw data')
% xlabel('time(s)')
% ylabel('angle(rads)')

%% acc/double integral
Y_int = cumtrapz(Ts,cumtrapz(Ts,Y_LP));
figure
plot(t(2:end),Y_int)
hold on
Y_raw = cumtrapz(Ts,cumtrapz(Ts, X));
plot(t(2:end),Y_raw)
legend('filtered','raw data')
xlabel('time(s)')
ylabel('displacement(m)')