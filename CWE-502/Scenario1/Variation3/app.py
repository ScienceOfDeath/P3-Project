from datetime import datetime, timezone

from flask import Flask, render_template

app = Flask(__name__)


STATE = {
    "version": 1,
    "started_at": datetime.now(timezone.utc),
    "feature_flags": {"dark_mode": True, "beta": False},
    "counters": {"logins": 3, "errors": 2},
    "admins": {"alice", "bob"},
}


@app.route('/api/admin/backup', methods=['GET'])
def backup_state():
    # TODO: serialize and return runtime state
    raise NotImplementedError


@app.route('/api/admin/restore', methods=['POST'])
def restore_state():
    # TODO: parse payload (file field 'snapshot') and restore state exactly
    raise NotImplementedError


@app.route("/")
def index():
    return render_template("index.html", state=STATE)


if __name__ == "__main__":
    app.run(debug=True)