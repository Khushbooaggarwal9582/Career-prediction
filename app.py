from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os
import pickle
from datetime import datetime
from mongodb_roadmaps import get_collection, get_roadmap
from users_db import db_handler

app = Flask(__name__)
CORS(app)

career_model = pickle.load(open("career_model.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))
skills_mlb = pickle.load(open("skills_mlb.pkl", "rb"))
feature_columns = pickle.load(open("feature_columns.pkl", "rb"))
stage2_models = pickle.load(open("stage2_models.pkl", "rb"))
stage2_encoders = pickle.load(open("stage2_encoders.pkl", "rb"))


def build_feature_row(education, specialization, interests, skills_string):
    row = pd.Series(0, index=feature_columns, dtype=int)

    for prefix, value in [
        ("Education_Level", education),
        ("Specialization", specialization),
        ("Interests", interests),
    ]:
        col_name = f"{prefix}_{value}"
        if col_name in row.index:
            row[col_name] = 1

    skills_list = [s.strip() for s in skills_string.split(",")]
    skill_vector = skills_mlb.transform([skills_list])[0]
    skill_col_names = ["Skill_" + c for c in skills_mlb.classes_]
    for name, val in zip(skill_col_names, skill_vector):
        row[name] = val

    return pd.DataFrame([row], columns=feature_columns)


# The ML model has more career titles than the roadmap dataset.
# Keep the ML labels unchanged and map related titles to the closest
# available roadmap template. This fixes cases such as:
# "Web Developer" -> "Frontend Developer".
CAREER_ROADMAP_ALIASES = {}  # Every ML career title has its own MongoDB roadmap.


def resolve_roadmap_career(career):
    # Keep the ML career title unchanged: MongoDB stores one domain-specific
    # roadmap document for every career label produced by the model.
    return CAREER_ROADMAP_ALIASES.get(career, career)


LOCAL_ROADMAPS = {}
try:
    from roadmaps_data import ROADMAPS as SEED_ROADMAPS
    for career_key, steps_list in SEED_ROADMAPS.items():
        LOCAL_ROADMAPS[career_key] = [
            {"step": i, "title": title, "skill": skill, "project": project}
            for i, (title, skill, project) in enumerate(steps_list, start=1)
        ]
except Exception:
    pass


def build_roadmap(career):
    # IMPORTANT: exact career match only. No generic fallback.
    roadmap_career = resolve_roadmap_career(career)
    try:
        doc = get_roadmap(roadmap_career)
        if doc and doc.get("steps"):
            return doc.get("steps")
    except Exception:
        pass
    return LOCAL_ROADMAPS.get(roadmap_career, [])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    education = data.get("education")
    specialization = data.get("specialization")
    interests = data.get("interests")
    skills = data.get("skills")

    if not all([education, specialization, interests, skills]):
        return jsonify({"error": "Missing one or more required fields."}), 400

    row = build_feature_row(education, specialization, interests, skills)

    category_num = career_model.predict(row)[0]
    category = label_encoder.inverse_transform([category_num])[0]

    title_model = stage2_models[category]
    title_encoder = stage2_encoders[category]

    probabilities = title_model.predict_proba(row)[0]
    top3_idx = probabilities.argsort()[::-1][:3]
    top3_titles = title_encoder.inverse_transform(top3_idx)
    top3_confidence = probabilities[top3_idx]

    predictions = [
        {"title": str(title), "confidence": round(float(conf) * 100, 1)}
        for title, conf in zip(top3_titles, top3_confidence)
    ]

    # Build the roadmap in the SAME response as the prediction.
    # This avoids a second frontend request and guarantees that the
    # roadmap uses the exact career returned by the ML model.
    top_career = predictions[0]["title"]
    roadmap_steps = build_roadmap(top_career)

    # Automatically save prediction if user is logged in
    email = data.get("email")
    if email:
        pred_info = {
            "career": top_career,
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_steps": len(roadmap_steps)
        }
        db_handler.save_prediction(email, pred_info)

    return jsonify({
        "category": category,
        "career": top_career,
        "predictions": predictions,
        "roadmap_for": resolve_roadmap_career(top_career),
        "roadmap": roadmap_steps,
        "roadmap_source": "mongodb",
    })


@app.route("/roadmap", methods=["POST"])
def roadmap():
    data = request.get_json() or {}
    career = data.get("career")
    if not career:
        return jsonify({"error": "Career is required."}), 400

    steps = build_roadmap(career)
    if not steps:
        return jsonify({"error": "No roadmap found for this career."}), 404

    return jsonify({
        "career": career,
        "roadmap_for": resolve_roadmap_career(career),
        "roadmap": steps
    })


@app.route("/roadmap/<path:career>", methods=["GET"])
def roadmap_by_career(career):
    # Useful for checking exactly what MongoDB returns for one career.
    roadmap_career = resolve_roadmap_career(career)
    try:
        doc = get_roadmap(roadmap_career)
        if not doc:
            return jsonify({"error": f"No roadmap found for '{career}'", "roadmap_for": roadmap_career}), 404
        return jsonify(doc)
    except Exception as exc:
        return jsonify({"error": str(exc), "roadmap_for": roadmap_career}), 500


# ── Auth & Profile Persistence Routes ──────────────────────────────────

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    success = db_handler.register_user(email, password)
    if not success:
        return jsonify({"error": "User with this email already exists."}), 400

    return jsonify({"message": "User registered successfully."})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = db_handler.verify_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password."}), 401

    return jsonify({
        "message": "Login successful.",
        "user": user
    })


@app.route("/api/profile", methods=["GET"])
def get_profile():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400

    user = db_handler.get_user_profile(email)
    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify(user)


@app.route("/api/save_prediction", methods=["POST"])
def save_prediction():
    data = request.get_json() or {}
    email = data.get("email")
    career = data.get("career")
    category = data.get("category")
    total_steps = data.get("total_steps", 5)
    if not email or not career or not category:
        return jsonify({"error": "Email, career, and category are required."}), 400

    pred_info = {
        "career": career,
        "category": category,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_steps": total_steps
    }
    db_handler.save_prediction(email, pred_info)
    return jsonify({"message": "Prediction saved successfully.", "prediction": pred_info})



@app.route("/api/save_progress", methods=["POST"])
def save_progress():
    data = request.get_json() or {}
    email = data.get("email")
    career = data.get("career")
    checked_steps = data.get("checked_steps")
    if not email or not career or checked_steps is None:
        return jsonify({"error": "Email, career, and checked_steps are required."}), 400

    db_handler.save_progress(email, career, checked_steps)
    return jsonify({"message": "Progress saved successfully."})


if __name__ == "__main__":
    app.run(debug=True)