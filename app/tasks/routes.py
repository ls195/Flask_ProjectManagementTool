from flask import Flask, Blueprint, abort, app, render_template, request, redirect, url_for, session, flash        
import sqlite3
from app.tasks import tasks_routes

                                 






@tasks_routes.route("/project/task/details/<int:project_id>/<int:task_id>")              
def show_details_task(project_id, task_id):                                                 
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor() 
    c.execute("SELECT * FROM tasks WHERE id = ? AND project_id = ?", (task_id, project_id,))
    task = c.fetchone()
    conn.close()
    return render_template("task_detail.html", task = task)


@tasks_routes.route("/project/task/details/user_normal/<int:project_id>/<int:task_id>")              
def show_details_task_user_normal(project_id, task_id):                                               
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor() 
    c.execute("SELECT * FROM tasks WHERE id = ? AND project_id = ?", (task_id, project_id,))
    task = c.fetchone()
    conn.close()
    return render_template("task_detail_user_normal.html", task = task)


@tasks_routes.route("/task/update/<int:project_id>/<int:task_id>", methods=['GET'])                         
def update_task(project_id, task_id):                                                              
    conn = sqlite3.connect("project_management.db")                                                
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ? AND project_id = ?", (task_id, project_id,))
    task = c.fetchall() 
    c.execute("SELECT * FROM projects WHERE id = ? ", (project_id,))
    project = c.fetchall()
    c.execute("SELECT * from mitarbeiter WHERE project_id = ?", (project_id,))
    mitarbeiter = c.fetchall()
    conn.close()
    
    if task and project:
        return render_template("task_update.html", task = task, project = project, mitarbeiter = mitarbeiter)        
    else:
        return "Projekt nicht geunden", 404

@tasks_routes.route("/task/update/normal/<int:project_id>/<int:task_id>", methods=['GET'])                         
def update_task_user_normal(project_id, task_id):                                                               
    conn = sqlite3.connect("project_management.db")                                              
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ? AND project_id = ?", (task_id, project_id,))
    task = c.fetchall() 
    c.execute("SELECT * FROM projects WHERE id = ? ", (project_id,))
    project = c.fetchall()
    c.execute("SELECT * from mitarbeiter WHERE project_id = ?", (project_id,))
    mitarbeiter = c.fetchall()
    conn.close()
    
    if task and project:
        return render_template("task_update_user_normal.html", task = task, project = project, mitarbeiter = mitarbeiter)        
    else:
        return "Projekt nicht geunden", 404





@tasks_routes.route("/task/update/<int:project_id>/<int:task_id>", methods=['POST'])                    
def update_task_post(project_id, task_id):                                               
    task_title = request.form['task_title']
    due_date = request.form['due_date']                                                   
    task_status = request.form['task_status']
    assigned_to =  request.form['assigned_to']
    description = request.form['description']
    priority = request.form['task_priority']
    
    conn = sqlite3.connect("project_management.db")
    cursor = conn.cursor()
    cursor.execute(
    """
        UPDATE tasks SET title =?, description=?, due_date=?, priority=? , status  =?, assigned_to = ?
    WHERE id =?
    """, (task_title, description, due_date, priority, task_status, assigned_to, task_id))
    conn.commit()
    conn.close()
    return show_tasks_project_add_task(project_id)

@tasks_routes.route("/task/update/normal/<int:project_id>/<int:task_id>", methods=['POST'])                   
def update_task_post_normal(project_id, task_id):                                               
    task_title = request.form['task_title']
    due_date = request.form['due_date']                                                    
    task_status = request.form['task_status']
    assigned_to =  request.form['assigned_to']
    description = request.form['description']
    priority = request.form['task_priority']
    
    conn = sqlite3.connect("project_management.db")
    cursor = conn.cursor()
    cursor.execute(
    """
        UPDATE tasks SET title =?, description=?, due_date=?, priority=? , status  =?, assigned_to = ?
    WHERE id =?
    """, (task_title, description, due_date, priority, task_status, assigned_to, task_id))
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()  
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id, ))   
    project = c.fetchall()                    
    conn.commit()
    conn.close()
    return render_template("task_segment_user_normal.html", tasks=tasks, project = project)

                    
@tasks_routes.route("/task/delete/<int:task_id>/<int:project_id>")         
def delete_task(task_id, project_id):
    conn = sqlite3.connect("project_management.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()   
    conn.close()
    admin_status = session.get('admin', None)
    if admin_status == 1:      
        return show_tasks_project_add_task(project_id)
    else: 
        return show_tasks_project_add_task_user_normal(project_id)


@tasks_routes.route("/add/task/<int:project_id>", methods=["GET"])                          
def show_tasks_project_add_task(project_id):
    conn = sqlite3.connect("project_management.db")                                         
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()  
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id, ))   
    project = c.fetchall()                                            
    conn.close()
    return render_template("task_segment.html", tasks=tasks, project = project)

@tasks_routes.route("/add/task/user_normal/<int:project_id>", methods=["GET"])                          
def show_tasks_project_add_task_user_normal(project_id):
    conn = sqlite3.connect("project_management.db")                                        
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()  
    c.execute("SELECT * FROM projects WHERE id = ?", (project_id, ))   
    project = c.fetchall()                                            
    conn.close()
    return render_template("task_segment_user_normal.html", tasks=tasks, project = project)

@tasks_routes.route("/project/details/tasks/add/<int:project_id>", methods=["POST"])       
def add_task(project_id):
    print("Task angelegt")                                                                
    task_title = request.form['task_title']
    task_description = request.form['task_description']         
    task_duedate = request.form['task_duedate']
    task_priority = request.form['task_priority']
    task_assigned_to = request.form['task_assigned_to']
    project_id = project_id
    print(f"{project_id}")

    conn = sqlite3.connect('project_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, due_date, priority, project_id, assigned_to) VALUES (?,?,?,?,?,?)"
              , (task_title, task_description, task_duedate, task_priority, project_id, task_assigned_to))
    conn.commit()
    conn.close()    
    admin_status = session.get('admin', None) 
    if admin_status == 1:      
        return show_tasks_project_add_task(project_id)
    else: 
        return show_tasks_project_add_task_user_normal(project_id)

