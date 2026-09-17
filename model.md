---
title: 生成模型
slug: model
---
# 生成模型

本页描述 1 Mb 深度实验及后续主线沿用的生成机制。实现依据为 `run_shard.R::genetic_value`、`prepare_extension.py::plans_for_replicates` 与新重复确认的 `run.R`；来源及哈希见[来源页](sources.md)。

* 目录
{:toc}

## 1. 模拟单位与数据流

一条输入由 **区域 × 重复编号 × 真值场景 × donor 数 n × 目标细胞数 m** 标识。同一条输入同时交给各比较方法。重复编号表示新的模拟抽样，不表示新的独立基因组区域。

```text
本地 UKBB chr22 基因型
  → 冻结 1 Mb 区域、样本面板、SNP 次序与等位基因方向
  → 选择 causal SNP 和效应符号
  → 生成 GWAS 表型、目标细胞类型的 donor 均值
  → 每个 SNP 的 donor 级 OLS：beta / SE / P / z
  → CLike、coloc.abf（相关历史批次另有 coloc.susie）
  → 按各自冻结界值计数保留、过滤或支持
```

**独立遗传关联样本量是 donor 数 n。** 每 donor 测 m 个细胞降低表达均值的细胞采样噪声，但不会把 QTL 样本量变为 n×m。

## 2. 基因型与 LD

使用本地 UKBB chr22 的 0/1/2 等位基因剂量，计数方向为 BIM A1。每个面板分别进行 SNP 均值填补；样本量不同的 QTL 面板虽按身份嵌套，但其填补均值可以不同。

模型区分三种 LD：CLike 使用参考面板的有符号相关矩阵；SuSiE 历史拟合使用与对应 GWAS/QTL 关联数据一致的面板 LD；选块和 clumping 使用相关系数的平方 r²。有符号 R 不能用 r² 矩阵代替。

参考面板与 GWAS 及最大 QTL 面板分离。位点/SNP 和等位基因方向必须一致；异常 LD、零方差或非有限关联统计量会使受影响分片停止。因果候选的频率筛选不等于删除输入中的其他 SNP。

## 3. 遗传效应

对性状 t 的 causal 集合 Cₜ，令 Kₜ 为其大小，fⱼ、sⱼ 分别为参考面板等位基因频率和经验剂量标准差；符号 aₜⱼ 独立抽取 ±1。代码计算：

$$
\beta_{tj}=\frac{a_{tj}}{s_j}\sqrt{\frac{h^2_{\mathrm{ref}}}{K_t}},
\qquad h^2_{\mathrm{ref}}=0.2,
$$

$$
G_{ti}=\sum_{j\in C_t}(X_{ij}-2f_j)\beta_{tj}.
$$

无 causal 的性状令 Gₜᵢ=0。同一性状内各 causal 的参考标准化效应绝对值相同：单 causal 为 √0.2；双 causal 每个为 √0.1。没有额外人为加强 private causal。共享 causal 指两性状使用同一个 SNP，不要求效应符号相同。

**0.2 是参考效应尺度，不保证实际遗传率为 20%。** 当 causal 之间存在 LD 时，遗传方差含交叉项：

$$V_{G,t}=\boldsymbol\beta_t^\top\Sigma_X\boldsymbol\beta_t.$$

实际样本方差还受选定面板和有限抽样影响，应读取保存的表型方差记录，而不能把配置字段直接写成实测 h²。

## 4. GWAS 表型

对固定 20,000 个 GWAS 样本：

$$Y^{\mathrm{GWAS}}_i=G_{1i}+\epsilon_i,
\qquad\epsilon_i\sim N(0,0.8).$$

同一区域、重复、场景内的不同 QTL 深度使用同一份 GWAS。H0 与 QTL-only 场景的 GWAS 遗传项为零。

## 5. 目标细胞类型表达均值

等价的细胞层表达写为：

$$Y_{ij}=G_{2i}+U_i+E_{ij},\qquad
U_i\sim N(0,0.8),\quad E_{ij}\sim N(0,8).$$

Uᵢ 是同一 donor 所有目标细胞共享的残差项；Eᵢⱼ 是独立的细胞层残差。对 m 个目标细胞取均值：

$$\bar Y_{i,m}=G_{2i}+U_i+\bar E_{i,m},\qquad
\bar E_{i,m}=\frac{1}{m}\sum_{j=1}^{m}E_{ij}.$$

因此：

$$\operatorname{Var}(\bar E_{i,m})=\frac{8}{m},\qquad
\operatorname{Var}(U_i+\bar E_{i,m})=0.8+\frac{8}{m}.$$

| 目标细胞 m | 细胞均值噪声 8/m | 总非遗传方差 0.8+8/m |
|---:|---:|---:|
| 10 | 0.800 | 1.600 |
| 50 | 0.160 | 0.960 |
| 200 | 0.040 | 0.840 |
| 1,000 | 0.008 | 0.808 |

增加 m 只能减少细胞均值噪声，不能消除 donor 残差的 0.8。均值性状在该模型下的理论遗传方差占比为：

$$h_m^2=\frac{V_G}{V_G+0.8+8/m}.$$

若仅为解释而额外假设 V_G=0.2，则 m=10 和 1,000 时分别约为 11.11% 和 19.84%；这是公式示例，非每条输入的实测结果。

## 6. 深度如何配对

代码直接模拟高斯细胞总和的增量，无需保存 n×m 个单细胞数值。对递增深度 m₀=0、m₁=10、m₂=50、m₃=200、m₄=1,000：

$$\Delta S_{i,k}\sim N\{0,8(m_k-m_{k-1})\},\qquad
\bar E_{i,m_k}=\frac{\sum_{\ell\le k}\Delta S_{i,\ell}}{m_k}.$$

这在本高斯模型下与嵌套使用同一批细胞的均值分布一致，不是先生成互不相关的四份表达：

$$\operatorname{Cov}(\bar E_{i,m},\bar E_{i,M})=\frac{8}{\max(m,M)}.$$

同一 n 内，不同 m 共享区域、causal、效应、GWAS、donor 噪声及嵌套细胞。**跨 n 的比较不同：**基因型按 donor 身份嵌套，但各面板分别填补，且表型噪声可独立，所以不能描述为只改变 n 的完全配对干预。

新重复确认虽只保留 n=500、m=1,000，仍消费历史省略面板/深度的随机数位置，以维持原生成顺序。H0–H2 使用单独命名空间，并共享该重复下的 null/present 组成；同一重复下的场景不能自动视作统计独立。

## 7. 关联统计量

每个 SNP 分别拟合含截距的一元线性回归：

$$Y_i=\alpha+X_{ij}b_j+e_i.$$

输出边际估计 b̂ⱼ、SE、双侧 t 检验 P 值（自由度 n−2），并以 zⱼ=b̂ⱼ/SEⱼ 作为 CLike 输入。这里 z 是 beta/SE 的惯用命名；P 值在代码中来自 t 分布。

## 8. 模型边界

这是归一化高斯目标细胞均值模型。它没有显式生成 UMI/count、文库大小、dropout、批次、细胞组成变化或 reads-per-cell；也没有在当前实验中加入混合细胞 bulk 机制。因此，m 表示目标类型细胞数，不能称为测序 reads 深度。

[scPower](https://www.nature.com/articles/s41467-021-26779-7) 支持把 donor 数、细胞数与测序深度分开考虑；本项目的 0.8、8 和 0.2 仍须作为本地模拟设定解释，不能由该文献推导为通用常数。
