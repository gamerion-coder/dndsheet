"""XML Normalizer - converts raw XML elements into normalized JSON structures."""
import re
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from .xml_loader import XmlLoader


def clean_text(text: str | None) -> str:
    """Remove extra whitespace from text."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def slugify(name: str) -> str:
    """Convert a name into a URL-safe slug."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def parse_modifiers(item: ET.Element) -> list[dict]:
    """Parse <modifier> children from an item element."""
    modifiers = []
    for mod in item.findall('modifier'):
        modifiers.append({
            'category': mod.get('category', ''),
            'text': clean_text(mod.text or '')
        })
    return modifiers


def normalize_item(item: ET.Element) -> dict[str, Any]:
    """Normalize a single <item> element."""
    name = clean_text(item.findtext('name', ''))
    item_type = clean_text(item.findtext('type', ''))
    dmg1 = item.findtext('dmg1', '')
    dmg2 = item.findtext('dmg2', '')
    dmgType = item.findtext('dmgType', '')

    entry = {
        'id': f"item-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'type': item_type,
        'magic': item.findtext('magic', '') == '1',
        'weight': item.findtext('weight', ''),
        'value': item.findtext('value', ''),
        'text': [clean_text(t.text) for t in item.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in item.findall('text') if t.text and 'Source:' in t.text), '')),
        'modifier': parse_modifiers(item),
    }

    # Damage block (only for weapons)
    if dmg1 or dmg2:
        entry['damage'] = {
            'dmg1': dmg1,
            'dmg2': dmg2,
            'dmgType': dmgType,
        }

    # Weapon properties
    prop = item.findtext('property', '')
    if prop:
        entry['property'] = prop.split(',')

    # Armor class
    ac = item.findtext('ac', '')
    if ac:
        entry['ac'] = ac

    # Stealth penalty
    stealth = item.findtext('stealth', '')
    if stealth:
        entry['stealth'] = stealth

    # Strength requirement
    strength = item.findtext('strength', '')
    if strength:
        entry['strength'] = strength

    # Range
    range_val = item.findtext('range', '')
    if range_val:
        entry['range'] = range_val

    # Detail
    detail = item.findtext('detail', '')
    if detail:
        entry['detail'] = detail

    return entry


def normalize_spell(spell: ET.Element) -> dict[str, Any]:
    """Normalize a single <spell> element."""
    name = clean_text(spell.findtext('name', ''))
    entry = {
        'id': f"spell-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'level': spell.findtext('level', ''),
        'school': spell.findtext('school', ''),
        'casttime': spell.findtext('casttime', ''),
        'range': spell.findtext('range', ''),
        'component': spell.findtext('component', ''),
        'material': spell.findtext('material', ''),
        'duration': spell.findtext('duration', ''),
        'classes': spell.findtext('classes', ''),
        'text': [clean_text(t.text) for t in spell.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in spell.findall('text') if t.text and 'Source:' in t.text), '')),
    }
    return entry


def normalize_feat(feat: ET.Element) -> dict[str, Any]:
    """Normalize a single <feat> element."""
    name = clean_text(feat.findtext('name', ''))
    entry = {
        'id': f"feat-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'prerequisite': clean_text(feat.findtext('prerequisite', '')),
        'text': [clean_text(t.text) for t in feat.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in feat.findall('text') if t.text and 'Source:' in t.text), '')),
    }
    return entry


def normalize_race(race: ET.Element) -> dict[str, Any]:
    """Normalize a single <race> element."""
    name = clean_text(race.findtext('name', ''))
    entry = {
        'id': f"race-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'speed': race.findtext('speed', ''),
        'ability': clean_text(race.findtext('ability', '')),
        'text': [clean_text(t.text) for t in race.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in race.findall('text') if t.text and 'Source:' in t.text), '')),
    }
    return entry


def normalize_class(cls: ET.Element) -> dict[str, Any]:
    """Normalize a single <class> element."""
    name = clean_text(cls.findtext('name', ''))
    entry = {
        'id': f"class-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'hd': cls.findtext('hd', ''),
        'spellcast': cls.findtext('spellcast', ''),
        'text': [clean_text(t.text) for t in cls.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in cls.findall('text') if t.text and 'Source:' in t.text), '')),
    }
    return entry


def normalize_background(bg: ET.Element) -> dict[str, Any]:
    """Normalize a single <background> element."""
    name = clean_text(bg.findtext('name', ''))
    entry = {
        'id': f"bg-{slugify(name)}",
        'slug': slugify(name),
        'name': name,
        'text': [clean_text(t.text) for t in bg.findall('text') if clean_text(t.text)],
        'source': clean_text(next((t.text for t in bg.findall('text') if t.text and 'Source:' in t.text), '')),
    }
    return entry


def normalize_all(xml_path: str | Path, output_dir: str | Path) -> dict[str, int]:
    """Parse and normalize all entity types, save as JSON, return counts."""
    loader = XmlLoader(xml_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    counts = {}

    # Items
    items = [normalize_item(i) for i in loader.iter_items()]
    Path(output_dir / 'equipment.json').write_text(json.dumps(items, indent=2, ensure_ascii=False))
    counts['equipment'] = len(items)

    # Spells
    spells = [normalize_spell(s) for s in loader.iter_spells()]
    Path(output_dir / 'spells.json').write_text(json.dumps(spells, indent=2, ensure_ascii=False))
    counts['spells'] = len(spells)

    # Feats
    feats = [normalize_feat(f) for f in loader.iter_feats()]
    Path(output_dir / 'feats.json').write_text(json.dumps(feats, indent=2, ensure_ascii=False))
    counts['feats'] = len(feats)

    # Races
    races = [normalize_race(r) for r in loader.iter_races()]
    Path(output_dir / 'races.json').write_text(json.dumps(races, indent=2, ensure_ascii=False))
    counts['races'] = len(races)

    # Classes
    classes = [normalize_class(c) for c in loader.iter_classes()]
    Path(output_dir / 'classes.json').write_text(json.dumps(classes, indent=2, ensure_ascii=False))
    counts['classes'] = len(classes)

    # Backgrounds
    backgrounds = [normalize_background(b) for b in loader.iter_backgrounds()]
    Path(output_dir / 'backgrounds.json').write_text(json.dumps(backgrounds, indent=2, ensure_ascii=False))
    counts['backgrounds'] = len(backgrounds)

    return counts