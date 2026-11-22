# 怎么写一篇新文章

**一句话：往 `posts/` 里丢一个 `.md` 文件，push 上去，网站和下面的目录会自动更新。**

## 三步走

1. 复制 `posts/_template.md`，改名为 `YYYY-MM-DD-英文短标题.md`
   例如 `2026-12-03-amazon-keyword-research.md`
2. 填好文件顶部的 frontmatter，正文用 Markdown 正常写
3. `git add` → `commit` → `push`

push 之后 GitHub Actions 会自动跑 `scripts/build.py`，重新生成文章页、`docs/posts.json` 索引和本页下方的文章目录，大约 1 分钟后网站刷新。什么都不用手动构建。

## frontmatter 字段说明

```yaml
---
title: 文章标题                 # 必填
date: 2026-12-03               # 必填，YYYY-MM-DD
category: 选品与市场            # 必填，必须是 config.json 里列出的栏目之一
tags: [选品, 广告, 案例]        # 选填，逗号分隔或数组都行
summary: 一句话摘要             # 建议填，不填会自动截取正文开头
author: 赵国星                 # 选填，默认用 config.json 的 author
cover: ""                      # 选填，封面图 URL，留空则不显示
lang: zh-CN                    # 选填
draft: false                   # 选填，true = 不发布（本地也看不到）
---
```

## 栏目清单

在 `config.json` 的 `categories` 里维护，当前是：

选品与市场 / 独立站与建站 / 流量与投放 / B2B 获客 / AI 自动化 / 合规与物流 / 复盘与案例 / 增长黑客 / MBA案例

要加新栏目，改 `config.json` 后再跑一次构建即可，不用改代码。

## 文件命名规则

- 文件名前缀日期决定排序和 URL：`2026-12-03-xxx.md` → 网页地址 `p/xxx/`
- 后半段用小写英文、数字、连字符，**不要用中文、空格、下划线**
- 同一天写多篇没问题，只要后半段不重复
- 以 `_` 开头的文件（如 `_template.md`）会被当作模板跳过

## 图片怎么放

把图片放进 `docs/assets/images/`，正文里写：

```markdown
![说明](../../assets/images/你的图片.png)
```

> 注意：文章页在 `p/<slug>/` 目录下，回到站点根目录要写 `../../`。首页写 `assets/images/...` 即可。

## 本地预览

```bash
cd techx-chuhai
python3 scripts/build.py          # 生成 docs/ 下的页面和索引
python3 -m http.server 8000 -d docs
# 浏览器打开 http://localhost:8000
```

改了 `posts/` 或 `config.json`，重跑一次 `build.py` 再刷新页面。

## 内容约定

- 只写能落地的：给步骤、给参数、给判断线，少讲空概念
- 涉及数据标明来源和时间，别写「据说」「大概」
- 案例里的客户名、报价、后台截图先脱敏
- 最初那 4 篇示例文章（PMF 验证、DPI 选品打分、B2B 线索清洗、AI 自动化）只是用来演示排版，随时可以删掉；`2026-11-21-growth-*` 是「增长黑客精读笔记」系列，不是示例；`2026-11-22-case-*` 是「增长黑客 MBA 案例」系列，也不是示例
- 案例分析固定结构：案例背景 → 核心困境 → 关键事实 → 分析框架 → 当时的决策 → 结果 → 课堂讨论题 → 迁移到出海场景 → 别踩的坑 → 一句话结论
