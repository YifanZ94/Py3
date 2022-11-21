clear; clc
H = [15,20,25];
F = [30,35,40];
des = zeros(3,3);
std = 0.006;

for i = 1:3
    for j = 1:3
        dataE = load(sprintf('MMC_H%d_f%d_mag.txt',H(i),F(j)));
        dataM = load(sprintf('MMC_H%d_f%d_env.txt',H(i),F(j)));
        dataM(1,:) = dataM(2,:);
        net = dataE(:,3) - dataM(:,3);
        des(i,j) = find(net<0,1);
        desPost(i,j) = net(des(i,j));
        desPri(i,j) = net(des(i,j)-1);
        error(i,j) = abs(desPost(i,j))/(desPost(i,j)-desPri(i,j))*5/2;
        
        upper(i,j) = find(net<std,1);
        lower(i,j) = find(net<-std,1);
    end
end

%% 
data1 = load('MMC_H15_f40_env.txt');
data1(1,:) = data1(2,:);
data10 = load('MMC_H15_f40_mag.txt');
x1 = 0.5*(1:80);
net1 = data1(:,3)-data10(:,3)-0.005;
plot(x1-5,net1,'b',x1-5,net1+std,'g--',x1-5,net1-std,'g--')
xlim([-5 25]);
xlabel('distance(cm)')
ylabel('magnetic field density(gauss)')

hold on

data2 = load('MMC_H25_f40_env.txt');
data2(1,:) = data2(2,:);
data20 = load('MMC_H25_f40_mag.txt');
x2 = 0.5*(1:80);
net2 = data2(:,3)-data20(:,3)-0.005;
plot(x2-5,net2,'r',x2-5,net2+std,'g--',x2-5,net2-std,'g--')
xlim([-5 35]);
ylim([-0.2 0.2])
xlabel('distance(cm)')
ylabel('magnetic field density(gauss)')

plot([-5 17], [0 0],'--')