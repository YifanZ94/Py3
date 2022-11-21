clear; clc
data1 = load('ss_acc.txt');
data2 = load('ss_locs.txt');
data3 = load('ss_mag.txt');
x = linspace(0,20,size(data1,1));
magn = sqrt(data1(:,1).^2 + data1(:,2).^2+ data1(:,3).^2);
plot(x,data1,x,magn,'--')
legend('ax','ay','az','magnitude')
xlabel('time(s)')
ylabel('acc (m/S^2)')
title('accleration')

%%
accX = data1(:,1);
accY = data1(:,2);
accZ = data1(:,3);
Ax = atan(-accY./accZ)/pi*180;
Ay = -atan(-accX./sqrt(accY.^2+ accZ.^2))/pi*180;

% for i = 1:size(Ax,1)
%     Rx = [1,0,0; 0,cos(Ax),-sin(Ax);0,sin(Ax),cos(Ax)];
%     Ry = [cos(Ay),0,sin(Ay); 0,1,0; -sin(Ay),0,cos(Ay)];
% end
%%
figure
x2 = linspace(0,20,size(data2,1));
plot(x2,data2)
legend('x','y','z')
xlabel('time(s)')
ylabel('location(cm)')
title('location')