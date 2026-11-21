# TechX 出海实验室 · 出海干货库

> 出海干货 · 只写能落地的

**在线站点**：https://iguoxing.github.io/techx-chuhai/

一个用来长期沉淀出海实战文章的 GitHub 仓库：文章全部是 `posts/` 目录下的 Markdown 原文，网站由 `scripts/build.py` 自动生成并托管在 GitHub Pages。**写文章 = 新增一个 `.md` 文件**，不用装 Node、不用装 Jekyll、不用本地构建。

---

## 这个仓库解决什么问题

| 常见做法 | 麻烦在哪 | 这里怎么做 |
| --- | --- | --- |
| 公众号 / 专栏 | 内容锁在平台里，不好检索、不好复用 | 原文是纯 Markdown，随时可导出、可改版 |
| 自建博客 CMS | 要服务器、要数据库、要维护 | GitHub Pages 全静态，零运维零成本 |
| Hugo / Jekyll | 要装环境、记模板语法 | 一个 Python 标准库脚本，零第三方依赖 |
| 纯 md 文件夹 | 没有网页，手机上看不方便 | 自动生成带分类、标签、搜索、明暗主题的站点 |

## 站点已带的能力

- 📚 分类筛选、标签聚合、全文标题/摘要搜索，支持 URL 参数直接分享筛选结果
- 🌓 深色 / 浅色主题切换并记住选择
- 📖 文章页自动生成目录（TOC）、阅读进度条、上一篇 / 下一篇
- 🔗 每篇文章一个干净的静态地址 `p/<slug>/`，带 title / description / OG 元信息
- 📱 手机、平板、桌面自适应
- 📦 `marked` 已放进仓库，站点本身零外部依赖（启用访问统计后才会加载一段 CF 脚本）
- 📊 访问统计已预留：`config.json` 填一个 token 即启用 Cloudflare Web Analytics，本地预览不计数
- 🤖 GitHub Actions：push 文章后自动重建站点、索引和下面的文章目录

## 目录结构

```
techx-chuhai/
├── config.json              # 站点名、简介、栏目、导航链接（改这里就行）
├── posts/                   # ← 你只管往这里写 Markdown
│   ├── _template.md         #   文章模板
│   └── 2026-11-21-xxx.md
├── scripts/
│   ├── build.py             # 零依赖构建脚本
│   └── page-template.html   # 文章页 HTML 模板
├── docs/                    # 生成的静态站点（GitHub Pages 发布这个目录）
│   ├── index.html
│   ├── posts.json           #   文章索引
│   ├── p/<slug>/index.html  #   每篇文章的落地页
│   └── assets/              #   CSS / JS / 本地 marked
├── .github/workflows/       # 自动构建
└── CONTRIBUTING.md          # 写文章的详细说明
```

## 快速开始

```bash
git clone https://github.com/iguoxing/techx-chuhai.git
cd techx-chuhai

python3 scripts/build.py                  # 重新生成站点
python3 -m http.server 8000 -d docs      # 本地预览 http://localhost:8000
```

发布新文章：

```bash
cp posts/_template.md posts/2026-12-03-my-new-post.md
# 编辑这个文件，填好 title / date / category / summary
git add posts/ && git commit -m "post: 新文章标题" && git push
```

push 后 Actions 自动构建，约 1 分钟网站更新。细节看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 绑自己的域名

在 DNS 加一条 CNAME 指向 `iguoxing.github.io`，把域名填进 `config.json` 的 `custom_domain`（构建时会自动生成 `docs/CNAME`），再到仓库 `Settings → Pages → Custom domain` 填一次即可。当前 `config.json` 里的 `base_url` 是 Pages 默认地址，换域名后同步改一下。

## 访问统计

用的是 **Cloudflare Web Analytics**：免费、不用 Cookie、不用弹 GDPR 同意横幅、**不用改 DNS**，能看到 PV / 访问数、来源、国家地区、设备类型和热门页面。数据只在 CF 后台看，页面上不显示阅读数。

### 第一次启用（只需一次）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)，左侧 `Analytics & Logs → Web Analytics` → `Add a site`
2. `Set up hostname` 填站点域名：现在填 `iguoxing.github.io`；以后绑了自定义域名就填那个域名
3. 在站点卡片点 `Manage site`，复制 JS snippet 里 `data-cf-beacon` 中的 **token**（一串字符）
4. 把 token 填进 `config.json`：

   ```json
   "analytics": {
     "enabled": true,
     "cloudflare_token": "这里粘贴 token"
   }
   ```

5. `git push` → Actions 自动重建，几分钟后 CF 后台就能看到数据

> CF 按 hostname 收数据，所以 `iguoxing.github.io` 下你其他 Pages 站点也会混进来。想数据干净：在 CF 后台按路径 `/techx-chuhai` 过滤，或者绑一个专属域名（例如 `notes.novaxtra.com`）再填那个域名。

### 其他说明

- 统计脚本由 `scripts/build.py` 自动注入到**首页和每一篇文章页**的 `</body>` 前，不用手动改 HTML
- 本机 `localhost` 预览和 `file://` 直接打开时**不加载**统计脚本，不会污染数据
- `analytics.enabled` 改成 `false` 可一键全关；token 留空时也不会注入任何脚本
- `ga4_id` / `baidu_id` 是预留位，填了会一起加载（GA4 国内常被墙，百度统计适合国内读者）
- 换域名后记得同步改 `config.json` 的 `base_url` 和 CF 后台的 hostname

## 文章目录

<!-- POSTS:START -->
### 选品与市场

- **2026.11.19** [选品别靠感觉，用一张 DPI 打分表](posts/2026-11-19-dpi-product-scoring.md) — 五个维度、每个 0–10 分，把「这个品能不能做」从拍脑袋变成一张能复盘的打分表。

### B2B 获客

- **2026.11.20** [B2B 线索清洗，从名单到能发的第一封邮件](posts/2026-11-20-b2b-lead-cleaning.md) — 一千条进口商名单不等于一千个客户。四步清洗把重复、经销商、无效联系方式全部挡在触达之前。

### AI 自动化

- **2026.11.21** [AI 自动化别一上来就搭系统，先找那 20 分钟](posts/2026-11-21-ai-automation-checklist.md) — 判断一件事该不该自动化，只需要三个数字：频率、单次耗时、判断是否可标准化。算完再动手。

### 复盘与案例

- **2026.11.18** [出海起步，先做 PMF 验证再谈投放](posts/2026-11-18-pmf-before-ads.md) — 预算烧在没验证的品上是最贵的学费。用三步最小验证，把「我觉得能卖」变成「数据说能卖」。

> 共 4 篇 · 最近更新 2026.11.21 · 本区块由 `scripts/build.py` 自动生成，请勿手动编辑
<!-- POSTS:END -->

## 授权

文章内容：**CC BY-NC-SA 4.0**（署名、非商业、相同方式共享）
站点代码：**MIT**

详见 [LICENSE](LICENSE)。
