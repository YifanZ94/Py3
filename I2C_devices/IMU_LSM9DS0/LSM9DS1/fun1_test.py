import time
from dynamic_functions import quaternion_iteration, Rot_by_quat, Euler_by_quat, Euler_by_acc, q_byEuler,\
yaw_by_2mags, Rx,Ry,Rz, Rot_by_Euler
from numpy.linalg import inv, norm
import numpy as np

acc_raw = np.loadtxt('acc_raw.txt')
gyro = np.loadtxt('gyro.txt')
# acc_correct = np.loadtxt('acc_corrected.txt')
# Euler_Rpi = np.loadtxt('Eulers.txt')

acc_correct_2 = np.zeros(gyro.shape)
Euler_Rpi_2 = np.zeros(gyro.shape)
quat = np.zeros((4,gyro.shape[1]))

Euler_Rpi_2[:,0] = np.squeeze(Euler_by_acc(acc_raw[:,0]))
quat[:,0] = np.squeeze(q_byEuler(Euler_Rpi_2[:,0]))
acc_correct_2[:,0] = np.matmul(Rot_by_Euler(Euler_Rpi_2[:,0]), acc_raw[:,0])

Ts = 0.03
gyro_diff_list = []

for i in range(1,gyro.shape[1]):
    Eulers_acc_k = np.squeeze(Euler_by_acc(acc_raw[:,i]))
    quat[:,i] = np.matmul(quaternion_iteration(gyro[:,i],Ts), quat[:,i-1])
    Eulers_gyro_k = Euler_by_quat(quat[:,i])
    
    # gyro_k_norm = norm(gyro[:,i])
    # gyro_prev_norm = norm(gyro[:,i-1])
    # gyro_diff_norm = abs(gyro_k_norm - gyro_prev_norm)
    
    Euler_Rpi_2[:,i] = np.squeeze(Eulers_gyro_k)
    
    if norm(gyro[:,i]) > 0.03:
        Euler_Rpi_2[:,i] = np.squeeze(Eulers_gyro_k)
    else:
        Euler_Rpi_2[:,i] = Eulers_acc_k
        quat[:,i] = np.squeeze(q_byEuler(Euler_Rpi_2[:,i]))
        
    acc_correct_2[:,i] = np.matmul(Rot_by_Euler(Euler_Rpi_2[:,i]), acc_raw[:,i])

#%%
# import matplotlib.pyplot as plt
# plt.plot(Euler_Rpi_2[1,:])
# plt.plot(Euler_Rpi.T[1,:])
# plt.show()
# Euler_diff = Euler_Rpi_2[:,:-1].T - Euler_Rpi

#%%
file = open('quats_pi.txt', 'w')
np.savetxt(file, quat)
file.close()

file = open('Eulers_pi.txt', 'w')
np.savetxt(file, Euler_Rpi_2)
file.close()

file = open('acc_pi.txt', 'w')
np.savetxt(file, acc_correct_2)
file.close()
