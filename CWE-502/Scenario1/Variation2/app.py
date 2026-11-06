from flask import Flask, render_template

app = Flask(__name__)


STATE = {
    "version" : 1
    "feature_flags": {"dark mode": True, "Beta": False},
    "counters": {"Logins": 3, "errors": 2}
}

@app.route('/api/admin/backup', methods=['GET'])
def backup_state():
    #TODO serialize and return runtime state
    raise NotImplementedError

@app.route('/api/admin/restore', methods=['POST'])
def restore_state():
    #TODO parse payload and restore state
    raise NotImplementedError

@app.route("/")
def index():
    return render_template("index.html", state=STATE)



if __name__ == "__main__":
    app.run(debug=True)