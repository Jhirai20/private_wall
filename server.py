from flask import Flask, redirect, render_template, request, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key='keepsake'
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/success',)
def result():
    mysql = connectToMySQL("private_wall")
    query = f"SELECT * FROM users WHERE id!={session['userid']}"
    results = mysql.query_db(query)
    mysql = connectToMySQL("private_wall")
    query = f"SELECT * FROM users JOIN message ON users.id= message.users_id WHERE recipiant_id={session['userid']}"
    message = mysql.query_db(query)

    return render_template("success.html", results=results, message=message)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
@app.route ('/process', methods=['POST'])
def process():
    is_valid = True
    if len(request.form['fname']) <1:
        flash("First name cannot be blank!")
    if len(request.form['lname']) <1:
        flash("Last name cannot be blank!")
    if len(request.form['email']) <1:
        flash("Email cannot be blank!")
    if request.form['password']!=request.form['password2']:
        flash("Passwords don't match!")
    if not is_valid:
        return redirect('/')
    else:
        if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
            flash("Invalid email address!")
        else:
            pw_hash = bcrypt.generate_password_hash(request.form['password2'])
            print(pw_hash) 
            mysql=connectToMySQL('private_wall')
            query = "INSERT INTO users(first_name, last_name, email,pw_hash, created_at, updated_at) VALUES (%(fname)s,%(lname)s,%(email)s,%(password_hash)s,NOW(),NOW());"
            data = {
                'fname': request.form['fname'],
                'lname': request.form['lname'],
                'email': request.form['email'],
                "password_hash" : pw_hash
            }
            mysql.query_db(query, data)
            mysql = connectToMySQL("private_wall")
            query1 = "SELECT * FROM users WHERE email = %(email)s;"
            data1 = { "email" : request.form["email"] }
            results = mysql.query_db(query1, data1)
            session['userfname'] = results[0]['first_name']
            session['userlname'] = results[0]['last_name']
            session['userid'] = results[0]['id']
            
            print(results[0]['id'])
            return redirect('/success')
    return redirect('/')

@app.route ('/login', methods=['POST'])
def login():
    mysql = connectToMySQL("private_wall")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['pw_hash'], request.form['password']):
            session['userid'] = result[0]['id']
            session['userfname'] = result[0]['first_name']
            session['userlname'] = result[0]['last_name']
            print(session['userid'])
            return redirect('/success')
    flash("You could not be logged in")
    return redirect("/")

@app.route('/destroy/<id>')
def destroy(id):
    mysql=connectToMySQL('private_wall')
    query=f"DELETE FROM message WHERE id='{id}'"
    print(query)
    mysql.query_db(query)
    return redirect('/success')

@app.route('/message',methods=['POST'])
def message():
    is_valid = True
    if len(request.form['message']) <2:
        flash("Message cannot be blank!")
    if not is_valid:
        return redirect('/success')
    else:
        mysql=connectToMySQL('private_wall')
        query = "INSERT INTO message(users_id, message, recipiant_id) VALUES (%(users_id)s,%(message)s,%(recipiant_id)s);"
        data = {
        'users_id':int(session['userid']),
        'message':request.form['message'],
        'recipiant_id':int(request.form["recipiant_id"])
        }
        mysql.query_db(query,data)
        return redirect('/success')
    return redirect('/success')
@app.route('/logout',)
def logout():
    session.clear()
    return redirect("/")

@app.route("/useremail",methods=['POST'])

def useremail():
    print("****************test if info was passed",request.form)
    found = False
    mysql = connectToMySQL('private_wall')
    query = "SELECT email FROM users WHERE email = %(email)s;"
    data = {'email': request.form['email']}
    result = mysql.query_db(query, data)
    print(result)
    if result:
        found = True
    return render_template ('partials/useremail.html', found=found)
        # render a partial and return it
        # Notice that we are rendering on a post! Why is it okay to render on a post in this scenario?
        # Consider what would happen if the user clicks refresh. Would the form be resubmitted?

@app.route("/emailsearch", methods=['GET'])
def serach():
    print("****************test if info was passed",request.form)
    mysql = connectToMySQL("private_wall")
    query = "SELECT * FROM users WHERE email LIKE %%(email)s;"
    print("***********", request.args.get('name'))
    data = {"email":request.args.get('name') + "%"}
    if len(request.args.get('name'))>0:
        results = mysql.query_db(query,data)
    return render_template('partials/emailsearch.html',email = results)

if __name__=="__main__":
    app.run(debug=True)