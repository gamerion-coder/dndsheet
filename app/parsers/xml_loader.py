"""XML Loader - parses the raw reference XML into Python objects."""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator


class XmlLoader:
    """Loads and iterates over entities in the reference XML."""

    def __init__(self, xml_path: str | Path):
        self.xml_path = Path(xml_path)
        self.tree = ET.parse(self.xml_path)
        self.root = self.tree.getroot()

    def iter_items(self) -> Iterator[ET.Element]:
        """Yield all <item> elements (weapons, armor, gear, etc.)."""
        for item in self.root.findall('item'):
            yield item

    def iter_spells(self) -> Iterator[ET.Element]:
        """Yield all <spell> elements."""
        for spell in self.root.findall('spell'):
            yield spell

    def iter_feats(self) -> Iterator[ET.Element]:
        """Yield all <feat> elements."""
        for feat in self.root.findall('feat'):
            yield feat

    def iter_races(self) -> Iterator[ET.Element]:
        """Yield all <race> elements."""
        for race in self.root.findall('race'):
            yield race

    def iter_classes(self) -> Iterator[ET.Element]:
        """Yield all <class> elements."""
        for cls in self.root.findall('class'):
            yield cls

    def iter_backgrounds(self) -> Iterator[ET.Element]:
        """Yield all <background> elements."""
        for bg in self.root.findall('background'):
            yield bg

    def iter_monsters(self) -> Iterator[ET.Element]:
        """Yield all <monster> elements."""
        for monster in self.root.findall('monster'):
            yield monster

    def stats(self) -> dict:
        """Return counts of each entity type."""
        return {
            'items': len(self.root.findall('item')),
            'spells': len(self.root.findall('spell')),
            'feats': len(self.root.findall('feat')),
            'races': len(self.root.findall('race')),
            'classes': len(self.root.findall('class')),
            'backgrounds': len(self.root.findall('background')),
            'monsters': len(self.root.findall('monster')),
        }