%% real data
clear; clc
load('H10-30_B.mat','-mat');
load('H10-30_Loc.mat','-mat');
load('H10-30_para.mat','-mat');

test = load('t_mag.txt');

testloc = load('tlocs.txt');
xt = linspace(0,20,size(testloc,1));
plot(xt,testloc)
legend('x','y','z')
xlabel('time(s)')
title('location')

test_acc = load('t_acc.txt');
xt = linspace(0,20,size(test_acc,1));
figure
plot(xt,test_acc)
legend('ax','ay','az')
xlabel('time(s)')
title('accleration')

%%
theta = 0;

BxR2 = Bmap(:,1);
ByR2 = Bmap(:,2);
BzR2 = Bmap(:,3);
xR = LocMap(:,1);
yR = LocMap(:,2);
zR = LocMap(:,3);
%%
demX = p(1);
demY = p(2);
demZ = p(3);
xMin = p(4);
yMin = p(5);
zMin = p(6);


%% KNN
for j = 1:size(test,1)
    measure = [test(j,1)*cos(theta)-test(j,2)*sin(theta), test(j,1)*sin(theta)+test(j,2)*cos(theta), test(j,3)];
    measure_R = [(measure(1)-xMin)/demX, (measure(2)-yMin)/demY, (measure(3)-zMin)/demZ];
    
    D = zeros(1,size(BxR2,1));
    for i = 1:size(BxR2,1)
        D(i) = (BxR2(i)- measure_R(1))^2 + (ByR2(i)- measure_R(2))^2 + (BzR2(i)- measure_R(3))^2;
    end
    [t, I(j)] = min(D);
    
    location(j,:) = [xR(I(j)) yR(I(j)) zR(I(j))];  
end

%% plot
xRef = 1:size(test,1);
plot(xRef,location(:,1),xRef,testloc(:,1))
legend('MATLAB','Python')
xlabel('real location(cm)')
ylabel('predicted location(cm)')
title('X')
%%
figure
plot(xRef,location(:,2),xRef,testloc(:,2))
legend('MATLAB','Python')
xlabel('X reference(cm)')
ylabel('Y axis(cm)')
title('Y')
%%
figure
plot(xRef,location(:,3),xRef,testloc(:,3))
legend('MATLAB','Python')
xlabel('X reference(cm)')
ylabel('Z axis(cm)')
title('Z')