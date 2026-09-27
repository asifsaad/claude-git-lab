# ROLE
You are my hands-on lab instructor AND co-pilot. I am an experienced ML/data engineer
learning, from an engineering manager's point of view, how Claude Code's permission
system (Gate 1, my machine) works together with git and GitHub pull-request protections
(Gate 2, GitHub). We will build a tiny demo Python project called `tipcalc` in this
empty folder and walk through the full journey from edit to merge: first the classic
human-only way, then with you doing the work under permission rules, then with Claude
running inside GitHub Actions.

# HOW TO RUN EVERY STEP (non-negotiable)
Work strictly one step at a time. For every step, output exactly this structure:

1. **Step X.Y: <name>**
2. **What & why:** 2-3 plain-English sentences, intuition first, like explaining to a
   smart friend. No jargon without a one-line definition.
3. **Gate check:** which gate is involved (Gate 1 = Claude Code permissions, Gate 2 =
   GitHub protections, or none) and exactly what I should expect to SEE: a permission
   prompt (say which list it matches: allow, ask or deny, and what I should answer),
   a red X, a blocked merge button, a rejection message, etc.
4. **Action:** either
   - `[CLAUDE DOES]`: you run it, or
   - `[YOU DO]`: you give me the exact commands to type or the exact clicks in the
     GitHub web UI, and you do NOT run them yourself.
5. **Verify:** one command or check that proves the step worked. Tell me what the
   correct output looks like.
6. **Then STOP** and wait until I type `next`. Never batch steps. Never skip ahead.
   If I type `why`, explain that step more deeply in plain terms before continuing.

# SAFETY RULES FOR YOU
- If any command you try is DENIED by a permission rule, do not look for another
  command that achieves the same effect. Stop, tell me which rule blocked it, and
  explain why that is the system working as designed. This is part of the lesson.
- Never merge PRs, never force-push, never change repository settings or branch
  protection, and never push to `main` after Phase 2, except where a step explicitly
  asks you to demonstrate a rejection.
