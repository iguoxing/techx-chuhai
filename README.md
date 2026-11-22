# TechX 出海实验室 · 出海干货库

> 出海干货 · 只写能落地的

**在线站点**：https://novaxtra.cn/ （DNS 生效前可用 https://iguoxing.github.io/techx-chuhai/）

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

当前绑定的是 `novaxtra.cn`（DNSPod 管理）。GitHub 侧已完成：`config.json` 的 `custom_domain` 和 `base_url` 都改成了新域名，构建时自动生成 `docs/CNAME`，Pages 也登记了自定义域名。

**DNSPod 需要加的 5 条记录**（主机记录 / 类型 / 记录值）：

| 主机记录 | 类型 | 记录值 | 说明 |
| --- | --- | --- | --- |
| `@` | A | `185.199.108.153` | GitHub Pages IPv4 |
| `@` | A | `185.199.109.153` | 同上 |
| `@` | A | `185.199.110.153` | 同上 |
| `@` | A | `185.199.111.153` | 同上 |
| `www` | CNAME | `iguoxing.github.io` | **不带仓库名** |

要点：

1. **顺序不能反**：先在 GitHub 仓库登记域名（已完成），再去 DNSPod 加记录，否则域名有被别人抢注的风险
2. `@` 用 A 记录，不能用 CNAME（裸域的 CNAME 不合规）；`www` 用 CNAME 指向 `iguoxing.github.io`，**不是** `iguoxing.github.io/techx-chuhai/`
3. 不要加 `*.novaxtra.cn` 这种泛域名解析，有域名接管风险（GitHub 官方明确警告）
4. 国内 DNSPod 通常几分钟生效，官方上限 24 小时
5. 生效后到 `Settings → Pages` 勾选 **Enforce HTTPS**，证书是 GitHub 自动签发的，可能要等几分钟到几小时

验证命令：`dig novaxtra.cn +noall +answer -t A` 应返回上面 4 个 IP；`dig www.novaxtra.cn +noall +answer -t CNAME` 应返回 `iguoxing.github.io`。

> 换域名时只需改 `config.json` 的两个字段并重跑构建，DNS 和 Pages 设置不用动。

## 访问统计

用的是 **Cloudflare Web Analytics**：免费、不用 Cookie、不用弹 GDPR 同意横幅、**不用改 DNS**，能看到 PV / 访问数、来源、国家地区、设备类型和热门页面。数据只在 CF 后台看，页面上不显示阅读数。

### 第一次启用（只需一次）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)，左侧 `Analytics & Logs → Web Analytics` → `Add a site`
2. `Set up hostname` 填站点域名：`novaxtra.cn`（DNS 生效前先用 `iguoxing.github.io`，否则 CF 可能验证不过）
3. 在站点卡片点 `Manage site`，复制 JS snippet 里 `data-cf-beacon` 中的 **token**（一串字符）
4. 把 token 填进 `config.json`：

   ```json
   "analytics": {
     "enabled": true,
     "cloudflare_token": "这里粘贴 token"
   }
   ```

5. `git push` → Actions 自动重建，几分钟后 CF 后台就能看到数据

> CF 按 hostname 收数据。绑了 `novaxtra.cn` 后数据就只属于这个站，比挂在 `iguoxing.github.io` 下干净（那个 hostname 下其他 Pages 站点的流量会混进来）。注意 `.cn` 和 `.com` 是两个独立域名，novaxtra.com 的流量不会自动算进来。

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

### 增长黑客

