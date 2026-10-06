from flask import Flask, render_template

app = Flask(__name__)

@app.route('/api/admin/backup', methods=['GET'])
def backup_state():

    #TODO serialize and return runtime state
    pass

@app.route('/api/admin/restore', methods=['POST'])
def restore_state():

    #TODO parse payload and restore state
    pass

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)