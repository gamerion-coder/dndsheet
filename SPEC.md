# SPEC.md

## Product Summary
dndsheet is a guided character builder for D&D 5e (2024).
The builder consumes a user-provided XML reference, normalizes it into JSON catalogs, lets the user create a character step by step, and renders the final JSON into a printable HTML sheet.

## Recommended Stack
- Python 3.11+
- Flask or FastAPI for backend routes
- Jinja2 for HTML rendering
- vanilla JavaScript for wizard UI
- pytest for tests

Preferred initial choice:
- Flask + Jinja2 + vanilla JS

Reason:
- simple
- easy to debug
- fits a shared workspace
- no unnecessary frontend framework complexity

## Folder Layout
```text
dndsheet/
  PROJECT.md
  SPEC.md
  BACKLOG.md
  STATE.md
  HEARTBEAT.md

  data/
    raw/
      reference.xml
    normalized/
      species.json
      alignments.json
      classes.json
      subclasses.json
      backgrounds.json
      skills.json
      feats.json
      spells.json
      equipment.json
      translations.pt-BR.json
      translations.en.json

  app/
    __init__.py
    routes.py
    services/
      builder_service.py
      render_service.py
      validation_service.py
      translation_service.py
    parsers/
      xml_loader.py
      xml_normalizer.py
    rules/
      eligibility.py
      derived_stats.py
      spell_rules.py
      feat_rules.py
    templates/
      base.html
      builder.html
      sheet.html
    static/
      css/
        app.css
        print.css
      js/
        builder.js

  tests/
    test_xml_loader.py
    test_normalizer.py
    test_validation.py
    test_spell_rules.py
    test_feat_rules.py

  exports/
    characters/
```

## Functional Scope

### 1. XML Ingestion
The XML must be parsed into normalized catalogs with stable IDs.

The parser must:
- preserve source identifiers where possible
- normalize names and option structures
- emit deterministic JSON
- record parsing warnings
- avoid silently dropping unknown fields

### 2. Bilingual Support
Use canonical IDs for all entities.
Store localized names and text separately.

Each domain object should support:
- `id`
- `slug`
- `name`
- `i18n`
- `source`
- `rules`
- `metadata`

Example:
```json
{
  "id": "species-human",
  "slug": "human",
  "name": "Human",
  "i18n": {
    "en": {
      "name": "Human"
    },
    "pt-BR": {
      "name": "Humano"
    }
  },
  "source": {
    "type": "xml",
    "ref": "species/human"
  }
}
```

### 3. Wizard Flow
The wizard must support the following ordered screens:

1. species + alignment
2. ability scores
3. class
4. skills
5. background
6. level
7. subclass
8. feats
9. spells
10. equipment
11. summary/review
12. export/render

### 4. Rules and Validation
Validation must be centralized in backend services.
Frontend validation is only for convenience.

Minimum validation rules:
- level must be integer and within allowed range
- subclass is unavailable when level < 3
- feat choices must respect level and prerequisites
- spell choices must respect class, level, and eligibility
- skill choices must enforce allowed counts and domain restrictions
- equipment choices must be internally consistent
- derived values must be computed from canonical stats, not free text

### 5. Final JSON Output
The final character JSON should contain:
- metadata
- locale
- ruleset version
- selected options
- ability scores
- proficiencies
- spells
- equipment
- derived sheet values
- audit trail of sources

Suggested shape:
```json
{
  "meta": {
    "character_id": "uuid-or-slug",
    "created_at": "ISO-8601",
    "updated_at": "ISO-8601",
    "locale": "pt-BR",
    "ruleset": "dnd-5e-2024",
    "source_priority": ["xml", "official-open-reference"]
  },
  "character": {
    "name": "",
    "alignment": "",
    "species": {
      "id": "",
      "label": ""
    },
    "class": {
      "id": "",
      "label": ""
    },
    "subclass": {
      "id": "",
      "label": ""
    },
    "background": {
      "id": "",
      "label": ""
    },
    "level": 1
  },
  "abilities": {
    "strength": 10,
    "dexterity": 10,
    "constitution": 10,
    "intelligence": 10,
    "wisdom": 10,
    "charisma": 10
  },
  "skills": [],
  "feats": [],
  "spells": {
    "known": [],
    "prepared": [],
    "slots": {}
  },
  "equipment": [],
  "derived": {
    "proficiency_bonus": 2,
    "initiative": 0,
    "passive_perception": 10,
    "armor_class": null,
    "hit_points": null,
    "speed": null,
    "spell_save_dc": null,
    "spell_attack_bonus": null
  },
  "audit": {
    "xml_refs": [],
    "warnings": []
  }
}
```

## API / Route Sketch

### HTML routes
- `GET /` -> builder start
- `GET /builder`
- `GET /sheet/<character_id>`

### JSON routes
- `GET /api/catalog/<domain>`
- `POST /api/character/validate-step`
- `POST /api/character/render`
- `POST /api/character/export-json`

## Rendering Requirements
The final sheet renderer must:
- consume only the final JSON object
- not depend on wizard state
- use Jinja2 templates
- support English and Portuguese labels
- have a dedicated print stylesheet
- include a print button that triggers browser print

## Translation Rules
- English is the canonical fallback
- Portuguese keys should be `pt-BR`
- translation gaps must degrade gracefully to English
- no duplicated rule logic per language

## Development Phases

### Phase 1
- inspect XML
- define normalized schema
- build parser
- export normalized catalogs

### Phase 2
- implement wizard pages and API endpoints
- implement validation services
- persist character JSON to `exports/characters/`

### Phase 3
- implement HTML sheet renderer
- implement print stylesheet
- finalize bilingual UI

### Phase 4
- add tests
- refine edge cases
- document assumptions and limitations

## Non-Goals for First Version
- multiplayer/session accounts
- cloud persistence
- campaign management
- live dice rolling
- inventory economics
- homebrew editor
- monster or NPC builder

## Known Risk Areas
- XML ambiguity
- incomplete translation coverage
- spell eligibility complexity
- feat prerequisite modeling
- deriving AC/HP/speed consistently from partial source data
- matching the visual layout of the desired 2024 sheet without an exact reference artifact

## Definition of Done
Done means:
- parser works on the provided XML
- user can complete the wizard
- JSON exports cleanly
- rendered sheet is readable and printable
- tests cover parser and core rules
- STATE.md reflects current truth
