#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TechX 出海实验室 · 站点构建脚本（零第三方依赖）

扫描 posts/*.md → 生成：
  docs/index.html              首页（数据内联，file:// 直接打开也能用）
  docs/p/<slug>/index.html    每篇文章的静态落地页
  docs/posts.json             对外可用的文章索引
  docs/sitemap.xml / robots.txt
  README.md                   自动更新「文章目录」区块

用法：python3 scripts/build.py
"""
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
SITE_DIR = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"
CONFIG_PATH = ROOT / "config.json"
INDEX_TPL = SCRIPTS_DIR / "index-template.html"
PAGE_TPL = SCRIPTS_DIR / "page-template.html"
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def log(msg):
    print("[build] " + msg)


def render(template, values):
    """一次性占位符替换，值里再出现 {{XXX}} 不会被二次解析。"""
    return PLACEHOLDER.sub(lambda m: str(values.get(m.group(1), m.group(0))), template)


def json_for_script(value):
    """JSON 文本内联进 <script> 时，避免 </script> 提前闭合。"""
    s = json.dumps(value, ensure_ascii=False)
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def h(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def parse_scalar(raw):
    v = raw.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        v = v[1:-1]
    return v


def parse_list(raw):
    v = raw.strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    return [parse_scalar(x) for x in re.split(r"[,，]", v) if x.strip()]


def parse_frontmatter(text):
    """返回 (meta dict, body str)。只支持简单的 key: value 格式。"""
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("缺少 frontmatter，文件必须以 --- 开头")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("frontmatter 没有闭合的 ---")

    meta = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, raw = m.group(1).lower(), m.group(2)
        if key == "tags":
            meta[key] = parse_list(raw)
        elif key == "draft":
            meta[key] = parse_scalar(raw).lower() in ("true", "yes", "1", "on")
        else:
            meta[key] = parse_scalar(raw)

    body = "\n".join(lines[end + 1:]).strip("\n")
    return meta, body


def plain_text(body):
    """粗略去掉 Markdown 标记，用于自动摘要和无 JS 预览。"""
    s = re.sub(r"```.*?```", "", body, flags=re.S)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"^\s{0,3}#{1,6}\s*", "", s, flags=re.M)
    s = re.sub(r"^\s{0,3}[>|]\s*", "", s, flags=re.M)
    s = re.sub(r"[*`_~]", "", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "post"


def load_post(path, config):
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    if meta.get("draft"):
        return None

    stem = path.stem
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", stem)
    date_iso = meta.get("date") or (m.group(1) if m else datetime.now().strftime("%Y-%m-%d"))
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_iso):
        raise ValueError("date 必须是 YYYY-MM-DD，当前为：" + date_iso)

    slug = meta.get("slug") or (m.group(2) if m else stem)
    slug = slugify(slug)
    title = meta.get("title") or stem
    category = meta.get("category") or "未归类"
    if category not in config.get("categories", []):
        log("⚠ %s 的栏目「%s」不在 config.json 里，建议补上或改文章" % (path.name, category))

    text = plain_text(body)
    summary = meta.get("summary") or (text[:96].replace("\n", " ") + ("…" if len(text) > 96 else ""))
    chars = len(re.sub(r"\s", "", text))

    return {
        "slug": slug,
        "filename": path.name,
        "title": title,
        "date_iso": date_iso,
        "date": date_iso.replace("-", "."),
        "category": category,
        "tags": meta.get("tags") or [],
        "summary": summary,
        "author": meta.get("author") or config.get("author", ""),
        "cover": meta.get("cover", ""),
        "lang": meta.get("lang", "zh-CN"),
        "word_count": chars,
        "reading_time": max(1, round(chars / 350)),
        "url": "p/%s/" % slug,
        "body": body,
        "plain": text,
    }


def collect(config):
    posts = []
    slugs = set()
    for path in sorted(POSTS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            p = load_post(path, config)
        except Exception as e:
            log("✗ 跳过 %s：%s" % (path.name, e))
            continue
        if p is None:
            log("· 跳过草稿 %s" % path.name)
            continue
        if p["slug"] in slugs:
            log("✗ slug 重复：%s（来自 %s），请改文件名" % (p["slug"], path.name))
            sys.exit(1)
        slugs.add(p["slug"])
        posts.append(p)

    posts.sort(key=lambda p: (p["date_iso"], p["filename"]), reverse=True)

    counts = {}
    for p in posts:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    categories = [{"name": c, "count": counts.get(c, 0)} for c in config.get("categories", [])]
    for c in counts:
        if c not in config.get("categories", []):
            categories.append({"name": c, "count": counts[c]})

    tag_counts = {}
    for p in posts:
        for t in p["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    tags = [{"name": k, "count": v} for k, v in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))]

    return posts, categories, tags


def base_values(config, posts, categories, tags):
    repo = config.get("repo", "")
    repo_url = "https://github.com/" + repo
    base = config.get("base_url", "").rstrip("/") + "/"
    links = "".join(
        '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (h(l.get("url", "")), h(l.get("label", "")))
        for l in config.get("links", [])
    )
    short = config.get("short_name") or config.get("name") or "T"
    return {
        "SITE_NAME": h(config.get("name", "")),
        "SHORT_NAME": h(short),
        "BRAND_INITIAL": h(short[0].upper()),
        "TAGLINE": h(config.get("tagline", "")),
        "HERO_TITLE": h(config.get("hero_title", config.get("name", ""))),
        "HERO_HIGHLIGHT": h(config.get("hero_highlight", "")),
        "DESCRIPTION": h(config.get("description", "")),
        "AUTHOR": h(config.get("author", "")),
        "LICENSE": h(config.get("license", "CC BY-NC-SA 4.0")),
        "LINKS_HTML": links,
        "REPO_URL": h(repo_url),
        "CONTRIBUTING_URL": h(repo_url + "/blob/main/CONTRIBUTING.md"),
        "BASE_URL": h(base),
        "YEAR": str(datetime.now().year),
        "categories": categories,
        "tags": tags,
        "posts": posts,
        "base": base,
    }


def build_index(config, posts, categories, tags, v):
    tpl = INDEX_TPL.read_text(encoding="utf-8")
    site_data = {
        "site": {
            "name": config.get("name", ""),
            "tagline": config.get("tagline", ""),
            "repo": config.get("repo", ""),
        },
        "updated": posts[0]["date"] if posts else "—",
        "total": len(posts),
        "categories": categories,
        "tags": tags,
        "posts": [{k: p[k] for k in ("title", "date", "date_iso", "category", "tags", "summary", "url", "reading_time", "word_count")} for p in posts],
    }
    values = dict(v)
    values["SITE_DATA"] = json_for_script(site_data)
    (SITE_DIR / "index.html").write_text(render(tpl, values), encoding="utf-8")


def nav_card(post, label, fallback):
    if not post:
        return '<a href="../../"><small>%s</small><b>%s</b></a>' % (h(label), h(fallback))
    return '<a href="../%s/"><small>%s</small><b>%s</b></a>' % (h(post["slug"]), h(label), h(post["title"]))


def build_post_pages(posts, v, config):
    tpl = PAGE_TPL.read_text(encoding="utf-8")
    p_dir = SITE_DIR / "p"
    p_dir.mkdir(parents=True, exist_ok=True)

    # 清掉已经删除的文章页（只清理 docs/p 下由本脚本生成的目录）
    keep = {p["slug"] for p in posts}
    for old in p_dir.iterdir():
        if old.is_dir() and old.name not in keep:
            shutil.rmtree(old)
            log("清理旧文章页 p/%s/" % old.name)

    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        canonical = v["base"] + p["url"]
        values = dict(v)
        values.update({
            "TITLE": h(p["title"]),
            "DESCRIPTION": h(p["summary"]),
            "CATEGORY": h(p["category"]),
            "DATE": h(p["date"]),
            "DATE_ISO": h(p["date_iso"]),
            "AUTHOR": h(p["author"]),
            "SUMMARY": h(p["summary"]),
            "WORD_COUNT": str(p["word_count"]),
            "READING_TIME": str(p["reading_time"]),
            "CANONICAL": h(canonical),
            "TAGS_HTML": "".join('<span class="tag">#%s</span>' % h(t) for t in p["tags"]) or '<span class="tag">#出海</span>',
            "PREV_HTML": nav_card(older, "← 上一篇（更早）", "没有更早的文章了，回首页"),
            "NEXT_HTML": '<a class="right" href="../%s/"><small>下一篇（更新）→</small><b>%s</b></a>' % (h(newer["slug"]), h(newer["title"]))
                          if newer else '<a class="right" href="../../"><small>下一篇（更新）→</small><b>已经是最新一篇，回首页</b></a>',
            "POST_JSON": json_for_script(p["body"]),
            "NOSCRIPT_PREVIEW": h(p["plain"][:600]),
            "JSONLD_TITLE": json_for_script(p["title"]),
            "JSONLD_DESC": json_for_script(p["summary"]),
            "JSONLD_AUTHOR": json_for_script(p["author"]),
        })
        out_dir = p_dir / p["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render(tpl, values), encoding="utf-8")


def build_index_data(posts, categories, tags, config, v):
    payload = {
        "site": {
            "name": config.get("name", ""),
            "tagline": config.get("tagline", ""),
            "description": config.get("description", ""),
            "author": config.get("author", ""),
            "repo": config.get("repo", ""),
            "base_url": v["base"],
        },
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "updated": posts[0]["date_iso"] if posts else "",
        "total": len(posts),
        "categories": categories,
        "tags": tags,
        "posts": [{k: p[k] for k in ("title", "date", "date_iso", "category", "tags", "summary", "author", "cover", "lang", "url", "reading_time", "word_count", "filename", "slug")} for p in posts],
    }
    (SITE_DIR / "posts.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_seo(posts, v, config):
    urls = [(v["base"], "")]
    urls += [(v["base"] + p["url"], p["date_iso"]) for p in posts]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        lines.append("  <url><loc>%s</loc>%s</url>" % (h(loc), "<lastmod>%s</lastmod>" % lastmod if lastmod else ""))
    lines.append("</urlset>")
    (SITE_DIR / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (SITE_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % v["base"], encoding="utf-8")

    cname = SITE_DIR / "CNAME"
    domain = str(config.get("custom_domain", "")).strip()
    if domain:
        cname.write_text(domain + "\n", encoding="utf-8")
    elif cname.exists():
        cname.unlink()


def update_readme(posts, categories):
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- POSTS:START -->", "<!-- POSTS:END -->"
    i1, i2 = text.find(start), text.find(end)
    if i1 < 0 or i2 < 0 or i2 < i1:
        log("⚠ README 没找到 POSTS 标记，跳过目录更新")
        return

    lines = []
    for c in categories:
        group = [p for p in posts if p["category"] == c["name"]]
        if not group:
            continue
        lines.append("### %s\n" % c["name"])
        for p in group:
            summary = p["summary"].replace("\n", " ")
            if len(summary) > 62:
                summary = summary[:62] + "…"
            lines.append("- **%s** [%s](posts/%s) — %s" % (p["date"], p["title"], p["filename"], summary))
        lines.append("")
    lines.append("> 共 %d 篇 · 最近更新 %s · 本区块由 `scripts/build.py` 自动生成，请勿手动编辑" %
                 (len(posts), posts[0]["date"] if posts else "—"))

    new = text[:i1 + len(start)] + "\n" + "\n".join(lines) + "\n" + text[i2:]
    if new != text:
        path.write_text(new, encoding="utf-8")
        log("已更新 README 文章目录")


def main():
    if not CONFIG_PATH.exists():
        log("✗ 找不到 config.json")
        sys.exit(1)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    posts, categories, tags = collect(config)
    v = base_values(config, posts, categories, tags)

    build_index(config, posts, categories, tags, v)
    build_post_pages(posts, v, config)
    build_index_data(posts, categories, tags, config, v)
    build_seo(posts, v, config)
    update_readme(posts, categories)

    log("完成：%d 篇文章，%d 个栏目 → docs/" % (len(posts), len([c for c in categories if c["count"]])))
    log("本地预览：python3 -m http.server 8000 -d docs")


if __name__ == "__main__":
    main()
