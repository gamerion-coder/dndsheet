import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DATABASE = '/home/gamerion_agent/.openclaw/shared-workspace/dndsheet/data/dndsheet.db'

def init_db():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                race TEXT,
                class TEXT,
                level INTEGER,
                strength INTEGER,
                dexterity INTEGER,
                constitution INTEGER,
                intelligence INTEGER,
                wisdom INTEGER,
                charisma INTEGER,
                hp INTEGER,
                ac INTEGER,
                inventory TEXT
            )
        ''')
        conn.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from flask import g # Import g to use with get_db

init_db() # Initialize the database when the app starts

@app.route('/characters', methods=['POST'])
def create_character():
    character_data = request.json
    if not character_data:
        return jsonify({"error": "Invalid character data"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO characters (name, race, class, level, strength, dexterity, constitution, intelligence, wisdom, charisma, hp, ac, inventory)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                character_data.get('name', ''),
                character_data.get('race', ''),
                character_data.get('class', ''),
                character_data.get('level', 0),
                character_data.get('strength', 0),
                character_data.get('dexterity', 0),
                character_data.get('constitution', 0),
                character_data.get('intelligence', 0),
                character_data.get('wisdom', 0),
                character_data.get('charisma', 0),
                character_data.get('hp', 0),
                character_data.get('ac', 0),
                character_data.get('inventory', '')
            )
        )
        conn.commit()
        return jsonify({"id": cursor.lastrowid, "message": "Character created successfully"}), 201
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/characters', methods=['GET'])
def get_all_characters():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    characters = cursor.fetchall()
    return jsonify([dict(row) for row in characters]), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
    character = cursor.fetchone()
    if character:
        return jsonify(dict(character)), 200
    return jsonify({"error": "Character not found"}), 404

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character_data = request.json
    if not character_data:
        return jsonify({"error": "Invalid character data"}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    # Check if character exists
    cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
    existing_character = cursor.fetchone()
    if not existing_character:
        return jsonify({"error": "Character not found"}), 404

    try:
        update_fields = []
        update_values = []
        for key, value in character_data.items():
            if key in ['name', 'race', 'class', 'level', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'hp', 'ac', 'inventory']: # Whitelist allowed fields
                update_fields.append(f"{key} = ?")
                update_values.append(value)
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        update_values.append(character_id)
        
        cursor.execute(
            f"UPDATE characters SET {', '.join(update_fields)} WHERE id = ?",
            tuple(update_values)
        )
        conn.commit()
        return jsonify({"message": "Character updated successfully"}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        if cursor.rowcount > 0:
            conn.commit()
            return jsonify({"message": "Character deleted successfully"}), 204
        else:
            return jsonify({"error": "Character not found"}), 404
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/_render_character_display/<int:character_id>')
def _render_character_display(character_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
    character = cursor.fetchone()
    if character:
        return render_template('_character_display.html', character=dict(character))
    return "Character not found", 404

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM characters")
    characters = cursor.fetchall()
    return render_template('index.html', characters=[dict(row) for row in characters])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
