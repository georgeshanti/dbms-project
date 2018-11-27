from flask import Flask, render_template, request, redirect
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
import json
import sqlite3
import os.path

class User(UserMixin):
    
    is_authenticated = False
    is_active = False
    is_anonymous = False

    def __init__(self, id):
        self.is_authenticated = True
        self.is_active = True
        self.id = id
    
    def get_id(self):
        return self.id

def set_api(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        result = {"status": "false"}
        if request.method == 'POST':
            form = request.form
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "calendar.db")
            conn = sqlite3.connect(db_path)
            keys = ['id', 'username', 'name', 'pass']
            c = conn.cursor()
            d = (form['user'], form['pass'], )
            c.execute("select * from users where username=? and pass=?", d)
            users = c.fetchall()
            conn.close()
            if len(users) != 1:
                return json.dumps(result)
            else:
                user = dict(zip(keys,users[0]))
                user_c = User(user["id"])
                login_user(user_c)
                result["status"] = "true"
                return json.dumps(result)

        else:
            return "No";

    @app.route('/api/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route('/api/new_reminder', methods=['POST'])
    @login_required
    def new_reminder():
        result = {"status": "true"}
        form = request.form
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "calendar.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        d = (form['name'], form['date'], form['desc'], form['group'], )
        c.execute("insert into reminder(name, time, desc, grp_id) values(?,?,?,?)", d)
        conn.commit()
        conn.close()
        return json.dumps(result)

    @app.route('/api/new_group', methods=['POST'])
    @login_required
    def new_group():
        result = {"status": "true"}
        form = request.form
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "calendar.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        d = (form['name'], form['desc'], )
        keys = ["id"];
        c.execute("insert into groups(name, desc) values(?,?)", d)
        d = (form['name'], )
        c.execute("select id from groups where name=?", d)
        grps = c.fetchall()
        grp = dict(zip(keys,grps[0]))
        d = (current_user.get_id(), grp['id'], )
        c.execute("insert into memberships(usr_id, grp_id) values(?,?)", d)
        conn.commit()
        conn.close()
        return json.dumps(result)

    @app.route('/api/add_group', methods=['POST'])
    @login_required
    def add_group():
        result = {"status": "true"}
        form = request.form
        print(form)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "calendar.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        d = (current_user.get_id(), form['id'], )
        keys = ["id"];
        c.execute("insert into memberships(usr_id, grp_id) values(?,?)", d)
        conn.commit()
        conn.close()
        return json.dumps(result)
