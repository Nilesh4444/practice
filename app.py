from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'medicines.db'

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/medicine', methods=['POST'])
def add_medicine():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medicines (
            generic_name, brand_name, drug_class, purpose, 
            recommended_dosage, administration_route, max_daily_dose, 
            special_instructions, common_side_effects, less_common_side_effects, 
            severe_side_effects, drug_interactions, warnings, 
            storage_instructions, faq
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['generic_name'], data['brand_name'], data['drug_class'], data['purpose'],
        data['recommended_dosage'], data['administration_route'], data['max_daily_dose'],
        data['special_instructions'], data['common_side_effects'], data['less_common_side_effects'],
        data['severe_side_effects'], data['drug_interactions'], data['warnings'],
        data['storage_instructions'], data['faq']
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Medicine added successfully!"})

@app.route('/medicine/<string:generic_name>', methods=['GET'])
def get_medicine(generic_name):
    conn = get_db_connection()
    medicine = conn.execute('SELECT * FROM medicines WHERE generic_name = ?', (generic_name,)).fetchone()
    conn.close()
    if medicine:
        return jsonify(dict(medicine))
    return jsonify({"error": "Medicine not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
