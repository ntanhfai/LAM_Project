import json

from flask import Flask, render_template, request, jsonify
import sqlite3
import models

app = Flask(__name__)
DATABASE = 'LAMdatabase.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_custom():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Custom")
    custom_list = cursor.fetchall()
    conn.close()
    return custom_list


def dict_factory( cursor, row, table):
    """Converts SQLite row to a dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        # d[col[0]] = row[idx]

        if 'id' in col[0].lower():
            d['id'] = row[idx]
        if 'name' in col[0].lower():
            d['name'] = row[idx]
    return d


# @app.route('/get_custom', methods=['POST', 'GET'])
# def get_custom_data():
#     conn = get_db_connection()
#     conn.row_factory = dict_factory  # Set the row_factory to convert rows to dictionaries
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Custom")
#     custom_list = cursor.fetchall()
#     conn.close()
#     ret = jsonify(custom_list)
#     return ret


@app.route('/')
def index():
    custom_list = get_custom()
    html_Projects = render_template("Modules/Module_Projects.html")
    return render_template('index.html', custom_list=custom_list)


@app.route('/data', methods=['POST'])
def process_data():
    data = request.form
    table = data['table']
    action = data['action']
    conn = get_db_connection()
    cursor = conn.cursor()

    if action == 'loadall':
        conn = get_db_connection()
        # conn.row_factory = dict_factory  # Set the row_factory to convert rows to dictionaries
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        custom_list = cursor.fetchall()
        conn.close()
        data_array = [list(row) for row in custom_list]
        json_data = json.dumps(data_array)
        print(json_data)
        # ret = jsonify(custom_list)
        return json_data

    if table == 'Custom':
        if action == 'add':
            custom_name = data['new_name']
            cursor.execute("INSERT INTO Custom (name_custom) VALUES (?)", (custom_name,))
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return jsonify({'message': 'Record added successfully', 'row_id': row_id})
        elif action == 'update':
            query = f"UPDATE Custom SET name_custom = '{data['new_name']}' WHERE id_custom = {data['myID']}"
            cursor.execute(query )
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record updated successfully'})
        elif action == 'delete':
            query = "DELETE FROM Custom WHERE id_custom = ?"
            cursor.execute(query, (data['myID'],))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record deleted successfully'})

    elif table == 'Project':
        if action == 'add':
            query = "INSERT INTO Project (Name_project,id_custom) VALUES (?,?)"
            cursor.execute(query, (data['new_name'],data['parent_id']))
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return jsonify({'message': 'Record added successfully', 'row_id': row_id})
        elif action == 'update':
            # query = "UPDATE Project SET Name_project = ? WHERE id_project = ?"
            # cursor.execute(query, (data['Name_project'], data['id_project']))
            query = f"UPDATE Project SET Name_project = '{data['new_name']}' WHERE id_project = {data['myID']}"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record updated successfully'})
        elif action == 'delete':
            query = "DELETE FROM Project WHERE id_project = ?"
            cursor.execute(query, (data['myID'],))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record deleted successfully'})

    elif table == 'Models':
        if action == 'add':
            query = "INSERT INTO Models (name_model, id_project) VALUES (?,?)"
            cursor.execute(query, (data['new_name'],data['parent_id']))
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return jsonify({'message': 'Record added successfully', 'row_id': row_id})
        elif action == 'update':
            # query = "UPDATE Models SET name_model = ? WHERE id_model = ?"
            # cursor.execute(query, (data['name_model'], data['id_model']))

            query = f"UPDATE Models SET name_model = '{data['new_name']}' WHERE id_model = {data['myID']}"
            cursor.execute(query)

            conn.commit()
            conn.close()
            return jsonify({'message': 'Record updated successfully'})
        elif action == 'delete':
            query = "DELETE FROM Models WHERE id_model = ?"
            cursor.execute(query, (data['myID'],))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record deleted successfully'})

    elif table == 'Label':
        if action == 'add':
            query = "INSERT INTO Label (name_label, id_model) VALUES (?,?)"
            cursor.execute(query, (data['new_name'],data['parent_id']))
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return jsonify({'message': 'Record added successfully', 'row_id': row_id})
        elif action == 'update':
            query = f"UPDATE Label SET name_label = '{data['new_name']}' WHERE id_label = {data['myID']}"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record updated successfully'})
        elif action == 'delete':
            query = "DELETE FROM Label WHERE id_label = ?"
            cursor.execute(query, (data['myID'],))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Record deleted successfully'})

    else:
        return jsonify({'message': 'Invalid table'})


@app.route('/get_projects', methods=['POST'])
def get_projects():
    custom_id = request.form.get('custom_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Project WHERE id_custom = ?", (custom_id,))
    project_list = cursor.fetchall()

    conn.close()

    return jsonify(project_list)


@app.route('/get_models', methods=['POST'])
def get_models():
    project_id = request.form.get('project_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Models WHERE id_project = ?", (project_id,))
    models_list = cursor.fetchall()

    conn.close()

    return jsonify(models_list)


@app.route('/get_labels', methods=['POST'])
def get_labels():
    model_id = request.form.get('model_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Label WHERE id_model = ?", (model_id,))
    labels_list = cursor.fetchall()

    conn.close()

    return jsonify(labels_list)


if __name__ == '__main__':
    app.run()
