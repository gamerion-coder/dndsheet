# PROJECT.md

## Project
dndsheet

## Root
/home/torres/.openclaw/workspace/projects/dndsheet

## Objective
Build a web application that lets a user create and inspect a D&D 5e (2024) character sheet from a guided interactive flow, using the provided XML as the main reference source.

The app must:
- support English and Portuguese
- store the final character as JSON
- render the final JSON into an HTML character sheet
- provide a print-to-PDF flow from the rendered sheet

## Core Product Requirements
The character creation flow must be interactive and follow these steps:

1. choose race/species and alignment
2. assign starting attributes
3. choose class
4. choose skills
5. choose background
6. choose level
7. choose subclass if level >= 3
8. choose feats/talents according to level and eligibility
9. choose spells according to level, class, and eligibility
10. add equipment

## Terminology Policy
Internally, use 2024 canonical terminology:
- species
- class
- subclass
- background
- feat
- spell
- equipment
- ability scores

UI labels may expose aliases when useful:
- "Race / Species"
- "Talents / Feats"

Do not fork business logic by language. Keep one canonical data model and translate labels/content through i18n fields.

## Source-of-Truth Policy
Priority order:
1. User-provided XML
2. Official open 2024 references for validation and missing general rules
3. 5etools only as a developer convenience for lookup, never as authoritative persisted source

Do not silently invent options not present in the XML unless explicitly marked as externally sourced and approved.

## Data Model Policy
The final character must be persisted as JSON.
The JSON is the primary runtime artifact.
HTML is a rendered view of the JSON.
PDF is produced from the rendered HTML via browser print flow.

## Architecture Policy
Prefer a simple, maintainable stack:
- Python backend
- Jinja2 templates for HTML sheet rendering
- lightweight frontend JS for wizard interactions
- normalized JSON catalogs generated from the XML

Avoid overengineering.
Do not introduce a database unless the project later requires persistence beyond flat files.

## Workspace Boundary
This is a shared workspace.
Operate only inside:
- /home/torres/.openclaw/workspace/projects/dndsheet/**

Do not edit unrelated projects.
Do not move or rewrite global agent files from inside this project.
Do not read from other project folders unless explicitly instructed.

## Deliverables
- XML ingestion/parsing pipeline
- normalized JSON content catalogs
- bilingual labels/content layer
- character creation wizard
- validation/rules layer
- final character JSON export
- HTML sheet renderer
- print stylesheet and print button
- project documentation
- tests for parser and rules-critical paths

## Acceptance Criteria
The project is acceptable only when all of the following are true:

1. A user can complete the full 10-step creation flow.
2. English and Portuguese are both available from the same canonical data.
3. Validation prevents illegal selections.
4. The resulting character is saved as a coherent JSON document.
5. The JSON renders into a readable D&D 2024-style HTML sheet.
6. The HTML sheet prints cleanly to PDF.
7. The parser and rules engine have basic automated tests.
8. Project state is documented in STATE.md and backlog is kept current.

## Working Mode
On each work cycle:
1. Read PROJECT.md, SPEC.md, STATE.md, and BACKLOG.md.
2. Pick one bounded, highest-priority unblocked task.
3. Make the smallest coherent change that moves the project forward.
4. Verify it.
5. Update STATE.md.
6. Update BACKLOG.md.

## Guardrails
Do not:
- scrape or embed copyrighted rule text beyond what is allowed by the source policy
- guess XML semantics without documenting the assumption
- change unrelated files in the shared workspace
- claim completion without a concrete artifact or passing check

## Escalate When
Escalate instead of guessing when:
- XML structure is ambiguous
- eligibility logic is unclear or contradictory
- bilingual mapping is underdetermined
- a rule depends on non-open content not present in XML
- print layout cannot match the target structure without a concrete reference sheet
