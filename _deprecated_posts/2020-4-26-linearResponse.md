---
title: 费米气的密度响应
tags: Note\笔记 QM\量子
key: LinearResponseTheory
layout: article
license: true
toc: true
pageview: true
aside:
    toc: true
sitemap: true
mathjax: true
---

## 线性响应理论

量子多体中涉及的线性响应理论，用来解决这样一个问题：

有某个体系，假设其哈密顿量是$H_0$。体系原本有一个密度算符$\rho_0 = e^{-\beta H_0}/Z_0$，沿着自己既定的道路演化。

在加上一个含时微扰后，体系的任一个可观测量$A$，其期望值（系综平均）也会相应地随时间改变，将这个改变近似到一阶，称为线性响应。

<!--more-->
如果将这个微扰描述成某个时间、空间都在变化的外场，微扰哈密顿一般可以写成：

$$ H_{pert} = \int dr h(r,t) O(r) $$

$O$是体系的某个算符，譬如$h$是外电势，$O$便取作电子密度算符。

考察某算符$A(r)$，经过一通计算后，可以获得一个十分漂亮的结果：

$$\braket{A(r)}_t \equiv Tr[\rho(t) A(r)] = \int dt' dr' \chi(r, r'; t, t') h(r', t')$$

其中$\chi(r, r'; t, t') = -i \theta(t-t') \braket{[A(r,t), O(r',t')]}_0$，算符$A(t)$定义为$e^{iH_0 t}Ae^{-iH_0 t}$。

这个式子在说，$(r',t')$处的场，对$(r,t)$处的某物理量会施加一个线性的影响，并且只有$t$时刻之前的场才能对$t$时刻的物理量施加影响。这也是经典量子力学沿用的伽利略时空观所要求的。

计算中使用的主要近似有两个：

- 假定体系绝热演化，即$H_0$的本征态在随时间缓慢变化，但处在任意本征态上的概率不随时间变化。
- 丢掉所有涉及$h$的二阶及以上项。

具体推导可以参考这个讲义：[Introduction to Many Body physics](https://dqmp.unige.ch/giamarchi/local/people/thierry.giamarchi/pdf/many-body.pdf)

当$H_0$是一个正常的具有时间平移和空间平移不变性的体系时，$\chi(r, r';t, t')$可以写作$\chi(r-r',t-t')$，对所有物理量进行Fourier变换后：

$$\braket{A(q,\omega)} = \chi(q,\omega)h(q,\omega)$$

$$\ket{S,S, \dots, S}$$

$$ \left|s,s-n\right\rangle \mapsto {\frac {1}{\sqrt {n!}}}\left(a^{\dagger }\right)^{n}|0\rangle _{B} $$

$$ S_{+}=\hbar {\sqrt {2s}}{\sqrt {1-{\frac {a^{\dagger }a}{2s}}}}\,a~,\qquad S_{-}=\hbar {\sqrt {2s}}a^{\dagger }\,{\sqrt {1-{\frac {a^{\dagger }a}{2s}}}}~,\qquad S_{z}=\hbar (s-a^{\dagger }a)$$

$$\left< \sum_j \sqrt {1-{\frac {a_j^{\dagger }a_j}{2s}}} \right> \approx N$$

$$H = \sum S_i \cdot S_j = \sum \left[ \frac{1}{2} (S^-_iS^+_j + S^+_iS^-_j) + S_{iz} S_{jz} \right]$$

$$S^-_i S^+_{i+1} \rightarrow a^+_i a_{i+1}$$

$$ \frac{\Delta M}{M(0)} = \frac{0.0587}{SQ} (\frac{k_B T}{2JS})^{\frac{3}{2}} $$