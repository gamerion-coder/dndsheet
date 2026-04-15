## Project
dndsheet

## Current Status
Phase 1 Complete — Parser and Normalized Catalogs Ready

## Current Phase
Phase 1 Complete

## Current Focus
Phase 2: Building the Flask API and wizard pages.

## Last Concrete Result
- Normalized JSON catalogs generated for all 6 entity types.
- XML parsed: 1615 items, 449 spells, 127 feats, 15 races, 12 classes, 16 backgrounds.
- Translations framework (EN/PT) scaffolded.
- Initial single-file wizard (index.html) prototyped but not yet integrated.

## Active Blocker
None.

## Assumptions Currently in Force
- XML is the primary content source.
- English is canonical; Portuguese degrades to English gracefully.
- Flask + Jinja2 + vanilla JS is the agreed stack.
- The first version targets one printable 2024-compatible character sheet layout.

## Next Best Action
1. Set up Flask app skeleton (routes, config).
2. Wire normalized JSON catalogs into Flask API endpoints.
3. Replace the single-file index.html with proper Jinja2 builder pages.
4. Implement step validation in backend.
5. Build character JSON persistence to `exports/characters/`.

## Last Verification
2026-04-15 15:21 UTC — Parser ran successfully, generated catalogs verified.