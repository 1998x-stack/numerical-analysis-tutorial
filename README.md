# 数值分析 · Numerical Analysis

28 章中文数值分析教程，从浮点误差、插值、逼近、数值微积分到线性系统、特征值和常微分方程。

**首页目标地址**：https://1998x-stack.github.io/numerical-analysis-tutorial/ （实际访问取决于 Pages 设置和部署结果）

## 内容状态
- **01–10**：两批独立深度重构，包含数学推导、26 幅原创 SVG、交互与可复现实验。
- **11–28**：原文保留在 `chapters/`，尚未逐章技术复审。
- 根目录 `01.html` 等历史入口仅作跳转，保证旧链接兼容。

## 七条学习路线

| 路径 | 章节 | 主题 |
|---|---|---|
| 计算可信度 | 01–02 | 概述、误差、浮点与稳定性 |
| 插值与连续性 | 03–06 | Lagrange、Newton、Hermite、样条 |
| 逼近与最小二乘 | 07–09 | 逼近、最小二乘 |
| 积分与微分 | 10–14 | 求积、微分、正交多项式 |
| 线性系统与迭代 | 15–19 | LU、Cholesky、CG |
| 非线性与特征值 | 20–24 | 求根、Newton、幂法、QR |
| 动力系统与实战 | 25–28 | Euler、RK、刚性、Poisson |

## 文件结构
```text
index.html                  # Pages 首页
courses.json                # 28 章元数据
chapters/01.html ... 28.html
assets/css/{site,article,legacy}.css
assets/js/                  # 搜索和渐进增强
assets/svg/                 # 可单独打开的图解
examples/reproduce.py      # 最小数值实验/回归断言
scripts/validate_site.py   # 静态链接与 SVG/MathML 检查
.github/workflows/pages.yml
AGENTS.md
```

## 预览与验证
```bash
python -m http.server 8000
# http://localhost:8000/
python scripts/validate_site.py
python examples/reproduce.py
# 可选浏览器验收（需先 pip install playwright 并安装 chromium）
python scripts/browser_check.py  # 11 页 × 4 视口 = 44 次浏览器检查
```

## GitHub Pages
2026-11-22 已完成第一批主分支 Pages 部署，后续仍逐次核查部署状态。本仓库历史记录已存在 GitHub 自动生成的 **pages build and deployment** 成功运行。为避免与现有 Pages 来源相冲突，本仓库自定义 Actions 仅负责静态、数值与浏览器验收；站点继续由现有 Pages 来源设置发布。若新仓库未启用，请在 **Settings → Pages → Build and deployment** 选择 **Deploy from a branch → main / (root)**。合入主分支后仍须核对 Pages 的最新构建和网站可访问性。

具体写作、可视化、校验标准见 [AGENTS.md](AGENTS.md)。叙事灵感来自 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts)，所有技术图解独立绘制。
