from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
# Importing the new db_manager and aliasing it to 'database' to minimize code changes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import conn as database


app = Flask(__name__)
CORS(app)

# Initialize database on startup with error catching
try:
    database.init_db()
except Exception as e:
    print(f"Startup DB Error: {e}")

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    conn, error = database.get_db_connection()
    if not conn:
        return jsonify({"error": f"Oracle Connection Failed: {error}"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID, NAME, EMAIL, COURSE FROM STUDENTS ORDER BY ID DESC")
        students = []
        for row in cursor.fetchall():
            students.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "course": row[3]
            })
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": f"Oracle Query Error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')
    
    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400
    
    conn, error = database.get_db_connection()
    if not conn:
        return jsonify({"error": f"Oracle Connection Failed: {error}"}), 500
    
    cursor = conn.cursor()
    try:
        # 11g compatible insert (ID is handled by trigger)
        cursor.execute(
            "INSERT INTO STUDENTS (NAME, EMAIL, COURSE) VALUES (:1, :2, :3)",
            (name, email, course)
        )
        conn.commit()
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Oracle Insert Error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')
    
    conn, error = database.get_db_connection()
    if not conn:
        return jsonify({"error": f"Oracle Connection Failed: {error}"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE STUDENTS SET NAME = :1, EMAIL = :2, COURSE = :3 WHERE ID = :4",
            (name, email, course, student_id)
        )
        conn.commit()
        return jsonify({"message": "Student updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn, error = database.get_db_connection()
    if not conn:
        return jsonify({"error": f"Oracle Connection Failed: {error}"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM STUDENTS WHERE ID = :1", (student_id,))
        conn.commit()
        return jsonify({"message": "Student deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
