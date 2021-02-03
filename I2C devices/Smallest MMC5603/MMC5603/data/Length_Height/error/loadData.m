clear; clc
T = [1,2,3];

x1 = 0:13;
x2 = 13.1:0.1:23;
x3 = 24:36;

%%
for i = 1:3
    figure
        dataE = load(sprintf('MMC_errorZ_%d_mag.txt',T(i)));
        dataM = load(sprintf('MMC_errorZ_%d_env.txt',T(i)));
        dataM(1,:) = dataM(2,:);
        dataE(1,:) = dataE(2,:);
        net2(:,i) =  dataM(:,3)-dataE(:,3);
        plot(x1,net2(1:14,i),x2,net2(15:114,i),x3,net2(115:end,i))
        hold on
        des2(i) = find(net2(:,i)<0,1);
end
