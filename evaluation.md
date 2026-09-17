---
title: 方法与评价
slug: evaluation
---
# 方法与评价

“lead 入口”“原始分数”“筛选界值”和“最终共定位支持”是不同环节。本页固定各自的含义，避免跨批次混用。

* 目录
{:toc}

## Original CLike

两侧分别按边际 P 值选择 lead，并贪心 clumping。为每个 lead 找局部 LD 邻域，枚举所有跨性状 lead 对，取两个邻域并集 B。在 B 内取两个 z 向量和有符号 LD 子矩阵：

$$R_B+\lambda I=U_B^\top U_B,\qquad
w_{t,B}=U_B^{-\top}z_{t,B}.$$

block 绝对余弦与区域得分分别为：

$$C_B=\frac{|w_{1,B}^\top w_{2,B}|}{\|w_{1,B}\|\,\|w_{2,B}\|},
\qquad S_O=\max_{B\ \mathrm{valid}} C_B.$$

这里先选 block，再局部白化；绝对值允许两侧整体方向相反。R² 只用于 lead/clumping/邻域规则，白化必须使用有符号 R。原方法分数不是共定位后验概率。

本页的 Original 指本地 `R/original_clike.R` 的局部白化余弦路线，当前调用使用两侧 P<10⁻³、min-block=5。历史 `R/block_coloc.R` 的局部 `coloc.abf` 最大 PP4 属于另一套混合流程，不能也标成同一个 Original。不同阈值下的 Original 也不是同一配置。

## Dimension CLike

候选 block、LD、ridge 与余弦保持不变，对每个 block 的维度 d_B 作参考变换，再取最大值：

$$q_B=\Pr\{T\ge C_B^2\},\qquad
T\sim\operatorname{Beta}\left(\frac12,\frac{d_B-1}{2}\right),$$

$$S_D=\max_{B\ \mathrm{valid}}[-\log_{10}(q_B)].$$

d_B 是 block 实际 SNP 数，不是 donor 数或有效独立 SNP 数。实现将 C² 的上界截在 `1 - .Machine$double.eps`，并直接计算 log-tail，减少数值下溢。

同一个 d 内这是单调变换；不同 d 之间可以重排 block 和输入。理想独立均匀球面方向的平方内积具有上述 Beta 参照，见 [Cai, Fan & Jiang (2013)](https://jmlr.csail.mit.edu/papers/v14/cai13a.html)。实际 CLike 有 lead 选择、block 选择、ridge、非零信号和跨 block 取最大值，因此 **q 只是参考尾面积，不能直接解释为已校准 P 值或后验概率**。当前研究使用开发数据冻结经验界值。

## 对照方法

`coloc.abf` 使用全区域 summary statistics，在单 causal 模型下输出 PP.H4；参见[原始 coloc 论文](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383)。

历史 `coloc.susie` 先对两侧精细定位，再比较信号对，参见[多 causal coloc–SuSiE 论文](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009440)。历史汇总可取信号对最大 PP4；这是带模型假设的方法输出，不等于 CLike 余弦。最新新重复确认仅比较 Original、Dimension 与 ABF，没有重拟合 SuSiE。

## 99% 开发保护界值

每个方法、n、m 分别处理三个共享场景。若某场景开发集有 N 条输入（含 no-call），目标保留率为 r，最多允许过滤：

$$a=\lfloor(1-r)N\rfloor.$$

将该场景有限分数升序排列，取第 a+1 个为场景界值；如果所有有限分数都可被允许过滤，则界值设为 +∞。再取三个场景界值的最小值，作为该方法、n、m 的共同界值 τ。

主分析 r=0.99、N=600，所以 a=6、候选界值为第7个有限分数。路由严格定义为：

```text
status == ok 且 score 有限 且 score < τ  → 过滤
分数等于 τ，或 no-call / NA             → 转交后续
```

三场景取最小值让开发数据中每类共享同时满足经验保护目标，但不保证新数据或未知总体达到99%。评价集中每类共享300条，漏失≤3条才达到该类99%经验保留。

## 最近确认的固定界值

条件为 n=500、m=1,000。这些数值从旧开发阶段保存下来，新批次没有重拟合。

| 方法 | 界值 τ | 限制场景 |
|---|---:|---|
| Original CLike | 0.238302279300059 | double_shared2 |
| Dimension CLike | 1.86995769551458 | double_shared2 |
| coloc.abf screen | 2.48048323978619×10⁻¹⁷ | double_shared1 |

ABF 的筛选界值很低，是为保留多 causal 共享输入而得到的开发结果。通过这个筛选界值不等于 PP4≥0.8 的强支持。三个方法不能共用一个数值界值，因为分数含义与尺度不同。

## 分母、NA 与 no-CS

| 量 | 分母与操作 |
|---|---|
| 共享保留率 | 转交的真实共享 / 全部真实共享；含 no-call 转交 |
| 非共享过滤率 | 被过滤的非共享 / 全部非共享 |
| 可评分覆盖率 | 有效有限分数输入 / 全部输入 |
| no-CS 条件回收率 | no-CS 真共享中的入选数 / 全部 no-CS 真共享 |
| 全共享中的额外贡献 | 同一回收数 / 全部真共享；与上一行分母不同 |

`no_leads`、`no_valid_block` 记为 NA，表示不能按该规则评分，不是余弦等于0或生物学不共享。在高召回预筛选中，它们全部转交，同时计入下游负担。在历史 no-CS 候选回收中，no-call 留在分母但不计作回收。分母为0时结果为 NA，不是0%。

no-CS 只取明确的 SuSiE `no_credible_sets` 状态，不把不收敛或数值失败全部并入。历史 Q5B 使用真共享 no-CS 子集中的**原始回收比例 ≥0.05 且 lower95>0**；它不是“全部共享增量的下界≥5个百分点”。不能把 51/1021=4.99510284% 四舍五入为5.00%后判通过。

## 保护通过与优势通过

“每类共享经验保留≥99%”是保护目标。“Dimension 相对 Original 的描述性优势”还要求每一种共享场景都不增加漏失，并且增加非共享过滤。

现有新重复确认在 n500×m1000 下：Original 过滤144/1050个非共享、漏失2/900个共享；Dimension 过滤343/1050、漏失3/900。每类共享均达到经验99%，但**不满足每类共享漏失不增加的更严格优势条件**。这段计数只用于说明评价规则，不能推导真实运行加速或独立位点泛化。

来源：[确认摘要](evidence/confirmation-summary.tsv)、[完成标记](evidence/confirmation-complete.json)。
