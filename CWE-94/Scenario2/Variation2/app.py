from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        user_variable = request.form.get("variable", "")
        user_calc = request.form.get("calc", "")
        
        template_str = f"{{% set {user_variable} %}}{{{{ {user_calc} }}}}"
        
        try:
            output = render_template_string(template_str)
        except Exception as e:
            output = f"Error: {e}"
    
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()