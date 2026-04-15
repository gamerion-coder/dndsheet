# BACKLOG.md

## P0 - Foundation
- [x] Create project folder structure
- [x] Add Python app scaffold
- [x] Add parser scaffold
- [x] Place XML under `data/raw/reference.xml`
- [x] Inspect XML structure and document mappings
- [x] Define normalized schemas for all core domains

## P1 - Data Normalization
- [ ] Normalize species/race data
- [ ] Normalize alignments
- [ ] Normalize classes
- [ ] Normalize subclasses
- [ ] Normalize skills
- [ ] Normalize backgrounds
- [ ] Normalize feats/talents
- [ ] Normalize spells
- [ ] Normalize equipment
- [ ] Build translation dictionaries for `en` and `pt-BR`

## P2 - Rules Layer
- [ ] Implement step validation service
- [ ] Implement level gating
- [ ] Implement subclass gating at level >= 3
- [ ] Implement feat prerequisite logic
- [ ] Implement spell eligibility logic
- [ ] Implement derived stat calculations

## P3 - Builder UI
- [ ] Build wizard shell
- [ ] Build step 1 species + alignment
- [ ] Build step 2 ability scores
- [ ] Build step 3 class
- [ ] Build step 4 skills
- [ ] Build step 5 background
- [ ] Build step 6 level
- [ ] Build step 7 subclass
- [ ] Build step 8 feats
- [ ] Build step 9 spells
- [ ] Build step 10 equipment
- [ ] Build review/export screen

## P4 - Rendering
- [ ] Design Jinja sheet template
- [ ] Render final JSON into HTML
- [ ] Add bilingual sheet labels
- [ ] Add print stylesheet
- [ ] Add print button

## P5 - Quality
- [ ] Add parser tests
- [ ] Add normalization tests
- [ ] Add validation tests
- [ ] Add spell logic tests
- [ ] Add feat logic tests
- [ ] Add one end-to-end character creation test

## P6 - Documentation
- [ ] Document XML assumptions
- [ ] Document route/API usage
- [ ] Document JSON schema
- [ ] Document known limitations

## Blocked / Needs Clarification
- [ ] Exact XML structure unknown until inspected
- [ ] Exact target sheet layout not yet attached here
- [ ] Rule gaps outside XML may require explicit approval
