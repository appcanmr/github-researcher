# GitHub Researcher

> Daily GitHub Trending analysis with AI insights — automatically updated every day.

## 🌟 Features

- **Automated Daily Fetching** — Pulls GitHub Trending data every day at 08:00 Beijing time
- **Multi-Language Coverage** — Tracks Python, JavaScript, TypeScript, Rust, and Go
- **Focus Area Classification** — Groups repos by: AI/ML/LLM, Dev Tools, Web Frameworks, Cloud/DevOps
- **GitHub Pages Dashboard** — Clean HTML report at [https://appcanmr.github.io/github-researcher/](https://appcanmr.github.io/github-researcher/)
- **JSON Data Archives** — Raw data saved for historical analysis

## 📂 Project Structure

```
github-researcher/
├── .github/workflows/daily-update.yml  # GitHub Actions scheduler
├── daily/                               # Daily JSON + Markdown reports
├── docs/                                # GitHub Pages source (HTML reports)
├── indexes/                             # Trend index
├── projects/                            # Deep-dive project analysis
├── scripts/
│   ├── fetch_trending.py                # Scrape GitHub Trending
│   └── generate_report.py               # Generate analysis reports
├── requirements.txt
└── README.md
```

## 🚀 How It Works

1. **GitHub Actions** triggers daily at `0 0 * * *` (UTC = 08:00 Beijing)
2. `fetch_trending.py` scrapes GitHub Trending for all languages + specific ones
3. `generate_report.py` classifies repos into focus areas and builds reports
4. Reports committed to `daily/` and `docs/daily/`
5. GitHub Pages serves `docs/` as a static site

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Fetch today's trending data
python scripts/fetch_trending.py

# Generate reports
python scripts/generate_report.py

# Serve docs locally
python -m http.server 8000 --directory docs
```

## 📊 Focus Areas

| Area | Keywords |
|------|----------|
| AI / ML / LLM | llm, gpt, neural, deep learning, transformer, diffusion, RAG |
| Developer Tools | cli, ide, debugger, testing, ci/cd, build |
| Web Frameworks | react, vue, next, nuxt, svelte, vite, tailwind |
| Cloud / DevOps | kubernetes, docker, terraform, aws, serverless |

## 🔒 GitHub Token

Set `GH_TOKEN` as a repository secret with `repo` scope for the workflow to commit changes.

---

*Built with ☕ and automation*
