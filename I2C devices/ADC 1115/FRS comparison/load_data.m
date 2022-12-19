clear; clc
data = load('slight_press2.txt');
X1 = 220:1230;
ref_in_gram = data(X1,3)/1.2;

FSR = load('slight_press2_force.txt');
X2 = 66:215;
FSR = resample(FSR(X2),size(X1,2),size(X2,2));

%%
subplot(211)
plot(ref_in_gram)
subplot(212)
plot(FSR)

%%
figure
Range = 534:690;
plot(ref_in_gram(Range)./FSR(Range))