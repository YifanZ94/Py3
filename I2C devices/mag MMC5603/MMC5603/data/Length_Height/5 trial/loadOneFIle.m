x1 = 0:10;
x2 = 10.1:0.1:20;
x3 = 21:30;

dataE = load(sprintf('MMC_H15_F20_1_env.txt'));
dataM = load(sprintf('MMC_H15_F20_1_mag.txt'));
dataM(2,:) = dataM(3,:);
dataM(1,:) = dataM(3,:);
dataE(1,:) = dataE(2,:);
net = dataM - dataE;
amp = sqrt(net(:,1).^2 + net(:,2).^2 + net(:,3).^2);

plot(x1,net(1:11,1),x2,net(12:111,1),x3,net(112:end,1))
figure
plot(x1,net(1:11,2),x2,net(12:111,2),x3,net(112:end,2))
figure
plot(x1,net(1:11,3),x2,net(12:111,3),x3,net(112:end,3))
figure
plot(x1,amp(1:11),x2,amp(12:111),x3,amp(112:end))