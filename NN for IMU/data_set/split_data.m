clear; clc
data1 = load('DataSet_train_fast_0.03.mat');
data2 = load('DataSet_test_fast_0.03.mat');
data3 = load('DataSet_train_slow_0.015.mat');
data4 = load('DataSet_test_slow.mat');
Input = cat(1, data1.InputCell, data2.InputCell, data3.InputCell, data4.InputCell);
Target = cat(1, data1.TargetCell, data2.TargetCell, data3.TargetCell, data4.TargetCell);

for i = 1:size(Input,1)
    inputs = cell2mat(Input(1));
    targets = cell2mat(Target(1));
    save(sprintf('Input%d',i), 'inputs');
    save(sprintf('Target%d',i), 'targets');
end