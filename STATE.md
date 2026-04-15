# STATE.md

## Project
dndsheet

## Current Status
Not started

## Current Phase
Foundation

## Current Focus
Prepare the project scaffold and inspect the XML into a normalized schema plan.

## Last Concrete Result
None yet.

## Active Blocker
The actual XML structure has not yet been inspected in this project context.

## Assumptions Currently in Force
- XML is the primary content source.
- The final artifact is a JSON-backed HTML sheet.
- English and Portuguese must come from the same canonical data.
- Jinja2 is the preferred renderer.
- The first version targets one printable 2024-compatible character sheet layout.

## Next Best Action
1. place the XML in `data/raw/reference.xml`
2. inspect its top-level entities and nesting
3. draft the normalization map for species, classes, subclasses, skills, backgrounds, feats, spells, and equipment
4. scaffold the parser

## Last Verification
Not available yet.

## Notes
Do not claim rules completeness until the XML has been parsed and compared against the open 2024 references.
