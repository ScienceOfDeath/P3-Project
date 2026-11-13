from flask import Flask, render_template, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # TODO: Add a password field here

with app.app_context():
    db.create_all()

custom_email_template = "Welcome to our platform, {{ user.username }}!"

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        # TODO: Add a password field here

        if username and email:
            new_user = User(username=username, email=email) # TODO: Add a password field here
            db.session.add(new_user)
            db.session.commit()

            template_to_render = custom_email_template.replace("{{ user.username }}", new_user.username)
            rendered_email = render_template_string(template_to_render, User=User)

            return f"""
            <h2>Registration Successful!</h2>
            <p>Here is the welcome email generated for you:</p>
            <hr>
            <div style="background: #f4f4f4; padding: 15px; border-left: 4px solid #007BFF; font-family: sans-serif;">
                <p><strong>To:</strong> {new_user.email}</p>
                <p>{rendered_email}</p>
            </div>
            <br>
            <a href="/register">Register another user</a> | <a href="/">Go to Admin Panel</a>
            """

        return "Registration failed. Please provide both username and email."

    return """
    <h2>User Registration</h2>
    <form method="POST" action="/register">
        <label>Username:</label><br>
        <input type="text" name="username" style="width: 300px; padding: 5px;" required><br><br>
        <label>Email:</label><br>
        <input type="email" name="email" style="width: 300px; padding: 5px;" required><br><br>
        # TODO: Add a password field here
        <button type="submit" style="padding: 8px 15px; background: #007BFF; color: white; border: none; cursor: pointer;">Register</button>
    </form>
    <br>
    <hr>
    <p><a href="/">Admin Panel (For admins only)</a></p>
    """

@app.route("/admin/template", methods=["POST"])
def update_template():
    global custom_email_template
    custom_email_template = request.form.get("template", custom_email_template)
    return "Template updated successfully! <a href='/'>Back to Admin Panel</a>"

if __name__ == "__main__":
    app.run()