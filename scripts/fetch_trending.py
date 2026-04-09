#!/usr/bin/env python3
"""
fetch_trending.py — Fetch GitHub Trending repositories.
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import date

GITHUB_TRENDING_URL = "https://github.com/trending"

# Languages to focus on
TARGET_LANGUAGES = {"Python", "JavaScript", "TypeScript", "Rust", "Go", "Java", "C++", "C#"}


def fetch_trending(language=None):
    """Fetch trending repositories from GitHub."""
    url = GITHUB_TRENDING_URL if not language else f"{GITHUB_TRENDING_URL}/{language}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GitHubResearcher/1.0)",
        "Accept": "text/html",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_trending(html):
    """Parse GitHub trending page HTML, return list of repo dicts."""
    soup = BeautifulSoup(html, "lxml")
    repos = []

    for article in soup.select("article.Box-row"):
        try:
            # Repo name and author
            h2 = article.select_one("h2 a")
            if not h2:
                continue
            href = h2.get("href", "")
            repo_name = href.lstrip("/")

            # Star count
            stars = article.select_one('[href*="/stargazers"]')
            stars_text = stars.get_text(strip=True).replace(",", "") if stars else "0"

            # Today stars
            today_stars = article.select_one(".d-inline-block.float-sm-right")
            today_text = ""
            if today_stars:
                txt = today_stars.get_text(strip=True)
                today_text = txt.replace("stars today", "").replace(",", "").strip()

            # Language
            lang = article.select_one('[itemprop="programmingLanguage"]')
            language = lang.get_text(strip=True) if lang else None

            # Description
            desc_tag = article.select_one("p")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # Stars count as int
            try:
                stars_int = int(stars_text)
            except ValueError:
                stars_int = 0

            repos.append({
                "name": repo_name,
                "stars": stars_int,
                "today_stars": today_text,
                "language": language,
                "description": description,
            })
        except Exception:
            continue

    return repos


def main():
    today = date.today().isoformat()

    # Fetch overall trending
    print(f"Fetching GitHub Trending for {today}...")
    html = fetch_trending()
    repos = parse_trending(html)

    # Filter for target languages
    all_repos = repos
    filtered = [r for r in repos if r["language"] in TARGET_LANGUAGES]

    output = {
        "date": today,
        "total": len(all_repos),
        "filtered_count": len(filtered),
        "repositories": all_repos,
        "filtered_repositories": filtered,
    }

    out_file = f"daily/{today}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Fetched {len(all_repos)} repos, {len(filtered)} in target languages.")
    print(f"Saved to {out_file}")

    # Also save per-language trending
    for lang in ["Python", "JavaScript", "TypeScript", "Rust", "Go"]:
        try:
            html_lang = fetch_trending(language=lang)
            repos_lang = parse_trending(html_lang)
            out_lang = f"daily/{today}-{lang}.json"
            with open(out_lang, "w", encoding="utf-8") as f:
                json.dump({"date": today, "language": lang, "repositories": repos_lang}, f, ensure_ascii=False, indent=2)
            print(f"Saved {lang} trending to {out_lang} ({len(repos_lang)} repos)")
        except Exception as e:
            print(f"Failed to fetch {lang}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
