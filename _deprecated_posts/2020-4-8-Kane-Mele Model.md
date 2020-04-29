---
title: Numerical Calculation of Kane-Mele model
tags: Note\笔记 Tech\技术
key: TightBindingModelKaneMele
layout: article
license: true
toc: true
pageview: true
aside:
    toc: true
sitemap: true
mathjax: true
---

$$\newcommand{\ad}{\text{ad}}$$
$$\newcommand{\End}{\text{End}}$$

The post below is about band structure calculation of a tight binding model on 2-dimensional honeycomb lattice. The model was first proposed by C.L. Kane and E.J. Mele in 2005.

I reproduce Fig. 1 in their paper via Python, it's a good exercise and indeed strengthen my understanding of translation symmetry and energy bands.

<!--more-->

Relevant papers:

[$Z^2$ Topological Order and the Quantum Spin Hall Effect](https://link.aps.org/doi/10.1103/PhysRevLett.95.146802)
Phys. Rev. Lett. 95, 146802 (2005).

[Quantum Spin Hall Effect in Graphene](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.226801)
Phys. Rev. Lett. 95, 226801 (2005).

## Introduction

For detail description of this model, see the paper. Basically, we have a tight-binding hamiltonian of this one electron system given in second quantization form

$$ H = H_1 + H_2 = \sum_{\braket{ij}\alpha} t_1 c_{i \alpha}^\dagger c_{j \alpha} + \sum_{\braket{\braket{ij}}\alpha\beta} it_2 \nu_{ij} s^z_{\alpha\beta} c_{i\alpha}^\dagger c_{j\beta}$$

in which first and second nearest neighbor hopping term is included.

The lattice we are considering is like a "strip" of graphene, means it has finite length in $y$ direction and infinite length in $x$ direction. We may assume that $N$ hexagon is aligning in $y$ direction, gives $N_j = 2N+2$ total atoms in a "unit cell" (this time the unit cell is a large one).

## Detail and Code

Label the cells in $x$ direction by index $n$, and atoms in a unit cell by index $j$, spin-1/2 is still denoted by $\alpha \in \\{ \uparrow, \downarrow \\}$.

Translation symmetry along $x$ allows us to introduce $k$, such that

$$ c_{nj\alpha} = \sum_k c_{kj\alpha} e^{-ikn}$$

and

$$ c^\dagger_{nj\alpha} = \sum_k c^\dagger_{kj\alpha} e^{ikn}$$

first consider the nearest hopping term, by some routine calculation

$$H_1 = t_1 \sum_k \sum_{j} \sum_{\Delta} c^\dagger_{kj\alpha} c_{k(j+\Delta j)\alpha} e^{-i k \Delta n}$$

where $\Delta$ goes over the 3 nearest neighbor of each atom, thus for each $k \in [0, 2\pi]$, an effective hamiltonian $h(k)$ in $2N_j \times 2N_j$ matrix form is obtained. For which, the base vector can be chosen as

$$\left[ 0\uparrow, 0 \downarrow, 1\uparrow, 1\downarrow, \dots , Nj-1\uparrow, Nj-1\downarrow \right]$$

the matrix element is non-zero only if the electron can transit between two sites

$$h_{j\alpha, (j+\Delta j)\alpha} = t_1 \sum_{\Delta n} e^{-i k \Delta n}$$

Code below adds the nearest neighbor hopping term

```python
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
N = 30
Nj = 2 * N + 2

def addHopping1(mat, Nj, t1, kx):
    for j in range(Nj):
        if j % 2 == 0:
            hoppingTo = [(0, 1), (0, -1), (1, 1)]
        else:
            hoppingTo = [(0, 1), (0, -1), (-1, -1)]
        for delta in hoppingTo:
            jDes = delta[1] + j
            if jDes >= 0 and jDes < Nj:
                elem = t1 * np.exp(1j * delta[0] * kx)
                mat[(2*j, 2*jDes)] += elem
                mat[(2*j + 1, 2*jDes + 1)] += elem
```

For the second neighbors

```python
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
                elem = 1j * delta[2] * t2 * np.exp(1j * delta[0] * kx)
                # print(j ,delta[0], jDes, elem)
                mat[(2*j, 2*jDes)] += elem
                mat[(2*j + 1, 2*jDes + 1)] += -elem
```
Calculate the spectrum

```python
def genHam(Nj, t1, t2, k):
    ham = np.zeros((2*Nj, 2*Nj), dtype=complex)
    addHopping1(ham, Nj, t1, k)
    addHopping2(ham, Nj, t2, k)
    return ham


ks = np.linspace(0, +2*np.pi, 200)
plt.axis([0, 2*np.pi, -1.1, 1.1])
for k in ks:
    hamilton = genHam(Nj, 1, 0.05, k)
    vals = list(map(np.real ,la.eigvals(hamilton)))
    xs = [k] * (2*Nj)
    plt.scatter(xs, vals, c='black', s=1)
plt.show()
```

and the output

![spectrum](/assets/images/KaneMeleSpectrum1.png)

Rashba term and sublattice potential can be added by rewriting the first function:

```python
def addHopping1(mat, Nj, t1, tr, tv, kx):
    for j in range(Nj):
        if j % 2 == 0:
            mat[(2*j, 2*j)] += tv
            mat[(2*j + 1, 2*j + 1)] += tv
            hoppingTo = {(0, 1): (-0.5, np.sqrt(3)/6), (0, -1): (0, -np.sqrt(3)/3), (1, 1): (0.5, np.sqrt(3)/6)}
        else:
            mat[(2*j, 2*j)] += -tv
            mat[(2*j + 1, 2*j + 1)] += -tv
            hoppingTo = {(0, 1): (0, np.sqrt(3)/3), (0, -1): (0.5, -np.sqrt(3)/6), (-1, -1): (-0.5, -np.sqrt(3)/6)}
        for delta in hoppingTo:
            dx, dy = hoppingTo[delta]
            jDes = delta[1] + j
            if jDes >= 0 and jDes < Nj:
                elem = np.exp(1j * delta[0] * kx)
                mat[(2*j, 2*jDes)] += t1 * elem
                mat[(2*j + 1, 2*jDes + 1)] += t1 * elem
                mat[(2*j+1, 2*jDes)] += 1j * tr * (dy + 1j * dx) * elem
                mat[(2*j, 2*jDes+1)] += 1j * tr * (dy - 1j * dx) * elem
```

## Discussions

to be continued ...