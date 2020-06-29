import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import random

N = 31
Nj = 2 * N + 2


def genHam(Nj, t1, SO, tr, tv, k):
    # 新建一个2Nj * 2Nj的零矩阵
    ham = np.zeros((2*Nj, 2*Nj), dtype=complex)
    addHopping1(ham, Nj, t1, tr, tv, k)
    addHopping2(ham, Nj, SO, k)
    return ham


def addHopping1(mat, Nj, t1, tr, tv, kx):
    for j in range(Nj):
        if j % 2 == 0:
            # 子晶格势项
            mat[(2*j, 2*j)] += tv
            mat[(2*j + 1, 2*j + 1)] += tv
            if j % 4 == 0:
                hoppingTo = {(0, 1): (-0.5, np.sqrt(3)/6), (0, -1): (0, -np.sqrt(3)/3), (1, 1): (0.5, np.sqrt(3)/6)}
            else:
                hoppingTo = {(0, 1): (-0.5, np.sqrt(3)/6), (0, -1): (0, -np.sqrt(3)/3), (-1, 1): (0.5, np.sqrt(3)/6)}
        else:
            mat[(2*j, 2*j)] += -tv
            mat[(2*j + 1, 2*j + 1)] += -tv
            if j % 4 == 1:
                hoppingTo = {(0, 1): (0, np.sqrt(3)/3), (0, -1): (0.5, -np.sqrt(3)/6), (-1, -1): (-0.5, -np.sqrt(3)/6)}
            else:
                hoppingTo = {(0, 1): (0, np.sqrt(3)/3), (0, -1): (0.5, -np.sqrt(3)/6), (1, -1): (-0.5, -np.sqrt(3)/6)}
        for delta in hoppingTo:
            dx, dy = hoppingTo[delta]
            jDes = delta[1] + j
            if jDes >= 0 and jDes < Nj:
                elem = np.exp(-1j * delta[0] * kx)
                # 最近邻跃迁项
                mat[(2*j, 2*jDes)] += elem * t1
                mat[(2*j + 1, 2*jDes + 1)] += elem * t1
                # Rashba项
                mat[(2*j+1, 2*jDes)] += 1j * tr * (dy + 1j * dx) * elem
                mat[(2*j, 2*jDes+1)] += 1j * tr * (dy - 1j * dx) * elem


# 次近邻跃迁项
def addHopping2(mat, Nj, t2, kx):
    for j in range(Nj):
        if j % 4 == 0:
            des = [(0, 2, -1), (0, -2, -1), (-1, 0, +1), (1, 0, -1), (+1, -2, +1), (+1, 2, +1)]
        elif j % 4 == 1:
            des = [(0, 2, -1), (0, -2, -1), (-1, 0, -1), (1, 0, +1), (-1, -2, +1), (-1, 2, +1)]
        elif j % 4 == 2:
            des = [(0, 2, +1), (0, -2, +1), (-1, 0, +1), (1, 0, -1), (-1, -2, -1), (-1, 2, -1)]
        else:
            des = [(0, 2, +1), (0, -2, +1), (-1, 0, -1), (1, 0, +1), (+1, -2, -1), (+1, 2, -1)]
        for delta in des:
            jDes = delta[1] + j
            if jDes >= 0 and jDes < Nj:
                elem = 1j * delta[2] * t2 * np.exp(-1j * delta[0] * kx)
                mat[(2*j, 2*jDes)] += elem
                mat[(2*j + 1, 2*jDes + 1)] += -elem


def addMagenticField(mat, Nj, H):  # Zeeman term, magnetic field in x direction
    for j in range(Nj):
        mat[(2*j, 2*j + 1)] += H
        mat[(2*j + 1, 2*j)] += H


num = 200
ks = np.linspace(0, +2*np.pi, num)
plt.axis([0, +2*np.pi, -1.1, 1.1])
for k in ks:
    # 在这里填入哈密顿量各个参数：t1为最近邻，SO为自旋轨道耦合……
    hamilton = genHam(Nj, t1=1, SO=0.06, tr=0.05, tv=0.1, k=k)
    # addMagenticField(hamilton, Nj, H=0.0)
    # 求出所有本征值
    vals = list(map(np.real, la.eigvals(hamilton)))
    xs = [k] * (2*Nj)
    plt.scatter(xs, vals, c='black', s=1)  # 绘图
plt.show()
