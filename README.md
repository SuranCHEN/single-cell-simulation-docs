# Single-cell simulation · model & settings

CLike 的中文模型与实验设置文档。核对日期：2026-09-17。

**网站：<https://suranchen.github.io/single-cell-simulation-docs/>**

- [生成模型](model.md)
- [实验设置与参数依据](settings.md)
- [方法、阈值与评价](evaluation.md)
- [版本脉络](history.md)
- [来源与复现边界](sources.md)

GitHub Pages 从 `main` 根目录构建 Jekyll。正文保存在 Markdown；更新后自动发布。此仓库只包含文档、公开协议摘录和汇总，不含 UKBB 个体数据、donor身份、LD矩阵或凭证。

检查文档：`python3 check_docs.py`。这只核对文档结构、内部链接、协议关键字段与汇总，不启动模拟。
