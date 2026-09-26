#!/usr/bin/env python3
"""
Verschiebt faellige Blog-Entwuerfe aus content/blog-drafts/ nach blog/,
regeneriert die Artikel-Liste in blog/index.html und aktualisiert sitemap.xml.

Ein Entwurf gilt als faellig, wenn sein FRONTMATTER-Feld publish_date
kleiner oder gleich dem heutigen Datum ist. Dateien, deren Name mit "_"
beginnt (z. B. _TEMPLATE.html), werden ignoriert.

Wird taeglich von .github/workflows/publish-blog.yml aufgerufen.
"""
import datetime
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "content" / "blog-drafts"
PUBLIC_DIR = ROOT / "blog"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE_URL = "https://cleanconnect.de"

FRONTMATTER_RE = re.compile(r"<!--\s*FRONTMATTER\s*(.*?)-->", re.DOTALL)
COMMENT_RE = re.compile(r"<!--(?!\s*FRONTMATTER).*?-->\s*", re.DOTALL)
# Reste aus _TEMPLATE.html, die nie oeffentlich werden duerfen.
PLACEHOLDER_RE = re.compile(
    r"\[(Artikel-Titel|Ziel-Keyword|Kurzbeschreibung|Kategorie|Einleitung|"
    r"Zwischenüberschrift|Platzhalter|Stichpunkt|Interner Link|CTA-)"
)
MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
             "August", "September", "Oktober", "November", "Dezember"]


