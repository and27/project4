import os
from flask import request, render_template, redirect, session
from flask_session import Session
from settings import app
from wrapd import loginRequired
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Session(app)

@app.route("/game")
def game():
	return render_template("a.html")

@app.route("/statistics")
def game_statistics():
	performanceList=[]
	row = db.execute("select * from performance where id_user=:id_user",{"id_user":1}  )
	result = row.fetchall()
	for r in result:
		performanceList.append(r[2])
	return render_template("statistics.html", performanceList=performanceList)


@app.route("/")
def index():
	if session.get('username') is not None:
		return redirect('/game')
	else:
		return render_template("index.html")

@app.route("/login", methods=['POST','GET'])
def login():
	session.clear()
	username = request.form.get("username")
	pwd = request.form.get("pwd")
	
	
	if request.method == 'POST':
		if not username:
			print("error")
		if not pwd:
			print("error")
	
		users = db.execute("SELECT * from users where username 	= :username", { "username":username })	
	
		result = users.fetchone()
		if result == None or not check_password_hash(result[2], pwd):
			return render_template("error.html", message="invalid password")
		else:
			session['username']=result[0]
	
		return redirect("/char")
	else:
		return render_template("login.html")

	
@app.route("/logout", methods=['GET'])
def logout():
        
        session.clear()
        return redirect("/")

@app.route("/register", methods=['GET','POST'])
def register():
	username = request.form.get('username')
	pwd = request.form.get('pwd')
	email = request.form.get('email')
	session.clear()

	
	if request.method == 'POST':
		if not username:
			render_template("error.html", message="you need to provide a username")
		if not email:
			render_template("error.html", message="you need to provide a valid email")
		if not pwd:
			render_template("error.html", message="you need to provide a password")
		else:
			hpwd=generate_password_hash(pwd)
			db.execute("insert into users values  (:username, :email, :pwd)", {"username":username,"email":email,"pwd":hpwd})
			db.commit()
		
			return render_template("login.html")
		
	else: 
		return render_template("register.html")
		
	
@app.route("/char")
def char():
	return render_template("character.html")

	
