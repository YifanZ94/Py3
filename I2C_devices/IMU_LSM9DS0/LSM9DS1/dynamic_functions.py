# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:04:31 2022

@author: Administrator
"""
import scipy.linalg
import numpy as np
from math import sin, cos, atan2, atan, asin, pi, sqrt

def quaternion_iteration(omega,Ts):
    A = np.array([[0, -omega.item(0), -omega.item(1), -omega.item(2)],
        [omega.item(0), 0, omega.item(2), -omega.item(1)],
        [omega.item(1), -omega.item(2), 0, omega.item(0)],
        [omega.item(2), omega.item(1), -omega.item(0), 0]])
    return scipy.linalg.expm(A*Ts/2)

def Rot_by_quat(q):
    R = np.array([[q.item(0)**2+q.item(1)**2-q.item(2)**2-q.item(3)**2, 2*(q.item(1)*q.item(2)-q.item(0)*q.item(3)), 2*(q.item(0)*q.item(2)+q.item(1)*q.item(3))],
          [2*(q.item(1)*q.item(2)+q.item(0)*q.item(3)), q.item(0)**2-q.item(1)**2+q.item(2)**2-q.item(3)**2, 2*(q.item(2)*q.item(3)-q.item(0)*q.item(1))],
          [2*(q.item(1)*q.item(3)-q.item(0)*q.item(2)), 2*(q.item(0)*q.item(1)+q.item(2)*q.item(3)), q.item(0)**2-q.item(1)**2-q.item(2)**2+q.item(3)**2]])
    return R
    
def Euler_by_quat(q):
    Eulers = np.array([[atan2(2*(q.item(0)*q.item(1)+q.item(2)*q.item(3)), 1-2*(q.item(1)**2+q.item(2)**2))],
                      [asin(2*(q.item(0)*q.item(2)-q.item(3)*q.item(1)))],
                      [atan2(2*(q.item(0)*q.item(3)+q.item(1)*q.item(2)), 1-2*(q.item(2)**2+q.item(3)**2))]])
    return Eulers
# *180/pi
                       
def Euler_by_acc(a):
    Eulers = np.array([[atan2(a.item(1),a.item(2))],
                    [atan(-a.item(0)/sqrt(a.item(1)**2 + a.item(2)**2))],
                    [0]])
    return Eulers
    
def q_byEuler(Eulers_in):
    Eulers = Eulers_in/2
    q = np.array([[cos(Eulers.item(0))*cos(Eulers.item(1))*cos(Eulers.item(2))+sin(Eulers.item(0))*sin(Eulers.item(1))*sin(Eulers.item(2))],
      [cos(Eulers.item(1))*cos(Eulers.item(2))*sin(Eulers.item(0))-sin(Eulers.item(1))*sin(Eulers.item(2))*cos(Eulers.item(0))],
      [cos(Eulers.item(0))*sin(Eulers.item(1))*cos(Eulers.item(2))+sin(Eulers.item(0))*cos(Eulers.item(1))*sin(Eulers.item(2))],
      [sin(Eulers.item(2))*cos(Eulers.item(1))*cos(Eulers.item(0))-cos(Eulers.item(2))*sin(Eulers.item(1))*sin(Eulers.item(0))]])
    return q
    

def yaw_by_2mags(loc1, loc2):
    yaw = atan2(-(loc1.item(1)-loc2.item(1)),(loc1.item(0)-loc2.item(0)))
    return yaw

def Rx(roll):
    R = np.array([[1,0,0], [0,cos(roll),-sin(roll)], [0,sin(roll),cos(roll)]])
    return R

def Ry(pitch):
    R = np.array([[cos(pitch),0,sin(pitch)], [0,1,0], [-sin(pitch),0,cos(pitch)]])
    return R

def Rz(yaw):
    R = np.array([[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0,0,1]])
    return R

def Rot_by_Euler(Euler):
    R = np.matmul(np.matmul(Rx(Euler[0]), Ry(Euler[1])), Rz(Euler[2]))
    return R

# def X_velocity_displace_iteration(x,a,Ts):
#     x_k = np.array([[x.item(0)+a.item(0)*Ts],
#       [x.item(1)+x.item(0)*Ts+a.item(0)*Ts**2/2]])
#     return x_k
#%% variables standard format    
# quat = np.array([[1,0,0,0]]).T
# omega = np.array([[0.1,0.1,0.05]]).T
# Ts = 0.01
# quat_k = np.dot(quaternion_iteration(omega,Ts),quat)
# R = Rot_by_quat(quat)
# a = np.array([[0.1,0.1,9.8]]).T
# Euler_q = Euler_by_quat(quat)
# Euler_a = Euler_by_acc(a)
# q_Euler = q_byEuler(Euler_a)
# x_kpri = np.array([[0,1]]).T
# x_k = X_velocity_displace_iteration(x_kpri,a,Ts)



