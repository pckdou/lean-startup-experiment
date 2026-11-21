import uuid
from flask import Flask, request, make_response, render_template, redirect, url_for
from app.flags import get_variant
from app.tracker import track

app = Flask(__name__)
FLAG = "short_onboarding"

def current_user():
    uid = request.args.get("uid") or request.cookies.get("uid") or str(uuid.uuid4())
    return uid, get_variant(uid, FLAG)

@app.route("/")
def index():
    uid, variant = current_user()
    track(uid, variant, "visit")
    resp = make_response(render_template("index.html", variant=variant, uid=uid))
    resp.set_cookie("uid", uid)
    return resp

@app.route("/signup", methods=["GET", "POST"])
def signup():
    uid, variant = current_user()
    if request.method == "POST":
        track(uid, variant, "signup_completed")
        return redirect(url_for("dashboard", uid=uid))
    track(uid, variant, "signup_started")
    return render_template("signup.html", variant=variant, uid=uid)

@app.route("/dashboard")
def dashboard():
    uid, variant = current_user()
    return render_template("dashboard.html", variant=variant, uid=uid)

@app.route("/use-feature", methods=["POST"])
def use_feature():
    uid, variant = current_user()
    track(uid, variant, "feature_used")
    return "계획이 생성되었습니다! <a href='/dashboard?uid=%s'>돌아가기</a>" % uid

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
