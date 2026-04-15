"""Flask routes for dndsheet."""
import json
import uuid
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, send_from_directory


api = Blueprint('api', __name__)

# Paths relative to project root
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'normalized'
EXPORTS_DIR = BASE_DIR / 'exports' / 'characters'


def load_catalog(name: str) -> list[dict]:
    """Load a normalized JSON catalog."""
    path = DATA_DIR / f'{name}.json'
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8'))


def load_translations(locale: str = 'en') -> dict:
    """Load translation file for a locale."""
    path = DATA_DIR / f'translations.{locale}.json'
    if not path.exists():
        path = DATA_DIR / 'translations.en.json'
    return json.loads(path.read_text(encoding='utf-8'))


# ─── HTML Routes ────────────────────────────────────────────────────────────

def create_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/builder')
    def builder():
        lang = request.args.get('lang', 'en')
        return render_template('builder.html', lang=lang)

    @app.route('/sheet/<character_id>')
    def sheet(character_id: str):
        path = EXPORTS_DIR / f'{character_id}.json'
        if not path.exists():
            return "Character not found", 404
        character = json.loads(path.read_text(encoding='utf-8'))
        lang = character.get('meta', {}).get('locale', 'en')
        translations = load_translations(lang)
        return render_template('sheet.html', character=character, t=translations)

    @app.route('/favicon.png')
    def favicon():
        return send_from_directory(BASE_DIR / 'app' / 'static', 'favicon.png')

    # ─── API Routes ─────────────────────────────────────────────────────────

    @api.route('/api/catalog/<catalog_name>')
    def catalog(catalog_name: str):
        """Return normalized catalog."""
        data = load_catalog(catalog_name)
        return jsonify(data)

    @api.route('/api/translations/<locale>')
    def translations(locale: str):
        """Return translation file."""
        return jsonify(load_translations(locale))

    @api.route('/api/character/validate-step', methods=['POST'])
    def validate_step():
        """Validate a wizard step submission."""
        body = request.get_json()
        step = body.get('step')
        data = body.get('data', {})

        # Basic step validation
        if step == 1:
            if not data.get('species'):
                return jsonify({'valid': False, 'error': 'Species required'}), 400
            if not data.get('alignment'):
                return jsonify({'valid': False, 'error': 'Alignment required'}), 400
        elif step == 2:
            for attr in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
                val = data.get(attr, 0)
                if not isinstance(val, int) or val < 1 or val > 30:
                    return jsonify({'valid': False, 'error': f'Invalid {attr}'}), 400
        elif step == 3:
            if not data.get('characterClass'):
                return jsonify({'valid': False, 'error': 'Class required'}), 400
        elif step == 6:
            level = data.get('level', 0)
            if not isinstance(level, int) or level < 1 or level > 20:
                return jsonify({'valid': False, 'error': 'Level must be 1-20'}), 400
        elif step == 7:
            level = data.get('level', 1)
            subclass = data.get('subclass')
            if level < 3 and subclass:
                return jsonify({'valid': False, 'error': 'Subclass available at level 3+'}), 400

        return jsonify({'valid': True})

    @api.route('/api/character/export-json', methods=['POST'])
    def export_json():
        """Persist final character as JSON."""
        body = request.get_json()
        character = body.get('character', {})

        # Ensure meta
        if 'meta' not in character:
            character['meta'] = {}
        character['meta']['character_id'] = str(uuid.uuid4())
        character['meta']['created_at'] = __import__('datetime').datetime.now().isoformat()
        character['meta']['ruleset'] = 'dnd-5e-2024'

        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        char_id = character['meta']['character_id']
        path = EXPORTS_DIR / f'{char_id}.json'
        path.write_text(json.dumps(character, indent=2, ensure_ascii=False), encoding='utf-8')

        return jsonify({'character_id': char_id, 'url': f'/sheet/{char_id}'})

    @api.route('/api/character/<character_id>')
    def get_character(character_id: str):
        """Retrieve a saved character."""
        path = EXPORTS_DIR / f'{character_id}.json'
        if not path.exists():
            return jsonify({'error': 'Not found'}), 404
        return jsonify(json.loads(path.read_text(encoding='utf-8')))