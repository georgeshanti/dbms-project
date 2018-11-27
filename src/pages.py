from flask import Flask, render_template, request
from flask_login import login_required, current_user
import sqlite3
import os.path

def set_pages(app):
    @app.route('/')
    def index_page():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dash():

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "calendar.db")
        conn = sqlite3.connect(db_path)
        keys = ['id', 'name']
        c = conn.cursor()
        d = str(current_user.get_id())
        c.execute("select groups.id as id, groups.name as name from memberships, groups where memberships.grp_id=groups.id and memberships.usr_id=?", d)
        groups = c.fetchall()
        group_list = list(map(lambda x: dict(zip(keys,x)), groups))

        r_keys = ["name", "desc", "date"]
        c.execute("select reminder.name as name, reminder.desc as desc, reminder.time as date from memberships, reminder where memberships.grp_id=reminder.grp_id and memberships.usr_id=?", d)
        reminders = c.fetchall()
        reminders_list = list(map(lambda x: dict(zip(r_keys,x)), reminders))
        print(reminders_list)

        return render_template('dashboard-cards.html', group_list=group_list, rems=reminders_list)

    @app.route('/search/<name>')
    def search_page(name):
        print(name)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "calendar.db")
        conn = sqlite3.connect(db_path)
        keys = ['id', 'name', 'desc']
        c = conn.cursor()
        d = ('%'+name+'%', )
        c.execute("select id, name, desc from groups where name like (?)", d)
        groups = c.fetchall()
        group_list = list(map(lambda x: dict(zip(keys,x)), groups))
        print(group_list)

        return render_template('search-group.html', list=group_list, name=name)

    @app.route('/search')
    def emp_search_page():
        return search_page("")
