
from flask import Flask, Blueprint, abort, app, render_template, request, redirect, url_for, session, flash         #Flask-Modul und render_template für html-rendering
import sqlite3
from app.main import main_routes


@main_routes.route("/login")
def show_login():
    return render_template("login.html")

# @main_routes.route("/base2")
# def show_base2():
#     return render_template("base2.html")


@main_routes.route("/login/verification", methods=["POST", "GET"])
def login():
    password = request.form['password']
    email = request.form['email']
    
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()  
    c.execute("SELECT * FROM mitarbeiter WHERE email = ?", (email,))
    mitarbeiter = c.fetchall()
    conn.close()
    if password and email:
        if password == user[3] and email == user[2]:
            session['admin'] = user[4]
            session['username'] = user[1]
            session['user_id'] = user[0]
            if mitarbeiter:
                session['mitarbeiter_id'] = mitarbeiter[0][0]
                
            return redirect(url_for("projekte_routes.index_project"))
        else:
            return render_template("register.html")
            
            
    
@main_routes.route("/registration", methods = ['POST'])                     #registration       Allgemein 3
def regist_person():    
    if session.get('email_vergeben'):
       session.pop('email_vergeben', None)
    elif session.get('username_vergeben'):     
        session.pop('username_vergeben', None)
    elif session.get('email_vergeben') and session.get('username_vergeben'):
        session.pop('email_vergeben', None)
        session.pop('username_vergeben', None)
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    admin = 1
    conn = sqlite3.connect('project_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", 
              (email,))
    user_email = c.fetchall()
    c.execute("SELECT * FROM users WHERE username = ?", 
              (username,))
    user_name = c.fetchall()
    if user_email:
        session['email_vergeben'] = 1
        return redirect(url_for("main_routes.get_regist_form"))                                     
    elif user_name:
        if username:
            session['username_vergeben'] = 1
            return redirect(url_for("main_routes.get_regist_form"))   
    else:
        c.execute("INSERT INTO users (username, email, password, admin) VALUES (?,?,?,?)"
            , (username, email, password, admin))
        conn.commit()
        conn.close()
        print("User_Admin wurde hinzugefuegt")                 
        return render_template("login.html")

@main_routes.route("/register")                                                     #register user, check for sessions
def get_regist_form():                                                              #Allgemein 4
    return render_template("register.html")





@main_routes.route("/logout")                                                           #logout
def logout():
    
    session.pop('admin', None)
    session.pop('username', None)

    return render_template("logout.html")