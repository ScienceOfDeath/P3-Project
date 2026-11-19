from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

variables = {}

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        var_input = request.form.get("var_def", "").strip()
        calculation = request.form.get("calc", "")

        if var_input and "=" in var_input:
            name, val = var_input.split("=", 1)
            variables[name.strip()] = val.strip()

        if calculation:
            # TODO: Make defined variables available during calculation and evaluate the expression
            try:
                output = render_template_string(f"{{{{ {calculation} }}}}")
            except Exception as e:
                output = f"Error: {e}"

    return render_template("index.html", output=output, variables=variables)

if __name__ == "__main__":
    app.run(debug=True)