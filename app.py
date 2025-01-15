from flask import Flask, render_template, redirect, request, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:RahilShaikh@localhost/lexus"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']=os.urandom(32)

db=SQLAlchemy(app)

r=redis.Redis(host="localhost", port=6379 ,decode_responses=True)

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    useremail=db.Column(db.String(200),nullable=False,unique=True)
    userpassword=db.Column(db.String(200),nullable=False)
    selectedimages=db.Column(db.JSON)
    todo=db.Column(db.JSON,default=[])

    def __init__(self,username,useremail,userpassword,selectedimages,todo):
        self.username=username
        self.useremail=useremail
        self.userpassword=userpassword
        self.selectedimages=selectedimages
        self.todo=todo or []

    def __repr__(self):
        return f'<User {self.username}>'

@app.route("/home",methods=["POST","GET"])
def homepage():
    if request.method=="POST":
        user_action=request.form.get('action')
        if user_action=='login':
            return redirect(url_for('login'))
        if user_action=='signup':
            return redirect(url_for('signup'))
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['username'].lower()
        user_email = request.form['useremail']
        user_password = request.form['userpassword']
        selected_images = request.form.getlist('images')

        #Redis
        user_info=r.hgetall(f"user:{user_name}")

        if user_info:
            print("Passing data from redis Login!")
            if user_info['userpassword']==user_password and user_info['useremail']==user_email:
                if set(selected_images)==set(json.loads(user_info['selectedimages'])):
                    session['user_id']=user_info['id']
                    return redirect(url_for('success'))
                else:
                    return render_template('login.html',msg="Wrong selection og images")
            else:
                return render_template('login.html',msg="Wrong Credentials!")
        else:
            #PostgreSQL
            user = db.session.query(User).filter(User.username == user_name).first()

            if user:
                if user_password == user.userpassword:
                    if user_email == user.useremail:
                        if set(selected_images) == set(user.selectedimages):
                            print("storing data while logging in!")
                            r.hmset(f"user:{user.username}",{
                                'id':user.id,
                                'useremail':user.useremail,
                                'userpassword':user.userpassword,
                                'selectedimages':json.dumps(user.selectedimages)
                            })
                            session['user_id']=user.id
                            return redirect(url_for('success'))
                        else:
                            return render_template('login.html', msg="Wrong selection of images!")
                    else:
                        return render_template('login.html', msg="Wrong email")
                else:
                    return render_template('login.html', msg="Wrong password")
            else:
                return render_template('login.html', msg="User does not exist!")

    else:
        return render_template('login.html')


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user_name = request.form['username'].lower()
        user_email = request.form['useremail']
        user_password = request.form['userpassword']
        password_check = request.form['passwordcheck']
        selected_images = request.form.getlist('images')

        if db.session.query(User).filter(User.username == user_name).count() != 0:
            return render_template('signup.html', msg="User with this username already exists!")

        if db.session.query(User).filter(User.useremail == user_email).count() != 0:
            return render_template('signup.html', msg="User with this email already exists!")

        if user_password != password_check:
            return render_template('signup.html', msg="Passwords not match!")

        new_user = User(
            username=user_name,
            useremail=user_email,
            userpassword=user_password,
            selectedimages=selected_images,
            todo=[]
        )
        db.session.add(new_user)
        db.session.commit()

        print("Storing while signing!")
        r.hmset(f"user:{new_user.username}",{
            'id':new_user.id,
            'useremail':new_user.useremail,
            'userpassword':new_user.userpassword,
            'selectedimages':json.dumps(new_user.selectedimages)
        })

        session['user_id']=new_user.id

        return redirect(url_for('success'))
    else:
        return render_template('signup.html')


@app.route('/success', methods=["GET", "POST"])
def success():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        if user.todo is None:
            user.todo = []
        
        if request.method == "POST":
            user_action = request.form.get('action')

            if user_action == "add":
                new_task = request.form.get('task')

                if new_task and new_task not in user.todo:
                    updated_todo = user.todo[:]
                    updated_todo.append(new_task)
                    user.todo = updated_todo 
                    db.session.commit()

            elif user_action == "delete":
                task_to_delete = request.form.get('task')

                if task_to_delete in user.todo:
                    updated_todo = user.todo[:]
                    updated_todo.remove(task_to_delete)
                    user.todo = updated_todo
                    db.session.commit()

    return render_template("success.html", user=user)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)