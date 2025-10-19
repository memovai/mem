# VibeGit: Memov


[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)
[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/memovai/mem)

**AI coding version control on top of Git. Track not just what changed, but _why_ it changed.**

---

## 🧠 Motivation

Traditional version control systems like Git are great at tracking code **changes**, but not the **reasoning** behind them. In an age of Vibe Coding, developers often interact with large language models (LLMs) through prompts, generate responses, and iteratively refine their code — but Git only sees the final result.

**Memov fills this gap.** It lets you version:

- 🤖 The **prompt** you gave to the AI  
- 📥 The **response** you received  
- 🧾 The **actual diff** made to your code
- 🧩 The **Source** diffs from Agent or User  

Even if no code changes occurred, you can still `mem snap` to record the interaction — because **thinking is part of the work**.

We are also developing an automation tool that does **not** require MCP or invasive workflow changes. Instead, it hacks the underlying logic of your development environment to automatically record every change you make. Our initial roadmap is focused on deep integration with Cursor, enabling seamless, context-rich versioning as you work. We also plan to provide migration tools to help users import their previous records and histories into Memov, ensuring a smooth transition and preservation of your valuable coding context.

---

## 🚀 Why Memov is Better than Git Alone

| Capability | Git | Memov |
|------------|-----|-------|
| Track prompt/response | ❌ | ✅ |
| Record reasoning without file change | ❌ | ✅ |
| Structure AI interactions with actual diffs | ❌ | ✅ |
| Avoid re-tokenizing for logs | ❌ | ✅ |
| Compatible with Git workflows | ✅ | ✅ |
| Uses Git internals (blobs/trees/commits/notes) | ✅ | ✅ |
| Supports semantic jump, show, amend | ❌ | ✅ |

> 💡 Instead of dumping prompts into Markdown or asking the AI to summarize its own reasoning (wasting tokens), **Memov captures structured data at the moment of interaction** — with no extra cost.

---

## 🧪 Installation

**Note:** Memov requires [git](https://git-scm.com/) to be installed. On Ubuntu/Debian, you can install it with:

```bash
sudo apt update && sudo apt install git
```

Clone the repository and install dependencies:

```bash
git clone https://github.com/memovai/mem.git
cd mem
pip install .
```

---

## 🚦 Quick Start

Initialize a Memov repo in your project:

```bash
mem init
```

Track files with context:

```bash
mem track file1.py -p "Initial layout" -r "Basic structure"
```

Take a snapshot (with or without file changes):

```bash
mem snap -p "Refactor config parser" -r "Switched to YAML"
```

Rename a file:

```bash
mem rename old.py new.py -p "Rename for clarity"
```

Remove a file:

```bash
mem remove legacy.py -p "Clean up" -r "No longer used"
```

Amend an existing commit with a prompt/response:

```bash
mem amend <commit-hash> -p "Better explanation" -r "Clarified method use"
```

Show history:

```bash
mem history
```

Inspect a snapshot:

```bash
mem show <prompt-id>
```

Jump to a specific snapshot:

```bash
mem jump <prompt-id>
```

Check status of working directory:

```bash
mem status
```

Use a different project root:

```bash
mem snap -p "Tweak README" --loc "/path/to/project"
```

---

## ⚙️ How It Works (Under the Hood)

Memov builds directly on Git’s plumbing layer:

- **File Tracking**: Uses `git hash-object` to store blobs before any formal commit.
- **Snapshots**: Uses `git mktree` + `git commit-tree` to snapshot project state, with prompt/response metadata.
- **Metadata**: Uses `git notes` to attach context to any commit (via `mem amend`).
- **Storage**: Stores everything in a bare repo under `.mem/memov.git`, separate from your main Git history.
- **Replaying History**: Uses commit trees + prompt IDs to support `mem jump`, `mem show`, etc.

---

## 📘 Command Reference

| Command | Description |
|---------|-------------|
| `mem init` | Initialize Memov and a bare Git repository |
| `mem track [file_paths...] [-p PROMPT] [-r RESPONSE] [-u]` | Track files with optional context |
| `mem snap [-p PROMPT] [-r RESPONSE] [-u]` | Create a snapshot, even without file changes |
| `mem rename old new [-p PROMPT] [-r RESPONSE] [-u]` | Rename tracked files |
| `mem remove path [-p PROMPT] [-r RESPONSE] [-u]` | Remove tracked files |
| `mem amend commit_hash [-p PROMPT] [-r RESPONSE] [-u]` | Attach/update context using Git notes |
| `mem history` | Show full history of tracked prompts and diffs |
| `mem show <prompt-id>` | Show full details of a specific snapshot |
| `mem jump <prompt-id>` | Checkout project to a previous snapshot |
| `mem status` | Show working directory diff vs. latest snapshot |

---

## 🧩 Final Thoughts

Memov is built for a world where LLMs, agents, and copilots are part of your team. When you build software with AI, your **process matters as much as your product** — and that process deserves to be versioned too.

If Git is the brain of your project, **Memov is its memory**.

In the era of vibe coding, every prompt you write, every response you receive, and every code transformation you make is costing your money! Your tokens and iterations are part of your intellectual property—they represent not just the final result, but the entire journey of problem-solving and creativity. Unlike traditional Git, which only records the end result of a feature with a brief description, Memov captures the full context: the prompts, the responses, and the reasoning behind every change. This makes your development history richer, more transparent, and more valuable for learning, collaboration, and reproducibility.
