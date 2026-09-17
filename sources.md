---
title: 来源与复现
slug: sources
---
# 来源与复现

核对日期：2026-09-17。本站依据已完成的本地协议、执行代码、摘要表及学习材料编写。公开内容为模型说明、设置和汇总；完整 UKBB bank 与执行所需数据保留在原项目。

* 目录
{:toc}

## 证据如何分层

| 层次 | 能证明什么 | 不能替代什么 |
|---|---|---|
| 协议 / config | 规定和保存了哪些设置 | 参数的生物学合理性或最优性 |
| 执行代码 | 生成、评分和路由如何实现 | 完整运行成功证明 |
| 完成标记 / 结果摘要 | 哪批执行完成、实际输出计数 | 独立位点或真实SC验证 |
| 历史讨论 / 学习文档 | 研究目标、来源与纠正背景 | 当前协议、代码与原始输出 |
| 外部文献 | 方法原理与设计背景 | 本地特定数字的经验验证 |

## 本地来源索引

下表路径相对于原始项目 `clike_ldblock_coloc_handoff_20260811/`。公开摘录移除了机器绝对路径和无关运行信息；原文件 SHA256 记录于[来源清单](evidence/source-manifest.json)，便于持有原项目者核对。摘录不是原文件的逐字节副本，也不是完整运行数据包。

| 来源 | 原项目相对路径 | 本站引用 |
|---|---|---|
| 1 Mb深度模型协议 | `outputs/sc_1mb_depth_20260910_v1/protocol.json` | [depth-20260910.json](evidence/depth-20260910.json) |
| donor扩展继承配置 | `scripts/sc_1mb_donor_20260911_v1/config.json` | [donor-config.json](evidence/donor-config.json) |
| 对称lead比较 | `outputs/sc_symmetric_20260912_v1/full/protocol.json` | [symmetric-20260912.json](evidence/symmetric-20260912.json) |
| 高召回设置 | `outputs/sc_high_recall_20260914_v1/protocol.json` | [high-recall.json](evidence/high-recall.json) |
| 新重复确认 | `outputs/sc_dimension_confirm_20260915_v1/PROTOCOL.json` | [confirmation.json](evidence/confirmation.json) |
| 旧formal设置 | `outputs/sc_formal_20260907_v1/protocol.json` | [formal-20260907.json](evidence/formal-20260907.json) |
| 新确认汇总 | `outputs/sc_dimension_confirm_20260915_v1/summary.tsv` | [汇总表](evidence/confirmation-summary.tsv) |
| 新确认完成 | `outputs/sc_dimension_confirm_20260915_v1/COMPLETE.json` | [完成标记](evidence/confirmation-complete.json) |

关键实现文件：

- `scripts/sc_1mb_pattern_20260909_v1/prepare_bank.py`：1 Mb窗口、面板填补、参考频率/标准差与LD。
- `scripts/sc_1mb_depth_20260910_v1/prepare_extension.py`：causal选择、频率/LD约束、效应符号和seed。
- `scripts/sc_1mb_depth_20260910_v1/run_shard.R`：遗传效应、GWAS/SC均值、嵌套深度、OLS、方法调用。
- `R/original_clike.R`：lead、clumping、局部邻域与白化绝对余弦。
- `scripts/sc_high_recall_20260914_v1/run.R`：开发保护界值与旧评价路由。
- `scripts/sc_dimension_confirm_20260915_v1/run.R`、`finish.R`、`verify.py`：新确认、实际汇总恢复与算术复核。

辅助历史解释来自 `outputs/sc_result_diagnostic_20260907_v1/排查结论.md`、`outputs/sc_source_reconciliation_20260909_v1/核对结论.md`，以及独立整理目录 `clike-正向成果/12_完整学习与组会材料_20260917/完整学习文档.md`。这些文件作为历史解释来源，不代替最新执行协议。

## 文献与支持范围

1. **Giambartolomei et al. (2014).** [Bayesian Test for Colocalisation between Pairs of Genetic Association Studies Using Summary Statistics](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383). *PLOS Genetics*. 支持经典coloc框架与单causal假设；不证明当前模拟下哪个方法更好。
2. **Wallace (2021).** [A more accurate method for colocalisation analysis allowing for multiple causal variants](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009440). *PLOS Genetics*. 支持多信号coloc–SuSiE分析背景。
3. **Schmid et al. (2021).** [scPower accelerates and optimizes the design of multi-sample single cell transcriptomic studies](https://www.nature.com/articles/s41467-021-26779-7). *Nature Communications* 12, 6625. 支持分别考虑样本数、细胞数与测序深度；不为0.8、8或目标网格作精确背书。
4. **Cai, Fan & Jiang (2013).** [Distributions of Angles in Random Packing on Spheres](https://jmlr.csail.mit.edu/papers/v14/cai13a.html). *JMLR* 14, 1837–1864. 支持随机球面方向角度参照；不校准经过自适应选择的CLike分数。
5. **用户提供的 CLike 方法讲义。** `WenxinJiang_jcsds_clike.pdf`，本地方法身份与局部白化路线的来源。它作为用户材料引用，不被写成已核验的同行评议论文，本站不分发讲义全文。

## 复现范围

本站足以阅读模型、检查公开协议摘录与确认汇总。完整重跑需要原项目代码、获授权的本地UKBB输入、冻结bank、causal计划、SNP/面板顺序、随机流和软件环境。只有seed不能保证跨软件版本逐位复现。

本次没有安装模拟依赖、运行模拟或修改原执行文件。新确认的真实执行恢复步骤见[版本页](history.md#新重复确认的实际执行链)。文档核验仅检查页面、链接、公式显示与摘录一致性，不声称重新验证全部科学结果。

## 维护本网页

正文为仓库根目录的 `index.md`、`model.md`、`settings.md`、`evaluation.md`、`history.md`、`sources.md`。编辑 Markdown 并提交后，GitHub Pages 从 `main` 分支根目录重新构建。导航与排版位于 `_layouts/default.html` 和 `assets/style.css`，公式由 MathJax 渲染。

这种发布方式使用 GitHub Pages 自带 Jekyll 构建与 Markdown 支持，参见 [GitHub 发布源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。新增实验时，应先保存独立协议和来源，再更新对应版本；不要直接覆盖旧版本使历史含义漂移。
