from flask import Flask, Blueprint, abort, app, render_template, request, redirect, url_for, session, flash        #Flask-Modul und render_template für html-rendering
import sqlite3
from app.mitarbeiter import mitarbeiter_routes


@mitarbeiter_routes.route("/mitarbeiter/add/<int:project_id>", methods=["POST"])  # Add MITARBEITER
def add_mitarbeiter(project_id):
    if session.get('email_vergeben'):                                       #Mitarbeiter 1
        session.pop('email_vergeben', None)

    email = request.form['email']
    password = request.form['password']
    vorname = request.form['vorname']
    nachname = request.form['nachname']
    rolle = request.form['rolle']
    admin = 0

    conn = sqlite3.connect('project_management.db')
    c = conn.cursor()

    # c.execute("SELECT * FROM mitarbeiter WHERE email = ?", (email,))          #nur für Prüfung gebraucht
    # mitarbeiter = c.fetchall()

    # c.execute("SELECT * FROM users WHERE email = ?", (email,))
    # user = c.fetchall()

    c.execute("INSERT INTO mitarbeiter (email, password, vorname, nachname, rolle, project_id) VALUES (?,?,?,?,?,?)",
                  (email, password, vorname, nachname, rolle, project_id))
    c.execute("INSERT INTO users (email, password, admin) VALUES (?,?,?)",
                  (email, password, admin))
    conn.commit()

    c.execute("SELECT id FROM mitarbeiter WHERE email = ?", (email,))
    mitarbeiter_id = c.fetchone()[0]

    c.execute("INSERT INTO mitarbeiter_projekt (mitarbeiter_id, projekt_id) VALUES (?,?)",
                  (mitarbeiter_id, project_id))
    conn.commit()
    conn.close()

    print("Mitarbeiter hinzugefügt, Verbindung zur DB wieder geschlossen")

    if session.get('admin') == 1:
        print(f"Zugang zu mitarbeiter_segment aufgrund der session gewährt:\nSession['admin']: {session['admin']}")
        return mitarbeiter_segment(project_id)
    else:
        print(f"Zugang zu index_projekt verweigert:\nSession['admin']: {session['admin']}")
        return render_template("register.html")

    



@mitarbeiter_routes.route("/mitarbeiter/<int:project_id>", methods = ["GET"])                  # MITARBEITER 2
def mitarbeiter_segment(project_id):
    
    session['project_id']=project_id
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("SELECT * FROM mitarbeiter WHERE project_id = ? ", (project_id, ))
    mitarbeiter = c.fetchall()                                         
    conn.close()
    
    if session['admin'] == 1:
        return render_template("mitarbeiter.html", mitarbeiter=mitarbeiter)
    else:
        return render_template("register.html")
 
 
        
@mitarbeiter_routes.route("/mitarbeiter/update/<int:mitarbeiter_id>/<int:project_id>", methods=["GET"]) 
def update_mitarbeiter_get(mitarbeiter_id, project_id): 
    project_id = project_id
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("SELECT * FROM mitarbeiter WHERE id = ? ", (mitarbeiter_id, ))
    mitarbeiter = c.fetchall()
    conn.close()
    
    if mitarbeiter and session['admin'] == 1:
        return render_template("mitarbeiter_update.html", mitarbeiter = mitarbeiter, project_id = project_id)
    else:
        return "Projekt nicht geunden", 404
    
    
    
@mitarbeiter_routes.route("/mitarbeiter/update/<int:mitarbeiter_id>/<int:project_id>", methods=['POST'])                       #Update, Change eines bestehenden Mitarbeiters
def update_mitarbeiter_post(mitarbeiter_id, project_id):                                                                            #Datenmanipulation bzw. Daten einpflegen --> POST
    vorname = request.form['vorname']
    nachname = request.form['nachname']                                                                                 #Mitarbeiter 4
    email = request.form['email']
    rolle =  request.form['rolle']
    project_id = project_id
    conn = sqlite3.connect("project_management.db")
    cursor = conn.cursor()
    cursor.execute(
    """
    UPDATE mitarbeiter SET vorname = ?, nachname = ?, email = ?, rolle = ?
    WHERE id =?
    """, (vorname, nachname, email, rolle, mitarbeiter_id))
    conn.commit()
    conn.close()
    #return redirect(url_for('mitarbeiter_routes.mitarbeiter_segment'))
    return mitarbeiter_segment(project_id)

@mitarbeiter_routes.route("/mitarbeiter/delete/<int:mitarbeiter_id>/<int:project_id>")                    #Update, Change eines bestehenden Mitarbeiter
def delete_mitarbeiter(mitarbeiter_id,project_id):                                                  #Mitarbeiter5
    
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("DELETE FROM mitarbeiter WHERE id = ?", (mitarbeiter_id,))
    conn.commit()   
    conn.close()
    return mitarbeiter_segment(project_id)