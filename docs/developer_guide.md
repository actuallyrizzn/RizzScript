# Developer Guide

This document explains **how to work on the RizzScript codebase** — from environment setup to release management.

---

## 1. Code Style

• Follow **PEP 8** with 4-space indents.  
• Use *snake_case* for functions and variables, *PascalCase* for classes.  
• Limit lines to **120 chars** where practical (PyQt signals can be verbose).

---

## 2. Virtual Environment

The repo does not commit virtual-env folders.  Create one per the Installation guide.

---

## 3. Running the App in Dev Mode

```bash
$ python app.py
```

Hot-reload is not yet supported; restart the app to see changes.

---

## 4. Linting & Formatting

We recommend:

```bash
$ pip install black flake8 isort
$ black app.py
$ isort app.py
$ flake8
```

CI is not enforced yet, but please run the above before submitting a PR.

---

## 5. Branching Strategy

• **main** — always deployable  
• **feature/<topic>** — short-lived feature branches  
• **fix/<bug-id>** — bug-fix branches  

Merge requests should target **main** and require at least one approving review.

---

## 6. Commit Message Convention

Use **Conventional Commits** _(e.g. `feat: add dark mode`, `fix: handle 404`)_.  This makes automated changelog generation trivial.

---

## 7. Release Process

1. Update `CHANGELOG.md` (keep, create if missing).  
2. Bump the version inside `app.py` (a constant to be added).  
3. Run PyInstaller (see Installation guide).  
4. Draft a GitHub Release attaching `dist/RizzScript.exe` and any macOS/Linux builds.  

---

## 8. Dependency Management

If adding new libraries, update `requirements.txt` **and** provide a clear justification in the PR.

---

## 9. Testing

Tests are currently TODO.  Suggested stack: **pytest + pytest-qt** for GUI elements.

---

## 10. Contact & Support

RizzScript is maintained by volunteers.  Ping us in GitHub Discussions or open an Issue for quick help.