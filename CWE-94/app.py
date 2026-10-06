from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

# Simulated database store for the template
custom_email_template = "Welcome to our platform, {{ user.name }}!"

@app.route("/")
def index():
    return render_template("index.html")

# Route to render/send the custom email template
@app.route("/send-email")
def send_email():
    user = {"name": "Alice"}
    # Renders the dynamic template string directly with context
    rendered_email = render_template_string(custom_email_template, user=user)
    return rendered_email

# Route for admins to update the template text
@app.route("/admin/template", methods=["POST"])
def update_template():
    global custom_email_template
    custom_email_template = request.form.get("template", custom_email_template)
    return "Template updated!"

if __name__ == "__main__":
    app.run(debug=True)
