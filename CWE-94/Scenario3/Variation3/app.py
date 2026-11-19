from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        calculation = request.form.get("calc", "")

        if mode == "advanced":
            # TODO: Handle conditional expressions inn Advanced Mode
            template_str = f"{{{{ {calculation} }}}}"
        
        else:
            template_str = f"{{{{ {calculation} }}}}"

        try:
            output = render_template_string(template_str)
        except Exception as e:
            output = f"Error: {e}"
    
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)