- **2026.11.21** [精读 01｜增长黑客到底是个什么岗位](posts/2026-11-21-growth-01-growth-hacker-origin-sean-ellis.md) — Sean Ellis 提出增长黑客的前提是已经有 PMF：要找的不是品牌市场，而是只盯增长的人。
- **2026.11.21** [精读 02｜增长率才是唯一的方向盘](posts/2026-11-21-growth-02-growth-rate-compass-paul-graham.md) — Paul Graham：创业公司的定义就是快速增长，「每月新增 100」不是率，是下降的增长率。
- **2026.11.21** [精读 03｜冷启动必须做不能规模化的事](posts/2026-11-21-growth-03-do-things-dont-scale.md) — 用户不会自己来：手动招募、亲自上门，先用不可规模化的动作找到最热情的那一类人。
- **2026.11.21** [精读 04｜AARRR 五段漏斗，先修最漏的那段](posts/2026-11-21-growth-04-aarrr-pirate-metrics.md) — 把用户生命周期拆成获客、激活、留存、推荐、收入五段，用转化率找瓶颈，而不是凭感觉加投放。
- **2026.11.21** [精读 05｜所有渠道都会越来越差](posts/2026-11-21-growth-05-shitty-clickthroughs.md) — Andrew Chen：渠道效果必然衰减，早期 CPA 不能线性外推，模型里要给恶化留余量。
- **2026.11.21** [精读 06｜唯一重要的是产品市场匹配](posts/2026-11-21-growth-06-only-thing-that-matters-pmf.md) — Marc Andreessen：团队、产品、市场三者里市场最被低估；没到 PMF 时，所有优化都是白做。
- **2026.11.21** [精读 07｜40% 测试：测依赖，不测喜欢](posts/2026-11-21-growth-07-sean-ellis-40-test.md) — 问「如果明天用不了会怎样」，≥40% 回答非常失望才算有 PMF 信号；只问激活用户。
- **2026.11.21** [精读 08｜把 PMF 变成一个能提分的引擎](posts/2026-11-21-growth-08-superhuman-pmf-engine.md) — Superhuman 用四问问卷 + 路线图对半分，三个季度把 PMF 分数从 22% 推到 58%。
- **2026.11.21** [精读 09｜漏斗是漏的，循环是复利的](posts/2026-11-21-growth-09-growth-loops-vs-funnels.md) — Reforge：把增长设计成「产出再投入」的自增强闭环，每一轮都要能喂出下一轮。
- **2026.11.21** [精读 10｜留存是那个沉默的杀手](posts/2026-11-21-growth-10-retention-silent-killer.md) — Reforge：留存曲线走不走平，比任何首日数据都重要；等收入掉下来才发现已经晚了。
- **2026.11.21** [精读 11｜所有公司共用一个增长飞轮](posts/2026-11-21-growth-11-universal-growth-loop.md) — Brian Balfour：增长换来资源，资源解决更大问题，再产出增长；反过来也会负向复利。
- **2026.11.21** [精读 12｜别被单一北极星指标骗了](posts/2026-11-21-growth-12-north-star-metric-trap.md) — Brian Balfour：指标是生态系统不是记分牌，输出指标滞后，要盯可操作的输入指标。
- **2026.11.21** [精读 13｜你庆祝什么，团队就优化什么](posts/2026-11-21-growth-13-meaningless-growth-wheel.md) — Brian Balfour：注册数、下载量这类虚荣指标会形成自我强化的轮子，把团队带偏。
- **2026.11.21** [精读 14｜渠道和商业模式不匹配，再努力也白搭](posts/2026-11-21-growth-14-channel-model-fit.md) — Brian Balfour：很多增长卡住不是 LTV:CAC 没调好，而是这个渠道根本养不起你的客单价。
- **2026.11.21** [精读 15｜先算天花板，再谈努力](posts/2026-11-21-growth-15-model-market-fit-threshold.md) — Brian Balfour：PMF 只是入场券，市场 × 客单 × 可拿份额才决定你能长到多大。
- **2026.11.21** [精读 16｜发布不是那一天，是一套动作](posts/2026-11-21-growth-16-launch-for-growth.md) — Brian Balfour：把发布拆成预热、分批放量、回收反馈、二次传播，才能反复提取增长。
- **2026.11.21** [精读 17｜AI 能把产量拉满，但拉不出循环](posts/2026-11-21-growth-17-ai-content-growth-loop.md) — Brian Balfour 拆解 LinkedIn 的 AI 内容循环：低成本供给 + 分发入口 + 回流，缺一不可。
- **2026.11.21** [精读 18｜先验证假设，再写商业计划](posts/2026-11-21-growth-18-lean-startup-loop.md) — HBR 精益创业：把「按计划执行」换成构建-测量-学习循环，用可核算的指标判断进展。
- **2026.11.21** [精读 19｜增长黑客是一套流程，不是技巧清单](posts/2026-11-21-growth-19-growth-hacking-map.md) — Neil Patel 的全景入门：产品、渠道、数据、实验四块一起转，每个动作都要可测量可复制。
- **2026.11.21** [精读 20｜13 条原则里，最影响增长的是这两条](posts/2026-11-21-growth-20-startups-in-13-sentences.md) — Paul Graham：宁可少数人深爱，也别让多数人觉得还行；你衡量什么，就会变成什么。

### MBA案例

