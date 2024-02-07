clear; clc
data1 = load('test.txt');
x = 1:20;
plot(x,data1)
legend('X raw','Y raw','Z raw','X rotated','Y rotated','Z rotated')