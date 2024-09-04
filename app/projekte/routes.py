from flask import Flask, Blueprint, abort, app, render_template, request, redirect, url_for, session, flash         #Flask-Modul und render_template für html-rendering
import sqlite3
from app.projekte import projekte_routes

# @projekte_routes.route("/base")                                                 # Erstellung der Route /base , was die Funktin show_base_template aufruft
# def show_base_template():
#     return render_template("base.html")


 
# @projekte_routes.route("/project")                                              #view projects, Auflisten aller bestehenden Projekte
# def index_project():                                                                  #Projekt 3
    
#     admin_status = session.get('admin', None)
#     admin_username = session.get('username')
#     user_id = session.get('user_id')
#     conn = sqlite3.connect("project_management.db")                             
#     c = conn.cursor()
#     c.execute("SELECT * FROM projects WHERE project_manager_id = ?", (user_id,))
#     projects = c.fetchall()                                      
#     conn.close()
#     if admin_status == 1:
#         flash(f"Welcome {admin_username} to your Project-Overview:\n You are Admin!")
#         return render_template("project.html", projects=projects)
#     elif admin_status == 0:
#         flash(f"Welcome {admin_username} to your Project-Overview:\n You are no Admin!")      
#         return render_template("project_user_normal.html", projects=projects)
#     else:
#         flash(f"Zugang zu index_projekt verweigert:\nSession['admin']: {admin_status}")
#         return render_template("register.html")
    

@projekte_routes.route("/project")                                              #view projects, Auflisten aller bestehenden Projekte
def index_project():                                                                  #Projekt 3
    admin_status = session.get('admin', None)
    admin_username = session.get('username')
    user_id = session.get('user_id')
    
    if admin_status == 1:

        conn = sqlite3.connect("project_management.db")                             
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE project_manager_id = ?", (user_id,))
        projects = c.fetchall()                                    
        conn.close()
        flash(f"<p><strong>Welcome {admin_username}</strong>,<br>create ur own project, add tasks and invite employees! <br>Add a project and select it to get further.")
        return render_template("project.html", projects=projects)
    
    elif admin_status == 0:
        
        conn = sqlite3.connect("project_management.db")                             
        c = conn.cursor()
        c.execute("SELECT * from mitarbeiter_projekt WHERE mitarbeiter_id = ?", (session['mitarbeiter_id'], ))
        mitarbeiter_projekte=c.fetchall()                                                     
        projects = []                                                                           
        for project in mitarbeiter_projekte:
            c.execute("SELECT * FROM projects WHERE id = ?",(project[1], ))                                                      
            project=c.fetchone()
            
            if project: 
                projects.append(project)     
        conn.close()    
        return render_template("project_user_normal.html", projects=projects)
    else:
        return render_template("register.html")

@projekte_routes.route("/project/add/<int:user_id>", methods=["POST"])                         
def add_project(user_id):                                                           
    project_name = request.form['project_name']
    project_description = request.form['project_description']
    project_startdate = request.form['project_startdate']
    project_enddate = request.form['project_enddate']
    project_managerid = user_id
    project_status = request.form['project_status']
    
    conn = sqlite3.connect('project_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO projects (project_name, description, start_date, end_date, project_manager_id, status) VALUES (?,?,?,?,?,?)"
              , (project_name, project_description, project_startdate, project_enddate, project_managerid, project_status,))
    conn.commit()
    c.execute("SELECT * FROM projects")
    #projects = c.fetchall()   
    conn.close()
    print("Projekt angelegt, Verbindung zur DB wieder geschlossen")                 
    admin_status = session.get('admin')
    if admin_status == 1:
        return redirect(url_for("projekte_routes.index_project"))
    # elif admin_status == 0:
    #     return render_template("projekte_routes/project_user_normal.html", projects=projects)
    else:
        return render_template("register.html")
    
    
@projekte_routes.route('/add/project/<int:user_id>')                                                  #simple route /add/project                  
def add_new_project(user_id):                                                              #Route um auf Projekt_add zu gelangen
    return render_template('add_project.html', user_id = user_id)                                # Projekt 3                        


@projekte_routes.route("/project/update/<int:project_id>", methods=['GET'])                     #Update, change bestehendes Projekt
def update_project(project_id):                                                     #Datenbereitstellung    --> GET
    conn = sqlite3.connect("project_management.db")                                 #Projekt 4
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = c.fetchall() 
    conn.close()
    
    if project and session['admin'] == 1:
        return render_template("/project_update.html", project=project)
    else:
        return "Projekt nicht geunden", 404
    
    
    
@projekte_routes.route("/project/update/<int:project_id>", methods=['POST'])                    #Update, Change eines bestehenden Projektes
def update_project_post(project_id):                                                #Datenmanipulation bzw. Daten einpflegen --> POST
    project_name = request.form['project_name']                                     #Projekt 5
    description = request.form['description']       #project_name, description, start_date, end_date, project_manager_id, status                   
    start_date = request.form['start_date']
    end_date =  request.form['end_date']
    project_manager_id = request.form['project_manager_id']
    project_status = request.form['project_status']
    conn = sqlite3.connect("project_management.db")
    cursor = conn.cursor()
    cursor.execute(
    """
    UPDATE projects SET project_name =?, description=?, start_date=?, end_date=? , project_manager_id =?, status = ?
    WHERE id =?
    """, (project_name, description, start_date, end_date, project_manager_id, project_status, project_id))
    conn.commit()
    conn.close()
    return redirect(url_for('projekte_routes.index_project'))
    


@projekte_routes.route("/task/update/<int:project_id>/<int:task_id>", methods=['GET'])                          #Update, change Tasks eines bestimmten Projektes
def update_task(project_id, task_id):                                                               #Datenbereitstellung    --> GET
    conn = sqlite3.connect("project_management.db")                                                 #/task/update/{{project[0][0]}}/{{task[0]}}
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ? AND project_id = ?", (task_id, project_id,))        #Projekt 6
    task = c.fetchall() 
    c.execute("SELECT * FROM projects WHERE id = ? ", (project_id,))
    project = c.fetchall()
    conn.close()
    
    if task and project:
        return render_template("task_update.html", task = task, project = project)         
    else:
        return "Projekt nicht geunden", 404


@projekte_routes.route("/project/details/<int:project_id>")                             #view project_details + tasks
def show_details(project_id):                                                       #Projekt 7
    session['project_id'] = project_id
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor() 
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = c.fetchall()
    print(project)
    session['project_name'] = project[0][1] 
    c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()  
    print(tasks)                            
    conn.close()
    return render_template("project_details.html", project=project, tasks=tasks)


@projekte_routes.route("/project/details/user_normal/<int:project_id>")                             #view project_details + tasks
def show_details_user_normal(project_id):                                                       #Projekt 7
    session['project_id'] = project_id
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor() 
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = c.fetchall()
    print(project)
    session['project_name'] = project[0][1] 
    c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()  
    print(tasks)                            
    conn.close()
    return render_template("project_details_user_normal.html", project=project, tasks=tasks)
# @projekte_routes.route("/project/details/tasks/<int:project_id>")                             #view project_details
# def show_tasks_project(project_id):                                                         #Project8
#     conn = sqlite3.connect("project_management.db")
#     c = conn.cursor()
#     c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
#     task = c.fetchall()                                                 
#     conn.close()
#     return render_template("project_details.html", task=task)



@projekte_routes.route("/project/delete/<int:project_id>")         #delete project          #Project 9
def delete_project(project_id):
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()   
    c.execute("DELETE FROM tasks WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("projekte_routes.index_project"))
