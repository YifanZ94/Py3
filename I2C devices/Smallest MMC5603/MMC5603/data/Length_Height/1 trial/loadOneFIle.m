
dataE = load(sprintf('MMC_H15_f40_env.txt'));
dataM = load(sprintf('MMC_H15_f40_mag.txt'));
dataM(2,:) = dataM(3,:);
dataM(1,:) = dataM(3,:);
dataE(1,:) = dataE(2,:);
net = dataM - dataE;
amp = sqrt(net(:,1).^2 + net(:,2).^2 + net(:,3).^2);

x = 1:size(amp);
subplot(221)
plot(x,net(:,1))
title('x axis')
subplot(222)
plot(x,net(:,2))
title('y axis')
subplot(223)
plot(x,net(:,3))
title('z axis')
subplot(224)
plot(x,amp)
title('magnitude')