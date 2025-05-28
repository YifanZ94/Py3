clear; clc
data1 = load('origin_acc.txt');
data2 = load('origin_3in1.txt');
M1 = mean(data1,1);
M2 = mean(data2,1);
%%
data3 = load('X+90_acc.txt');
data4 = load('X+90_3in1.txt');
M3 = mean(data3,1);
M4 = mean(data4,1);
%%
data5 = load('000_acc.txt');
data6 = load('000_3in1.txt');
M5 = mean(data5,1);
M6 = mean(data6,1);
%%
data7 = load('Y+90_acc.txt');
data8 = load('Y+90_3in1.txt');
M7 = mean(data7,1);
M8 = mean(data8,1);