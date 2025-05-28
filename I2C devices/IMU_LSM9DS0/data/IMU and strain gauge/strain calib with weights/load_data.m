clear; clc
strain_gauge = load('10g.txt');
strain_gauge = strain_gauge - mean(strain_gauge(1:200,:));
plot(strain_gauge(:,2))
% X = {311:475, 688:760, 1063:1195};  % 2g
% X = {449:553, 790:875};  % 5g
X = {539:725, 939:1151, 1412:1554};  % 10g
% X = {254:598};  % 20g
% X = {459:738};  % 50g
% X = {333:652};  % 200g
% X = {366:953};  % 500g
%%
for i = 1:size(X,2)
    strain_mean(i) = mean(strain_gauge(X{i},2));
end

%% plot

weights = [2,5,10,20,50,200,500];
G = [1.16, 2.84, 5.58, 12, 30, 121, 300]* 10^-4;
scatter(weights,G)
xlabel('weight(g)')
ylabel('strain gauge reading')