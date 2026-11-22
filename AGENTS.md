# AGENTS.md — numerical-analysis-tutorial

## Mission
每篇 HTML 都应是一篇独立可读、证据可追溯的数值分析教程；不要写“讲义介绍了”“上节已经讲过”而不补足先验知识。

## Authoritative design practice
使用 https://github.com/1998x-stack/Olah-style-posts/tree/main/skills/olah-style-paper-posts/SKILL.md 的因果叙事：问题 → 反例 → 图解 → 机制 → 数学推导 → 数值实验 → 失败边界 → 参考资料。不得复制 Colah 文章的图文、标题结构和标识。所有图解独立原创。

## File owners
- `index.html` + `assets/css/site.css`：全站入口，七条路径。
- `courses.json`：课程唯一章节清单，包含 status: refined / legacy；同步维护链接。
- `chapters/NN.html`：正式章节稳定路径；根目录 NN.html 为历史重定向。
- `assets/css/article.css`：新版正文；`legacy.css`：过渡使用，06–28 不得误报已经精修。
- `assets/svg/NN-*.svg`：独立 SVG，viewBox、title、desc、清晰的尺寸与数学语义。
- `examples/reproduce.py`：无需网络的确定性数值断言。

## Content gate
1. 界定输入、输出和假设，区别条件数（问题）与稳定性（算法）。
2. 绝不将浮点舍入误差与插值截断余项混为一谈；不承诺不成立的收敛阶或渐进复杂度。
3. 只要是核心公式，就使用可访问 MathML（mfrac、msup、msub），显示公式带 aria-label 和内部横向滚动容器。SVG 内不嵌 MathML。
4. SVG 的每条箭头要能解释运算关系，至少 13px 标签；配逐图图注，脱离 JS 也能理解。
5. 每篇至少两幅解释型图、一段有断言的最小实验、错误案例、限制条件和原始来源链接。
6. 互动须使用原生 keyboard-accessible controls，静态内容不依赖 JS，不加载在线字体/CDN。
7. 验证 1440 / 768 / 390 / 360 px、打印、弱网、键盘焦点、公式排版、SVG 独立打开。
8. 发布之前运行 `python scripts/validate_site.py` 与 `python examples/reproduce.py`；未运行的浏览器检查必须写“未验证”。
9. 参考 Goldberg 的浮点算术论述、Higham 的数值稳定性理论、Berrut–Trefethen 的重心插值及 SciPy PCHIP 文档；区分来源结论和教学演示。

## Chapter 06–10 review invariants
- Spline: do not conflate natural S″ boundary with clamped S′ boundary; validate tridiagonal moment equations and example M=[0,-4,4,0].
- Chebyshev: weight 1/sqrt(1-x²) is integrable yet undefined at ±1; use θ transform, not endpoint evaluation.
- Continuous projection: distinguish L² and L∞ optimality and exact Gram integration from discrete least squares.
- Least squares: explain rank and κ₂(AᵀA)=κ₂(A)² only for full column rank; use QR/SVD for reliable implementations.
- Quadrature: Simpson 1:4:1 is for three equally spaced points; classic composite Simpson requires an even number of subintervals.
- Browser QA now covers chapters 01–10; new figures must be individually legible and have source-grounded captions.
