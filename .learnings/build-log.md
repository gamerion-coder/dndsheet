# D&D 5e Character Sheet - Build Log

## Context
- Building a D&D 5e Character Sheet web app (2024 PHB rules)
- Data file: `dnd_data_model.json` contains 1615 items (weapons, armor, spells, magic items, etc.)
- Missing from JSON: character creation data (races, classes, subclasses, skills, backgrounds, alignments, etc.)
- Solution: Hardcode character creation elements; use JSON for equipment/spells

## Key Decisions
1. Single HTML file with embedded CSS/JS
2. Vanilla JS (no frameworks)
3. Hardcode races, classes, subclasses, skills, backgrounds, alignments per 5e 2024 rules
4. Use JSON for equipment selection
5. i18n system for EN/PT toggle
6. Wizard → Character Sheet flow
7. Print CSS for PDF output
