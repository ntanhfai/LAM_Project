import sqlite3
from os.path import exists
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('LAMdatabase.db', timeout=10)
    except Error as e:
        print(e)
    return conn

if not exists('LAMdatabase.db'):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS "Custom" (
                        id_custom INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_custom VARCHAR(100)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "Project" (
                        id_project INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name_project VARCHAR(100),
                        id_custom INTEGER,
                        FOREIGN KEY (id_custom) REFERENCES Custom(id_custom) ON DELETE CASCADE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "Models" (
                        id_model INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_model VARCHAR(100),
                        id_project INTEGER,
                        FOREIGN KEY (id_project) REFERENCES Project(id_project) ON DELETE CASCADE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "Label" (
                        id_label INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_label VARCHAR(100),
                        path_label VARCHAR(100),
                        id_model INTEGER,
                        FOREIGN KEY (id_model) REFERENCES Models(id_model) ON DELETE CASCADE
                    )''')

    conn.commit()
    conn.close()

    import random
    import string


    # Hàm tạo chuỗi ngẫu nhiên
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))


    # Hàm thêm dữ liệu ngẫu nhiên vào bảng Custom
    def add_random_custom_data(num_records):
        conn = create_connection()
        cursor = conn.cursor()

        for _ in range(num_records):
            name_custom = random_string(10)  # Tạo tên custom ngẫu nhiên
            cursor.execute("INSERT INTO Custom (name_custom) VALUES (?)", (name_custom,))

        conn.commit()
        conn.close()


    # Hàm thêm dữ liệu ngẫu nhiên vào bảng Project
    def add_random_project_data(num_records):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_custom FROM Custom")
        custom_ids = [row[0] for row in cursor.fetchall()]  # Lấy danh sách id_custom từ bảng Custom

        for _ in range(num_records):
            name_project = random_string(10)  # Tạo tên project ngẫu nhiên
            id_custom = random.choice(custom_ids)  # Chọn một id_custom ngẫu nhiên
            cursor.execute("INSERT INTO Project (name_project, id_custom) VALUES (?, ?)", (name_project, id_custom))

        conn.commit()
        conn.close()


    # Hàm thêm dữ liệu ngẫu nhiên vào bảng Models
    def add_random_models_data(num_records):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_project FROM Project")
        project_ids = [row[0] for row in cursor.fetchall()]  # Lấy danh sách id_project từ bảng Project

        for _ in range(num_records):
            name_model = random_string(10)  # Tạo tên model ngẫu nhiên
            id_project = random.choice(project_ids)  # Chọn một id_project ngẫu nhiên
            cursor.execute("INSERT INTO Models (name_model, id_project) VALUES (?, ?)", (name_model, id_project))

        conn.commit()
        conn.close()


    # Hàm thêm dữ liệu ngẫu nhiên vào bảng Label
    def add_random_label_data(num_records):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_model FROM Models")
        model_ids = [row[0] for row in cursor.fetchall()]  # Lấy danh sách id_model từ bảng Models

        for _ in range(num_records):
            name_label = random_string(10)  # Tạo tên label ngẫu nhiên
            path_label = random_string(10)  # Tạo đường dẫn label ngẫu nhiên
            id_model = random.choice(model_ids)  # Chọn một id_model ngẫu nhiên
            cursor.execute("INSERT INTO Label (name_label, path_label, id_model) VALUES (?, ?, ?)",
                           (name_label, path_label, id_model))

        conn.commit()
        conn.close()


    # Sử dụng hàm để thêm dữ liệu ngẫu nhiên
    num_records = 10  # Số lượng bản ghi ngẫu nhiên muốn thêm
    add_random_custom_data(num_records)
    add_random_project_data(num_records)
    add_random_models_data(num_records)
    add_random_label_data(num_records)