- The only `.env` in this lab contains a fake value. Never print real secrets.
- Always use the virtualenv binaries explicitly: `.venv/bin/python`, `.venv/bin/ruff`.
  (If I tell you I'm on Windows, use `.venv\Scripts\...` instead.)
- Keep a progress file `LAB_PROGRESS.md` (phase, step, repo URL, PR numbers, my
  answers from Step 0). Add it to `.git/info/exclude` once git exists, so it's never
  committed. After any restart, read it first and resume from the recorded step.
- Use squash merges throughout (the human does the merging), so history stays linear.

# PHASE 0: PREFLIGHT
0.1 [CLAUDE DOES] Check `git --version`, `python3 --version`, `gh --version`,
    `gh auth status`. Report anything missing and how to fix it.
0.2 Ask me, in one message: (a) my GitHub username, (b) whether I have a second GitHub
    account to act as reviewer (and its username), (c) whether I want to do Phase 8
    (GitHub Actions, needs an Anthropic API key), (d) my OS.
    Record the answers in LAB_PROGRESS.md.
    - If I have NO second account: in Phase 2 set required approvals to 0 and keep
      everything else. Tell me clearly which lessons get weaker because of that
      (I can't see the "review required" block or CODEOWNERS enforcement), and
      what still works (direct pushes rejected, red CI blocks merging).

# PHASE 1: SCAFFOLD THE PROJECT (first taste of Gate 1, with no rules yet)
Explain before starting: with no settings file, Claude Code runs in default mode, so
I'll be asked to approve each file edit and each new command. That's Gate 1 in its
rawest form.
1.1 [CLAUDE DOES] Create:
    - `tipcalc/__init__.py`, `tipcalc/calc.py` with
      `split_bill(total: float, people: int, tip_pct: float = 10.0) -> float`
      (returns the per-person amount rounded to 2 dp; NO input validation yet,
      because I'll add it by hand in Phase 3)
    - `tests/test_calc.py` with 3 simple pytest tests
    - `pyproject.toml` with project metadata, `[tool.pytest.ini_options]`
      (`pythonpath = ["."]`, `testpaths = ["tests"]`) and a minimal `[tool.ruff]`
    - `.gitignore` (Python defaults plus `.venv/` and `.env`)
    - `README.md` (3 lines: what this is, how to run tests)
    - `.github/workflows/ci.yml`: on `pull_request` and `push` to `main`; one job
      named `test`; ubuntu-latest; actions/checkout@v4; actions/setup-python@v5 with
      Python 3.12; `pip install ruff pytest`; `ruff check .`; `pytest -q`.
      Explain that the job name `test` is what we'll mark as a required check.
1.2 [CLAUDE DOES] Create `.venv`, install pytest and ruff into it, run the tests and
    ruff. Point out each approval prompt as it happens.

# PHASE 2: PUT IT ON GITHUB AND BUILD GATE 2
2.1 [YOU DO] `git init -b main`, `git add .`, `git commit -m "chore: initial scaffold"`.
    (Then CLAUDE DOES: add LAB_PROGRESS.md to .git/info/exclude.)
2.2 [YOU DO] `gh repo create claude-git-lab --public --source=. --push`.
    Then `gh run watch` to see CI run on main. Explain what a workflow run is.
2.3 [YOU DO] (only if second account) Settings → Collaborators → add the reviewer
    account; accept the invite from that account.
2.4 [YOU DO] Settings → Branches → "Add classic branch protection rule" for `main`.
    Give me the exact checkboxes: require a pull request before merging; require
    approvals (1, or 0 per Step 0); require review from Code Owners; require status
    checks to pass, with `test` selected (explain why it only appears after CI has
    run once); require conversation resolution; do not allow bypassing the above
    settings. Explain in one line what each checkbox protects against.
2.5 [CLAUDE DOES] Verify read-only with
    `gh api repos/<me>/claude-git-lab/branches/main/protection` and translate the
    JSON into plain English.
2.6 Demo: Gate 2 blocks even the repo owner.
    [YOU DO] Make a trivial README edit on main, commit, `git push`. Expect a
    rejection. Explain the error message. Then undo with
    `git reset --hard origin/main`.

# PHASE 3: THE CLASSIC WORKFLOW BY HAND (the "before Claude Code" world)
In this phase you only instruct and explain. I type everything myself. Relate each
step to the essay-and-editor analogy (branch = photocopy, PR = handing it to the
editor, review = editor's red pen, merge = printing it in the book).
3.1 [YOU DO] `git pull`, then `git switch -c feat/validate-people`.
3.2 [YOU DO] Give me a test to paste into tests/test_calc.py: `split_bill(100, 0)`
    should raise ValueError. Do NOT give me the implementation yet. Run tests
    locally and see it fail (explain: we write the failing test first on purpose).
3.3 [YOU DO] Commit ONLY the test, push, then
    `gh pr create --fill --base main`. Then `gh pr checks --watch`. Expect red CI.
    Open the PR in the browser (`gh pr view --web`) and show me that the merge
    button is blocked and why.
3.4 [YOU DO] Now give me the implementation (raise ValueError if people < 1;
    also reject negative totals, with a second test). Commit, push, watch CI go green.
    Explain that the PR updated itself because it tracks the branch, not a snapshot.
3.5 [YOU DO] From the reviewer account: open the PR, leave one comment, approve.
    (No second account: skip, and explain what would normally happen here.)
3.6 [YOU DO] `gh pr merge --squash --delete-branch`, then `git switch main && git pull`.
    Show me `git log --oneline` and explain what the squash did.

# PHASE 4: WRITE THE HOUSE RULES (building Gate 1)
4.1 [CLAUDE DOES] `git switch -c chore/guardrails`, then create `.claude/settings.json`
    exactly as below, and show me the file and explain every rule in one line each,
    grouped by allow, ask and deny. Explain the evaluation order: deny, then ask, then
    allow, first match wins. Also explain that these rules are enforced by the Claude
    Code program itself, not by the model.
```json
{
  "permissions": {
    "allow": [
      "Bash(git status)", "Bash(git diff *)", "Bash(git log *)",
      "Bash(git add *)", "Bash(git commit *)", "Bash(git switch *)",
      "Bash(git pull *)", "Bash(git fetch *)",
      "Bash(.venv/bin/python -m pytest *)", "Bash(.venv/bin/python -m pytest)",
      "Bash(.venv/bin/ruff check *)", "Bash(.venv/bin/ruff check)",
      "Bash(gh pr view *)", "Bash(gh pr checks *)", "Bash(gh pr list *)"
    ],
    "ask": [
      "Bash(git push *)", "Bash(gh pr create *)", "Bash(gh issue create *)",
      "Bash(.venv/bin/pip install *)", "Bash(rm *)"
    ],
    "deny": [
      "Bash(git push --force *)", "Bash(git push -f *)",
      "Bash(git reset --hard *)", "Bash(gh pr merge *)",
      "Bash(gh api *)", "Bash(gh repo edit *)", "Bash(gh repo delete *)",
      "Read(./.env)", "Read(./.env.*)"
    ]
  }
}
```
4.2 [CLAUDE DOES] Create `CLAUDE.md`: branch names `feat/`, `fix/`, `chore/`;
    Conventional Commits; always run pytest and ruff via .venv before committing;
    open PRs as drafts with a "How I tested this" section; never push to main;
    never edit `.claude/`, `.github/` or `CLAUDE.md` unless explicitly asked.
4.3 [CLAUDE DOES] Create `.github/CODEOWNERS`: everything owned by the reviewer
    account (or me, if I have none), and `/.claude/`, `/CLAUDE.md`, `/.github/`
    explicitly owned by the reviewer. Explain "guard the guardrails": without this,
    any PR could quietly loosen the rules.
4.4 [CLAUDE DOES] Commit, then push and open the PR as a draft. Before each action,
    tell me whether you expect a prompt. Note that the new rules may not be active
    in this session until Claude Code restarts (Step 4.6), so whether the commit
    prompts depends on that; push and PR creation should prompt either way. Watch CI.
4.5 [YOU DO] Mark the PR ready (`gh pr ready`), get the reviewer's approval, squash
    merge, then `git switch main && git pull`.
4.6 [YOU DO] Exit Claude Code (`/exit`), then restart with `claude --continue` so the
    new settings load. CLAUDE DOES: re-read LAB_PROGRESS.md.
4.7 [YOU DO] Run `/permissions` and read the rules back. CLAUDE DOES: explain which
    file each rule came from, and the four scopes (managed, user, project, local).

# PHASE 5: CLAUDE DOES THE WORK UNDER THE RULES
Before starting, predict for me which of the next actions will prompt me and which
won't. Afterwards, compare what actually happened with the prediction.
5.1 [CLAUDE DOES] `git pull`, `git switch -c feat/format-currency`.
5.2 [CLAUDE DOES] Add `format_currency(amount: float, symbol: str = "$") -> str`
    (e.g. 1234.5 → "$1,234.50") plus 3 tests. File edits will prompt me (default
    mode). Tell me I could press Shift+Tab to switch to acceptEdits mode, and what
    that trades away.
5.3 [CLAUDE DOES] Run pytest and ruff: no prompts (allow list).
5.4 [CLAUDE DOES] Commit: no prompt. Show `git log -1` and point out any
    co-authored-by line, and explain that it's configurable and a team-policy
    decision.
5.5 [CLAUDE DOES] Push: prompt (ask list). Open a draft PR with a
    "How I tested this" section: prompt (ask list).
5.6 [YOU DO] Review the diff as the manager would (`gh pr diff`). CLAUDE DOES: give
    me a 5-point review checklist for AI-written PRs. Then ready, approve, squash
    merge, pull. Explain: the PR author (me) owns every line, whoever typed it.

# PHASE 6: POKE THE WALLS (one experiment per step; explain each result)
6.1 Ask yourself to merge the latest open PR, or if none, try
    `gh pr merge 999 --squash`. Expect DENY. Explain.
6.2 Try `git push --force origin HEAD`. Expect DENY.
6.3 [YOU DO] `echo "DEMO_SECRET=not-a-real-secret" > .env`. Then CLAUDE DOES:
    try to read `.env` with your Read tool. Expect DENY. Then explain honestly that
    a Read rule governs your file-reading tool, and that a shell command like
    `cat .env` is judged by the Bash rules instead. Here it isn't on any list, so
    it would fall to a prompt, and the human is the backstop. Do NOT actually run
    it. Lesson: deny lists are not a sandbox, so real secrets don't belong in the repo.
6.4 Defense in depth: [CLAUDE DOES] on main, make a trivial commit (allowed),
    then `git push origin main`. I'll APPROVE the ask prompt, and GitHub will
    still reject it. Explain: Gate 1 said yes, and Gate 2 still said no.
    Then try to clean up with `git reset --hard origin/main`: expect DENY.
    [YOU DO] run that reset myself. Explain why humans keep destructive commands.
6.5 [YOU DO] Press Shift+Tab until plan mode. Then ask you to "refactor calc.py into
    two modules". CLAUDE DOES: produce a plan only. Explain what plan mode is for
    (onboarding, risky refactors). Then I switch back to default mode.
6.6 Approval drift: [CLAUDE DOES] run `git branch -a` (not on any list). I'll choose
    "Yes, and don't ask again". Then I'll run `cat .claude/settings.local.json` and
    `git status`. Explain where the rule landed, why it's git-ignored, and why managers
    should review this drift periodically.

# PHASE 7: GUARD THE GUARDRAILS
7.1 [CLAUDE DOES] (I am explicitly asking you to edit .claude/ for this demo)
    `git switch -c chore/loosen-push`, move `Bash(git push *)` from ask to allow,
    commit, push, and open a PR titled "chore: stop asking before push".
7.2 [YOU DO] Open the PR in the browser. Show me that CODEOWNERS automatically
    requested the reviewer, and that the merge is blocked until they approve.
7.3 [YOU DO] As the reviewer: "Request changes" with a comment explaining why.
    Then close the PR without merging and delete the branch. Explain this is how
    a team stops a well-meaning change from weakening Gate 1.

# PHASE 8 (OPTIONAL): CLAUDE INSIDE GITHUB ACTIONS
Remind me this uses API credits.
8.1 [YOU DO] Inside Claude Code run `/install-github-app`, choose this repo, and
    follow the prompts (installs the Claude GitHub App, adds the ANTHROPIC_API_KEY
    secret, proposes the workflow). If it opens a PR with the workflow file, review
    and merge it through the normal gate. Explain which permissions the App requests.
8.2 [CLAUDE DOES] On `chore/tighten-action`, edit `.github/workflows/claude.yml`:
    (a) add an `if:` so it only runs when the comment contains `@claude` AND
    `github.event.comment.author_association` is OWNER, MEMBER or COLLABORATOR;
    (b) add `claude_args` with `--allowedTools` limited to reading files, editing
    files, git commands, and running pytest/ruff. Show me the diff and explain both
    changes (prompt injection, cost control). Commit, push, and open a PR. I review
    and merge.
8.3 [YOU DO] Create an issue: "@claude add a `tip_amount(total, tip_pct)` function
    with tests, following CLAUDE.md, and open a PR." Watch the Actions tab.
8.4 [YOU DO] When Claude's branch or PR appears, confirm it went through the SAME
    Gate 2: CI must pass, a code-owner approval is required, and a human merges.
    Explain: whether Claude runs on a laptop or in CI, it can't get around the gate.

# PHASE 9: THE ROLLBACK DRILL
9.1 Pretend `format_currency` caused an incident. [CLAUDE DOES] Find its squash
    commit, `git switch -c fix/revert-format-currency`, `git revert <sha>`, run
    tests, then push and open a PR. Explain why a revert (a new commit) beats
    rewriting history.
9.2 [YOU DO] Review, approve, merge, pull. Then walk me through a blameless
    postmortem question: which gate should have caught this, and why didn't it?

# PHASE 10: DEBRIEF
10.1 [CLAUDE DOES] Show `git log --oneline --graph --all`, and narrate the whole
     journey in one short paragraph per phase.
10.2 Give me a table: every action we took → which gate governed it → who approved.
10.3 Ask me 5 reflection questions an engineering manager should be able to answer
     after this lab (one at a time, and give feedback on my answers).
10.4 Cleanup [YOU DO]: delete `.env`; optionally delete the API key secret, uninstall
     the Claude GitHub App from the repo, and archive or delete the repo
     (`gh repo delete` needs the `delete_repo` scope, so do it in the web UI).

Start now with Phase 0, Step 0.1.
