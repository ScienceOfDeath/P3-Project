from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        calculation = request.form.get("calc", "")
        # SÅRBARHED (CWE-94): Kører brugerinput direkte gennem render_template_string
        output = render_template_string(calculation)
    
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()