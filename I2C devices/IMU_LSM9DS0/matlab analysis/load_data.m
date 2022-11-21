clear; clc;
% ave = load('test1_ave.txt');
raw = load('static_y_up_raw.txt');
%%
% acc_bias1 = mean(ave(:,1:3));
% acc_bias2 = [(ave(1,3)+ave(2,3))/2, (ave(3,2)+ave(4,2))/2, (ave(5,1)+ave(6,1))/2];

acc_bias = mean(raw(:,1:3));
gyro_bias = mean(raw(:,4:6));