def parse_frontmatter(html_text):
    match = FRONTMATTER_RE.search(html_text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def parse_date(value):
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def due_drafts(today):
    if not DRAFTS_DIR.exists():
        return []
    due = []
    for path in sorted(DRAFTS_DIR.glob("*.html")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_frontmatter(text)
        if not fields:
            print(f"[skip] {path.name}: kein FRONTMATTER-Block gefunden")
            continue
        publish_date = parse_date(fields.get("publish_date"))
        if publish_date is None:
            print(f"[skip] {path.name}: publish_date fehlt oder ungueltig ({fields.get('publish_date')!r})")
            continue
        if publish_date <= today:
            due.append((path, fields, text))
    return due


def finalize_article(text, slug, publish_date):
    """Bereitet einen Entwurf fuer die Veroeffentlichung vor.

    Entfernt interne Hinweis-Kommentare (FRONTMATTER bleibt, es wird fuer die
    Blog-Uebersicht gebraucht), setzt den Slug ein und uebernimmt publish_date
    in JSON-LD und sichtbares Datum, damit beides nie auseinanderlaeuft.
    """
    head, sep, rest = text.partition("<!DOCTYPE")
    text = COMMENT_RE.sub("", head) + sep + rest
    text = text.replace("[artikel-slug]", slug)
    iso = publish_date.isoformat()
    text = re.sub(r'("datePublished"\s*:\s*)"[^"]*"', rf'\g<1>"{iso}"', text)

    def fix_modified(match):
        current = parse_date(match.group(2))
        value = current if current and current >= publish_date else publish_date
        return f'{match.group(1)}"{value.isoformat()}"'

    text = re.sub(r'("dateModified"\s*:\s*)"([^"]*)"', fix_modified, text)
    text = text.replace('datetime="YYYY-MM-DD"', f'datetime="{iso}"')
    text = text.replace(
        "[Veröffentlichungsdatum]",
        f"{publish_date.day}. {MONTHS_DE[publish_date.month - 1]} {publish_date.year}",
    )
    return text


def publish(due, today):
    published = []
    for path, fields, text in due:
        dest = PUBLIC_DIR / path.name
        if dest.exists():
            print(f"[warn] {dest} existiert bereits, ueberspringe {path.name}")
            continue
        leftover = PLACEHOLDER_RE.search(text)
        if leftover:
            print(f"[skip] {path.name}: enthaelt noch Platzhalter ({leftover.group(0)}...)")
            continue
        text = finalize_article(text, path.stem, parse_date(fields["publish_date"]))
        dest.write_text(text, encoding="utf-8")
        path.unlink()
        published.append((dest, fields))
        print(f"[publish] {path.name} -> blog/{path.name} (publish_date={fields.get('publish_date')})")
    return published


def collect_public_articles():
    articles = []
    if not PUBLIC_DIR.exists():
        return articles
    for path in sorted(PUBLIC_DIR.glob("*.html")):
        if path.name == "index.html":
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_frontmatter(text) or {}
        articles.append((path, fields))
    return articles


def render_card(path, fields):
    title = fields.get("title", path.stem)
    description = fields.get("description", "")
    date = fields.get("publish_date", "")
    parsed = parse_date(date)
    label = f"{parsed.day}. {MONTHS_DE[parsed.month - 1]} {parsed.year}" if parsed else date
    href = path.name
    return (
        '<a class="blog-card" href="{href}">'
        '<time class="blog-date" datetime="{date}">{label}</time>'
        "<h2>{title}</h2>"
        "<p>{description}</p>"
        "</a>"
    ).format(
        href=escape(href),
        date=escape(date),
        label=escape(label),
        title=escape(title),
        description=escape(description),
    )


def update_blog_index(articles):
    index_path = PUBLIC_DIR / "index.html"
    if not index_path.exists():
        print("[warn] blog/index.html fehlt, ueberspringe Listen-Update")
        return False

    def sort_key(item):
        _, fields = item
        return parse_date(fields.get("publish_date")) or datetime.date.min

    articles_sorted = sorted(articles, key=sort_key, reverse=True)

    if articles_sorted:
        body = "\n".join(render_card(path, fields) for path, fields in articles_sorted)
    else:
        body = (
            '<p class="blog-empty">Noch keine veroeffentlichten Artikel. '
            "Neue Beitraege erscheinen hier automatisch, sobald sie ueber "
            "content/blog-drafts/ veroeffentlicht werden.</p>"
        )

    text = index_path.read_text(encoding="utf-8")
    new_block = f"<!-- BLOG_ARTICLES_START -->\n{body}\n<!-- BLOG_ARTICLES_END -->"
    new_text = re.sub(
        r"<!-- BLOG_ARTICLES_START -->.*?<!-- BLOG_ARTICLES_END -->",
        lambda _match: new_block,
        text,
        flags=re.DOTALL,
    )
    if new_text == text:
        return False
    index_path.write_text(new_text, encoding="utf-8")
    return True


def update_sitemap(published, index_changed, today):
    if not SITEMAP_PATH.exists() or not (published or index_changed):
        return False

    text = SITEMAP_PATH.read_text(encoding="utf-8")
    changed = False

    def upsert(loc, changefreq, priority):
        nonlocal text, changed
        if loc in text:
            return
        entry = (
            "  <url>\n"
            f"    <loc>{escape(loc)}</loc>\n"
            f"    <lastmod>{today.isoformat()}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>\n"
        )
        text = text.replace("</urlset>", entry + "</urlset>")
        changed = True

    upsert(f"{SITE_URL}/blog/index.html", "weekly", "0.6")
    if index_changed:
        # Blog-Uebersicht hat neue Eintraege: lastmod mitziehen.
        loc = re.escape(f"{SITE_URL}/blog/index.html")
        new_text = re.sub(
            rf"(<loc>{loc}</loc>\s*<lastmod>)[^<]*(</lastmod>)",
            rf"\g<1>{today.isoformat()}\g<2>",
            text,
        )
        if new_text != text:
            text, changed = new_text, True
    for dest, _fields in published:
        upsert(f"{SITE_URL}/blog/{dest.name}", "monthly", "0.6")

    if changed:
        SITEMAP_PATH.write_text(text, encoding="utf-8")
    return changed


def main():
    today = datetime.date.today()
    due = due_drafts(today)
    published = publish(due, today) if due else []

    index_changed = update_blog_index(collect_public_articles())
    sitemap_changed = update_sitemap(published, index_changed, today)

    if not published and not index_changed and not sitemap_changed:
        print("Keine faelligen Artikel, keine Aenderungen.")
        return 0

    print(
        f"Fertig: {len(published)} Artikel veroeffentlicht, "
        f"blog/index.html {'aktualisiert' if index_changed else 'unveraendert'}, "
        f"sitemap.xml {'aktualisiert' if sitemap_changed else 'unveraendert'}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
