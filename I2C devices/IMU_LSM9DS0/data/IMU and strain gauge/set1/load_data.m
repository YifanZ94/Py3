clear; clc
% systemIdentification   % sid app
% 4 and 7 is good comparison
F_transducer = load('test7_holdBoard_inAir_fast.txt');
IMU = load('test7_acc.txt');

C = 1.2e-3/(20*0.0098);   % C*gram --> strain reading
Force = F_transducer(:,2)/C;
aX = IMU(:,1);

subplot(211)
plot(Force)
xlabel('sampling')
ylabel('force(N)')
subplot(212)
plot(aX)
xlabel('sampling')
ylabel('accX(m/s2)')
%%
% X1 = 708:1465;    % test 1
% X2 = 79:274;

% X1 = 796:1473;    % test 4
% X2 = 106:277;

% X1 = 591:820;    % test 5
% X2 = 86:142;

% X1 = 672:1135;    % test 6
% X2 = 102:216;

X1 = 672:1135;    % test 7
X2 = 102:216;


%%  resample
Force = Force(X1);
aX = resample(aX(X2),size(X1,2),size(X2,2));
% 
% aX = aX(X2);
% Force = resample(Force(X1),size(X2,2),size(X1,2));

%% line plot
subplot(211)
plot(Force_4)
xlabel('sampling')
ylabel('force(N)')
subplot(212)
plot(aX_4)
xlabel('sampling')
ylabel('accX(m/s2)')

%% scatter plot
% acc_sets = [aX_5;aX_7];
% force_sets = [Force_5;Force_7];
% figure
% scatter(aX_5,Force_5)
% hold on
% scatter(aX_7,Force_7)
% hold on
% scatter(aX_4,Force_4)
xlabel('accX(m/s2)')
ylabel('force(N)')

%% sid result
out_filtered = sim(ss1,Force_7);
out_unfiltered = Force_7/0.2;
plot(out_unfiltered)
hold on
plot(aX_7)
hold on
plot(out_filtered,'k')
legend('F/m','a','sid-ss')
xlabel('sample')
ylabel('acc(m/s2)')
set(gca,'FontSize',15)

%% integration for displacement
Ts = 0.01;
displacement_a = cumtrapz(Ts, cumtrapz(Ts, aX_7));
displacement_F = cumtrapz(Ts, cumtrapz(Ts, Force_7/0.2));
displacement_filtered = cumtrapz(Ts, -cumtrapz(Ts, out_filtered));
figure
plot(displacement_a)
hold on
plot(displacement_F)
hold on
plot(displacement_filtered)
legend('acc','F/m','sid-ss')
xlabel('sample')
ylabel('displacement(m)')