- **2026.11.22** [案例 01｜Hotmail：一封邮件就是一条广告位](posts/2026-11-22-case-01-hotmail-signature-viral-loop.md) — 没有预算的免费邮箱，靠每封邮件底部的签名链接完成病毒传播——增长黑客的第一个教科书案例。
- **2026.11.22** [案例 02｜Dropbox：一条邀请链接如何做出 39 倍增长](posts/2026-11-22-case-02-dropbox-referral-loop.md) — 不是广告也不是地推，而是「你邀请、我送空间」的双向奖励——把推荐循环做成产品的一部分。
- **2026.11.22** [案例 03｜PayPal：借 eBay 的流量池点爆双边市场](posts/2026-11-22-case-03-paypal-ebay-parasitic-growth.md) — 注册就送 10 美元、推荐再送 10 美元——PayPal 用现金补贴跨过网络效应的临界点，再把 eBay 的流量变成自己的…
- **2026.11.22** [案例 04｜YouTube：把播放器变成分发渠道](posts/2026-11-22-case-04-youtube-embed-viral-loop.md) — 一段可复制的嵌入代码，让每个博主都成了 YouTube 的推广员——内容型产品的增长，藏在生产者的发布流程里。
- **2026.11.22** [案例 05｜Airbnb：借 Craigslist 的流量池完成冷启动](posts/2026-11-22-case-05-airbnb-craigslist-cold-start.md) — 没有房源就没有客人，没有客人就没有房东——Airbnb 的解法不是砸钱，而是把房源同步到别人已有的流量池。
- **2026.11.22** [案例 06｜Uber：每个城市都是一个独立的生意](posts/2026-11-22-case-06-uber-city-unit-economics.md) — 全球扩张的真相是几百次城市级冷启动——把单元经济模型算清楚，才知道哪个城市该加码、哪个该撤。
- **2026.11.22** [案例 07｜Slack：先拿下三个人，再拿下三万人的公司](posts/2026-11-22-case-07-slack-team-first-plg.md) — 企业软件不靠销售敲门，而是让一个小团队先用起来——团队级邀请机制让产品自己穿透组织。
- **2026.11.22** [案例 08｜Figma：把协作和社区做成增长飞轮](posts/2026-11-22-case-08-figma-collaborative-plg.md) — 浏览器里多人同时改一张图，免费团队版加模板社区——Figma 证明了协作本身就是最好的获客渠道。
- **2026.11.22** [案例 09｜Duolingo：留存做对了，买量才有意义](posts/2026-11-22-case-09-duolingo-retention-ab-testing.md) — 连胜、经验值、排行榜背后是一整套实验流水线——语言学习平台的增长，核心不是拉新而是让人明天还回来。
- **2026.11.22** [案例 10｜Shopify：商户成功才是平台增长飞轮](posts/2026-11-22-case-10-shopify-merchant-success-flywheel.md) — 不做流量垄断者，而是帮商户自己带流量——应用商店、主题市场和支付物流，把商户成功变成平台护城河。
- **2026.11.22** [案例 11｜TikTok：先买一个内容池，再谈算法分发](posts/2026-11-22-case-11-tiktok-algorithm-global-cold-start.md) — 进入海外市场时没有用户也没有内容——TikTok 用并购拿到现成内容池作为起点，再用算法把内容供给和消费接成飞轮。
- **2026.11.22** [案例 12｜SHEIN：供应链就是增长引擎](posts/2026-11-22-case-12-shein-supply-chain-growth-flywheel.md) — 小单快反让「测款」成本极低，社交内容让流量几乎免费——快时尚出海的核心竞争力，其实是一套增长飞轮。
- **2026.11.22** [案例 13｜Temu：全托管加补贴，能买来多长久的增长？](posts/2026-11-22-case-13-temu-full-managed-subsidy-growth.md) — 新平台一边要用户一边要商家，全托管降低供给门槛、补贴降低需求门槛——但补贴退坡后的留存才是真考题。
- **2026.11.22** [案例 14｜Anker：从平台卖家到品牌，口碑才是增长资产](posts/2026-11-22-case-14-anker-brand-flywheel-from-seller.md) — 不靠低价厮杀，而是用评论数据反推产品迭代、从平台向品牌独立站迁移——中国跨境品牌化的经典样本。
- **2026.11.22** [案例 15｜HubSpot：免费工具加内容，B2B 获客的另一条路](posts/2026-11-22-case-15-hubspot-inbound-content-flywheel.md) — 不打断客户，而是让客户主动找上门——一个免费测分工具、一套内容体系，撑起了 inbound marketing 的增长飞轮。
- **2026.11.22** [案例 16｜Zoom：一个链接带来的爆发增长，和它的信任危机](posts/2026-11-22-case-16-zoom-product-virus-and-trust-crisis.md) — 免费版加「点链接就能入会」把非用户变成用户，但增长快过信任建设时，病毒循环也会反噬。
- **2026.11.22** [案例 17｜Canva：模板是增长杠杆，分享是分发渠道](posts/2026-11-22-case-17-canva-template-sharing-flywheel.md) — 让不会设计的人也能做出好看的图，再让作品自带分享属性——freemium 加模板社区把非用户变成传播者。
- **2026.11.22** [案例 18｜Notion：空白页是转化率杀手，模板才是入口](posts/2026-11-22-case-18-notion-template-community-growth.md) — 功能强大的 All-in-one 工具反而不知从何下手——Notion 用模板社区和达人演示，把复杂产品变成了「拿来就能用」…
- **2026.11.22** [案例 19｜Spotify：每周给你一个回来的理由](posts/2026-11-22-case-19-spotify-discover-weekly-retention.md) — Discover Weekly 不是功能点缀，而是留存基础设施；Wrapped 把用户数据变成可分享的社交内容，增长于是自己…
- **2026.11.22** [案例 20｜GitHub：开发者的个人账号，就是最好的获客入口](posts/2026-11-22-case-20-github-developer-network-flywheel.md) — 免费公共仓库 + 协作机制 + 开源沉淀，让每个开发者的日常使用都变成一次产品传播——最难复制的护城河是社区。

> 共 44 篇 · 最近更新 2026.11.22 · 本区块由 `scripts/build.py` 自动生成，请勿手动编辑
<!-- POSTS:END -->

## 授权

文章内容：**CC BY-NC-SA 4.0**（署名、非商业、相同方式共享）
站点代码：**MIT**

详见 [LICENSE](LICENSE)。
