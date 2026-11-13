from flask import Flask, render_template, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

custom_email_template = "Welcome to our platform, {{ user.username }}!"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

@app.route("/admin/template", methods=["POST"])
def update_template():
    global custom_email_template
    custom_email_template = request.form.get("template", custom_email_template)
    return "Template updated successfully! <a href='/admin'>Back to Admin Panel</a>"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        if username and email:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()

            template_to_render = custom_email_template.replace("{{ user.username }}", new_user.username)
            rendered_email = render_template_string(template_to_render, User=User)

            return render_template(
                "login.html",
                registered_user=new_user,
                rendered_email=rendered_email
            )

        return render_template("login.html", error="Registration failed. Please provide username and email.")

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    email = request.form.get("email")
    user = User.query.filter_by(username=username, email=email).first()

    if user:
        return f"Logged in as {user.username}! <a href='/'>Home</a>"
    return render_template("login.html", error="Invalid credentials.")

if __name__ == "__main__":
    app.run(debug=True)