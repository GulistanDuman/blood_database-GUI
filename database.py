import mysql.connector

class Database:
    def __init__(self):
        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="G12345!",
            database="blood_database"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_donor(self, name, donor_id, age, blood_group, disease=None):
        
        query = "INSERT INTO donor (name, ID, age, blood_group, disease) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, donor_id, age, blood_group, disease))
        self.conn.commit()

    def delete_donor(self, donor_id):
        
        query = "DELETE FROM donor WHERE ID = %s"
        self.cursor.execute(query, (donor_id,))
        self.conn.commit()

    def update_donor(self, donor_id, name=None, age=None, blood_group=None, disease=None):
        
        query = "UPDATE donor SET "
        updates = []
        values = []

        if name:
            updates.append("name = %s")
            values.append(name)
        if age:
            updates.append("age = %s")
            values.append(age)
        if blood_group:
            updates.append("blood_group = %s")
            values.append(blood_group)
        if disease:
            updates.append("disease = %s")
            values.append(disease)

        if not updates:
            return  

        query += ", ".join(updates) + " WHERE ID = %s"
        values.append(donor_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def add_patient(self, patient_id, name, address, need_bloodgroup, host_name):
        
        query = "INSERT INTO patient (ID, name, address, need_bloodgroup, host_name) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (patient_id, name, address, need_bloodgroup, host_name))
        self.conn.commit()

    def delete_patient(self, patient_id):
        
        query = "DELETE FROM patient WHERE ID = %s"
        self.cursor.execute(query, (patient_id,))
        self.conn.commit()

    def add_user(self, username, password, is_admin):
        
        query = "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, password, is_admin))
        self.conn.commit()

    def delete_user(self, username):
        
        query = "DELETE FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        self.conn.commit()

    def get_user_by_username(self, username):
        
        query = "SELECT * FROM users WHERE username = %s"
        result = self.fetch_query(query, (username,))
        return result[0] if result else None

    def close_connection(self):
        
        self.conn.close()

