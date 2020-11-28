---
title: JuliaLang 初体验 & 超导中的杂质散射
tags: Note\笔记 Tech\技术
key: GreenfucntionSCstate
layout: article
license: true
toc: true
pageview: true
aside:
    toc: true
sitemap: true
mathjax: true
---

<!-- $$\newcommand{\ad}{\text{ad}}$$
$$\newcommand{\End}{\text{End}}$$ -->

这些天被各种渠道安利Julia，又见到哥们在复现一篇文献[^1]结果，用MATLAB写得很脏，于是进行了Julia初体验，感觉非常不错。

这也是我新配的电脑第一次（在没有打开steam的状态下）把八核十六线程跑满，生产力的香气从机箱里溢出来，值得祝贺（x

<!--more-->

## Introduction

这篇文章讲的大约是这么一个问题（二手转述自哥们）：通过STM扫描超导体表面，可以看出 $k$ 空间的电子密度分布，当存在一些能够和电子相互作用的杂质点（离子、磁性原子etc）时，密度分布会在原本的费米面上叠加一层花样，这样可以间接获得关于超导态&杂质的信息。我们想把这个花样算出来。

## 理论

基本上就是算一个格林函数……当把问题简化成电子在杂质的中心势场中运动之后，杂质散射的费曼图会非常好画。理论结果指导下的算法大概是：

- 二维布里渊区$(-\pi, +\pi)$，切分成N*N个格点
- 储存每个格点上的$G^0(\vec{k}, \omega)$ (4×4 矩阵)，即无杂质情况下的格林函数，超导体的格林函数似乎一般都写成这种4×4的形式（Nambu表示？）
- 微扰计算势能带来的格林函数变化（这个散射问题下微扰级数很巧的可以严格求和，非常漂亮，具体公式和费曼图见[^2]）

## 代码

```julia
using ProgressMeter
using Distributed
@everywhere using SharedArrays, LinearAlgebra
using PyPlot

# 增加16线程，注意别开太多
addprocs(16 - nprocs());
println("Running ",nprocs()," processes");

function B(kx::Float64, ky::Float64)::Matrix{Float64}
    Ex = -2 * t1 * cos(kx) - 2*t2*cos(ky) - 4*t3*cos(kx)*cos(ky);
    Ey = -2*t1*cos(ky) - 2*t2*cos(kx) - 4*t3*cos(kx)*cos(ky);
    Exy = -4*t4*sin(kx)*sin(ky);
    Δ = Δ₀*cos(kx)*cos(ky);
    return [
        [(Ex - μ)    Δ    Exy     0   ]; 
        [   Δ   (-Ex + μ)     0   -Exy]; 
        [Exy    0       (Ey - μ)  Δ   ];
        [0      -Exy    Δ   (-Ey + μ)]];
end


function generateG(N)::Array{Matrix{ComplexF64}}
    a = -π + π/N : 2*π/N : (π - pi / N + 0.00001 );
    wI4 = (ω + im * δ).* I4;
    [inv( wI4 - B(kx, ky)) for kx=a, ky=a]
end

@everywhere function ρ(qx, qy, G⁰, TG⁰, st, N)::ComplexF64
    result = 0.0;
    for kx in 1:st:N, ky in 1:st:N
        kpx = (kx + qx - 1 + N) % N + 1;
        kpy = (ky + qy - 1 + N) % N + 1;
        Gkkp = G⁰[kx, ky] * TG⁰[kpx, kpy];
        Gkpk = G⁰[kpx, kpy] * TG⁰[kx, ky];
        result += Gkkp[1,1] - conj(Gkpk[1, 1]) + Gkkp[3, 3] -conj(Gkpk[3,3]);
        # print(result, ' ')
    end
    return real(result * im)
end

println("preparing G^0 etc ...");

ω = -0.13;
V₀ = 0.4;
N = 400; # 画图的格点数
M = 200; # 积分时用的格点数，可以比画图用的格点少几倍
Δ₀ = 0.1;
μ = 1.25;
δ = 0.005;
st = convert(Int, (N / M));
(t1, t2, t3, t4) = (-1, 1.3, -0.85, -0.85);
I2 = Matrix{Float64}(I, 2, 2);
I4 = Matrix{Float64}(I, 4, 4);
V = kron(I2, (V₀.* I2));

G⁰ = generateG(N);
Γ⁰ = sum(G⁰[1:st:N, 1:st:N]) / (M^2);
T = inv(I4 - V*Γ⁰) * V;
TG⁰ = [T * g for g in G⁰];

println("Done! Generating Pixels ...");

offset = convert(Int, N/2); # 用来把布里渊区中心移动到图中央
final = SharedArray(zeros(N, N));
@time @sync @distributed for qx in 1:N # 只在这里开了多线程，并行计算像素点
    for qy in 1:N
        final[qx, qy] = ρ(qx-offset, qy-offset, G⁰, TG⁰, st, N);
    end
end

filename = "data400*200";
# 生成filename.txt 和 filename.png

# code for plot
PyPlot.set_cmap("gray_r")
imsave(filename * ".png", -final)

using DelimitedFiles
writedlm( filename * ".txt", final, ',');

println("Done! pixel data write to $filename.txt, $filename.png");
```

- Julia 这个语言对希腊字母、上下标的支持……孩子都感动哭了;
- 运行起来真的很快;
- 自己掌控数据类型的感觉真的很好
- 代码真的很短;
- 加上一堆macro之后并行计算这种事情也可以几行之内办到了（虽然还是调了一早上bug……）。

<font size="12px" color="#ff0000">快来用Julia！！！</font>



[^1]: Zhang, Yan-Yang, et al. ["Quasiparticle scattering interference in superconducting iron pnictides."](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.80.094528) Physical Review B 80.9 (2009): 094528.

[^2]: Balatsky, Alexander V., Ilya Vekhter, and Jian-Xin Zhu. ["Impurity-induced states in conventional and unconventional superconductors."](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.78.373) Reviews of Modern Physics 78.2 (2006): 373.