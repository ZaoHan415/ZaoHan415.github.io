---
title: 李代数逻辑链整理
tags: Note\笔记
key: LieAlgebraLearningAndForgetting
mathjax: true
articles:
  data_source: zaohan415.github.io
  show_cover: false
  show_excerpt: true
  show_readmore: true
  show_info: true
---
$$\newcommand{\ad}{\text{ad}}$$
$$\newcommand{\End}{\text{End}}$$

刘院（以下简称liu）名下的物院神课“李群与李代数”，久闻大名，这学期以身试法，上课体验却实在一言难尽……

<!--more-->

究其原因，liu基本是按韩其智《物理学中的群论》一书来讲的，此书逻辑链清晰，但大量重要命题没有证明，且存在逻辑跳步；liu的补充材料内容详实，但编排顺序常和认知顺序相悖，很多地方没有说清；再者，李代数整套理论包含层层抽象，本人被物理荼毒太久，对于使用一些抽象层次过高的方法容忍度较高，这种态度恐不适于学习一套数学理论，经常学到后面忘了前面。新开此坑，希望能借之看清李代数的脉络。

不求列出所有相关定理，而是希望寻找一条最短的路通向我们需要的结论，即李代数分类和Dynkin图。

先修内容预警：线性代数；

参考书目：
- 韩其智《物理学中的群论》
- Pierre Ramond, *Group Theory A Physicist’s Survey*
- liu的讲义和优秀同学的注解：[@ThomasYangth 's repo](https://github.com/ThomasYangth/Liu-Groups-pkuphy)

## 基本理论

研究李代数，是因为李群描述了很多有用的对称性，而李代数和局部李群之间有一一对应的关系，这个关系在早年间是由李氏三定理描画的，现代的数学书似乎不这么搞了，不过

### 李代数
定义了李乘积$L \times L \rightarrow L$的向量空间$L$称为一个李代数，李乘积记为

$$(x, y) \mapsto [x, y]$$

满足：
- 双线性
- $[x, x] = 0, \forall x$
- Jacobi Identity

同态、同构、子代数概念都可据此定义

对于有限维线性空间$V$，用$\End V$表示$V\rightarrow V$上所有线性变换的集合，$\End V$是一个$n^2$维线性空间，可以写成$n\times n$矩阵，按常规的矩阵乘法对易子定义的李括号可以形成一个李代数，记为$\text{gl}(V)$，大部分我们关心的李代数都可以表示成$\text{gl}(V)$的子代数，称为线性李代数。

每一有限维李代数都同构于某个线性李代数（[Ado-Iwasawa定理](https://en.wikipedia.org/wiki/Ado%27s_theorem)）

### 内导子

对于一般的代数$u$（定义了乘法的线性空间），导子$\delta$定义为满足

$$\delta(ab) = \delta(a)b + a\delta(b) $$

的$u \rightarrow u$线性映射。

对于李代数，$\forall x \in L$，可以定义导子 $\ad x$为映射$y \mapsto [x, y]$，可以证明它满足上面导子的定义。这一形式的导子称为内导子，其余都叫外导子。

#### 内积与Killing度规

内导子作为线性映射，在给李代数选择了一组基后，我们当然可以对于每个线性映射定义迹，由此可以引出内积、进而度规、正交等概念。

$X, Y \in L$, 定义内积为$(X, Y) = Tr(\ad(X)\ad(Y))$

Killing度规 

$$g_{ij} = (x_i, x_j)$$

### 结构常数

取李代数$L$的一组基${x_i}$，结构常数由下式定义：
$$[x_i, x_j] = a^k_{ij} x_k $$

由李乘积定义可以发现结构常数必然满足两个等式（略）。

在同构的意义上，结构常数唯一确定一个抽象李代数。

### 理想
$L$的子空间$I$如果满足

$$\forall x \in L, y \in I, [x, y] \in I$$

则$I$称为$L$的理想

### 单李代数、半单李代数

如果$L$除了它自己和0以外没有其它理想，且若$[L, L]$ 非0（这一条没有别的意思，只是去掉一维李代数情况）,则称$L$是单纯的。

半单李代数可以粗暴的定义为其Killing度规非退化的李代数。

### 商代数
对于$L$的每一个非零真理想$I$，可以有商代数$L/I$，显然应该要求商空间中的乘法定义为：

$$[x + I, y + I] = [x, y] + I$$



<!--
{% if site.liker_id %}
<iframe
  frameborder="no"  
  style="width: 100%; max-width: 360px; height: 180px; margin: auto; overflow: hidden; display: block;"
  src="https://button.like.co/in/embed/{{site.liker_id}}/button?referrer={{ page.url | absolute_url | cgi_escape }}">
</iframe>
{% endif %}
-->