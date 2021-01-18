
dataE = load(sprintf('MMC_new_env.txt'));
dataM = load(sprintf('MMC_new_mag.txt'));
dataM(2,:) = dataM(3,:);
dataM(1,:) = dataM(3,:);
dataE(1,:) = dataE(2,:);
net = dataM - dataE;

dataE2 = load(sprintf('MMC_old_env.txt'));
dataM2 = load(sprintf('MMC_old_mag.txt'));
dataM2(2,:) = dataM2(3,:);
dataM2(1,:) = dataM2(3,:);
dataE2(1,:) = dataE2(2,:);
net2 = dataM2 - dataE2;

amp = sqrt(net(:,1).^2 + net(:,2).^2 + net(:,3).^2);

x = 1:40;
plot(x,net(1:40,3),x,net2(1:40,3))

subplot(221)
plot(x,net(1:40,1))
title('x axis')
subplot(222)
plot(x,net(1:40,2))
title('y axis')
subplot(223)
plot(x,net(1:40,3))
title('z axis')
subplot(224)
plot(x,amp(1:40))
title('magnitude')