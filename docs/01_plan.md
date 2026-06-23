# 01. Project Plan

## 1. Summary
This section defines how the team will divide work, track progress, and deliver this project. It prescribes roles, sprint cadence, issue/PR workflow, and quality checks so everyone can coordinate reliably.

## 2. Roles & Responsibilities
- **Project Manager (PM):** Prioritize backlog, maintain milestones, run standups, and coordinate acceptance criteria.
- **Tech Lead:** Define architecture, approve design decisions, assign technical tasks, and lead code reviews.
- **Backend/Engine Developer(s):** Implement core data model, storage, and CLI commands.
- **Frontend/UX Developer(s):** (If applicable) Design simple UI views or improve CLI UX and formatting.
- **QA / Tester:** Create and run acceptance tests, maintain test plans, and validate releases.
- **Documenter:** Keep `docs/` current with intended use, API, and deployment steps.

## 3. Work Division
- Break work into small issues (1–3 days each) and tag with component labels (infra, core, cli, docs, test).
- Assign each issue to a single owner; owners open feature branches named `feat/<issue-number>-short-desc`.
- Use pull requests for all non-trivial changes; PRs require at least one approving review from the Tech Lead or another developer.

## 4. Tracking & Tools
- **Version Control:** Git with protected `main` branch; use topic branches per issue.
- **Issue Tracking:** GitHub Issues (or Jira) for backlog, with Milestones for sprints/releases.
- **Board:** Use GitHub Projects (Kanban) to track To Do / In Progress / In Review / Done.
- **CI:** Configure continuous integration to run unit and integration tests on PRs.
- **Labels & Templates:** Provide issue and PR templates; use labels like `priority/low|med|high`, `type/bug|feat|chore`.

## 5. Cadence & Meetings
- **Sprints:** 1–2 week sprints depending on course schedule. Define sprint goals in Milestones.
- **Standups:** 10–15 minute async or synchronous standups 2–3 times per week.
- **Planning/Retro:** Sprint planning before each sprint; short retrospective at sprint end.

## 6. Definition of Done
- Code merged to `main` with passing CI.
- Issue acceptance criteria met and verified by QA.
- Documentation updated (if public-facing change).

## 7. Artifacts & Deliverables
- Issue list and sprint Milestones.
- Pull requests with linked issues and review comments.
- Test reports from CI and manual acceptance test notes.

This plan gives a clear, lightweight process for dividing tasks and tracking progress across the team while ensuring code quality and traceability.