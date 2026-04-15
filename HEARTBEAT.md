# HEARTBEAT.md

Project root:
`/home/torres/.openclaw/workspace/projects/dndsheet`

Read first:
- PROJECT.md
- SPEC.md
- STATE.md
- BACKLOG.md

## Heartbeat Purpose
This heartbeat is for project supervision and disciplined continuation inside this project only.

## Rules
- Stay inside the `dndsheet` project directory.
- Do not touch unrelated projects in the shared workspace.
- Do not report progress unless a concrete change, file, or verification exists.
- Do not mark work complete unless the artifact exists and the relevant check passed.

## Heartbeat Checklist
1. Is the repo or project folder in a coherent state?
2. Is there a highest-priority unblocked task in BACKLOG.md?
3. Is there an active blocker recorded in STATE.md that still needs escalation?
4. Did the last work cycle leave uncommitted or unexplained changes?
5. Is there a small, safe, bounded action that can be completed now?

## Action Policy
If a safe bounded task is available, do exactly one of the following:
- scaffold one missing file/module
- implement one small parsing or validation unit
- add one focused test
- update one piece of documentation
- run one relevant verification command

Then:
- update STATE.md
- update BACKLOG.md if status changed

## Silence Policy
Reply `HEARTBEAT_OK` only if:
- no safe bounded task is available, or
- the project is blocked and already documented, or
- there is nothing new to report

## Escalation Policy
Send a concise status update only when:
- XML ambiguity blocks parser work
- rules ambiguity blocks validation
- print/render target is underspecified
- a verification command fails
- a meaningful milestone was completed
