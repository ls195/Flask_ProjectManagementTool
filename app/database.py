import sqlite3


def create_database():
    conn = sqlite3.connect("project_management.db")                     #Datenbank und Tabellen erstellen
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS projects(
                    id INTEGER PRIMARY KEY, 
                    project_name VARCHAR(255) NOT NULL, 
                    description VARCHAR(255), 
                    start_date DATE, 
                    end_date DATE, 
                    project_manager_id INTEGER REFERENCES employees(id), 
                    status VARCHAR(50)
                )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY, 
                    title VARCHAR(255) NOT NULL, 
                    description VARCHAR(255), 
                    status VARCHAR(50), 
                    due_date DATE, 
                    priority VARCHAR(50), 
                    project_id INTEGER REFERENCES projects(id), 
                    assigned_to INTEGER REFERENCES employees(id)
                )''')

    
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY, 
                    username VARCHAR(50), 
                    email VARCHAR(255), 
                    password VARCHAR(50),
                    admin INTEGER
                )''')

    
    c.execute('''CREATE TABLE IF NOT EXISTS mitarbeiter_projekt(
                    mitarbeiter_id INTEGER, 
                    projekt_id INTEGER, 
                    PRIMARY KEY (mitarbeiter_id, projekt_id),
                    FOREIGN KEY (mitarbeiter_id) REFERENCES mitarbeiter(id),
                    FOREIGN KEY (projekt_id) REFERENCES projekt(id)
                )''')

    
    c.execute('''CREATE TABLE IF NOT EXISTS mitarbeiter(
                    id INTEGER PRIMARY KEY, 
                    vorname VARCHAR(50),
                    nachname VARCHAR(50), 
                    email VARCHAR(255), 
                    password VARCHAR(50),
                    rolle VARCHAR(50),
                    project_id INTEGER
                )''')
    
    print(__name__)
    conn.commit()
    conn.close()


     