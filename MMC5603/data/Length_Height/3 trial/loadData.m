clear; clc
H = [15,20,25];
T = [1,2,3];
F = [30,35,40];
des = zeros(3,3);
std = 0.002;

x1 = 0:15;
x2 = 15.1:0.1:24.9;
x3 = 25:40;

for i = 1:3

    for j = 1:3
        figure
        dataE = load(sprintf('MMC_H%d_F30_%d_mag.txt',H(i),T(j)));
        dataM = load(sprintf('MMC_H%d_F30_%d_env.txt',H(i),T(j)));
        dataM(2,:) = dataM(3,:)+0.005;
        dataM(1,:) = dataM(3,:)+0.005;
        dataE(1,:) = dataE(2,:);
        net =  dataM(:,3)- dataE(:,3)-0.02';
%         hold on
        plot(x1,net(1:16),x2,net(17:115),x3,net(116:end))
        hold on
        plot([10 20],[0,0],'--b')
%         plot(x2,net(17:116))
        des(i,j) = find(net>0,1);
        xlim([10 30])
        xlabel('distance(cm)')
        ylabel('magnetic field density(gauss)')
    end
end