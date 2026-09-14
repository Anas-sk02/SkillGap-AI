import pandas as pd
import numpy as np
import json
import os
import joblib
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder

TAXONOMY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'role_skill_taxonomy.json')
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'model_artifacts')
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

PROJECT_TO_SKILLS = {
    "EDA Project": ["Python", "Pandas", "NumPy", "Data Visualization", "Statistics"],
    "Web Scraper": ["Python", "REST APIs", "Linux/Bash"],
    "ML Classifier": ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy", "Statistics"],
    "Neural Network": ["Python", "Deep Learning", "NumPy", "Machine Learning"],
    "REST API": ["Python", "REST APIs", "Django/Flask/FastAPI", "SQL", "Authentication/Security"],
    "E-commerce Site": ["HTML/CSS", "JavaScript", "React", "REST APIs", "CSS Frameworks"],
    "Portfolio Website": ["HTML/CSS", "JavaScript", "Responsive Design", "Git"],
    "Data Dashboard": ["Python", "Data Visualization", "SQL", "Pandas", "React"],
    "Chatbot": ["Python", "NLP", "Deep Learning", "Machine Learning"],
    "Image Classifier": ["Python", "Deep Learning", "NumPy", "Machine Learning", "Scikit-learn"],
    "Recommendation System": ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy", "SQL"],
    "Mobile App Backend": ["Python", "REST APIs", "SQL", "Authentication/Security", "Django/Flask/FastAPI"],
    "Docker Deployment": ["Docker", "CI/CD", "Linux/Bash", "ML Deployment"],
    "Model Deployment API": ["Python", "REST APIs", "ML Deployment", "MLOps", "Docker"],
    "React Dashboard": ["React", "JavaScript", "HTML/CSS", "State Management", "REST APIs"],
    "Database Schema Design": ["SQL", "Database Design", "Python"],
    "A/B Test Analysis": ["Statistics", "Python", "Pandas", "A/B Testing", "Data Visualization"],
    "NLP Sentiment Analysis": ["Python", "NLP", "Machine Learning", "Pandas", "Scikit-learn"],
    "Feature Engineering Pipeline": ["Python", "Feature Engineering", "Pandas", "NumPy", "Scikit-learn"],
    "TypeScript App": ["TypeScript", "JavaScript", "React", "HTML/CSS"],
}

ROLE_SKILLS = {
    "Data Scientist": ["Python", "Statistics", "SQL", "Data Visualization", "Pandas", "NumPy",
                       "Machine Learning", "Feature Engineering", "Scikit-learn", "Deep Learning",
                       "NLP", "ML Deployment", "A/B Testing"],
    "Backend Developer": ["Python", "SQL", "REST APIs", "Git", "Linux/Bash", "Django/Flask/FastAPI",
                          "Database Design", "Authentication/Security", "Unit Testing",
                          "Message Queues", "Docker", "CI/CD", "Microservices"],
    "ML Engineer": ["Python", "Machine Learning", "Statistics", "SQL", "Pandas", "NumPy",
                    "Deep Learning", "Scikit-learn", "Model Optimization", "ML Deployment",
                    "MLOps", "Docker", "Feature Engineering"],
    "Frontend Developer": ["HTML/CSS", "JavaScript", "Responsive Design", "Git", "React",
                           "State Management", "REST APIs", "TypeScript", "CSS Frameworks",
                           "Testing (Jest/RTL)", "Performance Optimization", "Webpack/Vite",
                           "Accessibility (a11y)"],
}

ROLE_WEIGHTS = {
    "Data Scientist": {"Python": 0.95, "Statistics": 0.90, "SQL": 0.85, "Data Visualization": 0.75,
                       "Pandas": 0.88, "NumPy": 0.82, "Machine Learning": 0.92, "Feature Engineering": 0.78,
                       "Scikit-learn": 0.85, "Deep Learning": 0.72, "NLP": 0.65, "ML Deployment": 0.68,
                       "A/B Testing": 0.60},
    "Backend Developer": {"Python": 0.88, "SQL": 0.90, "REST APIs": 0.95, "Git": 0.80, "Linux/Bash": 0.75,
                          "Django/Flask/FastAPI": 0.88, "Database Design": 0.85, "Authentication/Security": 0.82,
                          "Unit Testing": 0.78, "Message Queues": 0.70, "Docker": 0.80, "CI/CD": 0.72,
                          "Microservices": 0.65},
    "ML Engineer": {"Python": 0.95, "Machine Learning": 0.95, "Statistics": 0.85, "SQL": 0.78,
                    "Pandas": 0.85, "NumPy": 0.82, "Deep Learning": 0.88, "Scikit-learn": 0.80,
                    "Model Optimization": 0.78, "ML Deployment": 0.92, "MLOps": 0.88, "Docker": 0.82,
                    "Feature Engineering": 0.75},
    "Frontend Developer": {"HTML/CSS": 0.95, "JavaScript": 0.95, "Responsive Design": 0.85, "Git": 0.80,
                           "React": 0.92, "State Management": 0.82, "REST APIs": 0.80, "TypeScript": 0.78,
                           "CSS Frameworks": 0.72, "Testing (Jest/RTL)": 0.75,
                           "Performance Optimization": 0.70, "Webpack/Vite": 0.68, "Accessibility (a11y)": 0.65},
}

EXPERIENCE_SKILL_COUNTS = {
    "Beginner": (1, 4),
    "Intermediate": (3, 8),
    "Advanced": (6, 13),
}

ALL_SKILLS = sorted(set(s for skills in ROLE_SKILLS.values() for s in skills))
ALL_PROJECTS = list(PROJECT_TO_SKILLS.keys())
ROLES = list(ROLE_SKILLS.keys())
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]


def compute_fit_score(current_skills, role, experience_level):
    role_skill_weights = ROLE_WEIGHTS[role]
    total_weight = sum(role_skill_weights.values())
    matched_weight = sum(role_skill_weights.get(s, 0) for s in current_skills if s in role_skill_weights)
    base_score = matched_weight / total_weight
    exp_bonus = {"Beginner": 0.0, "Intermediate": 0.05, "Advanced": 0.10}[experience_level]
    noise = np.random.normal(0, 0.05)
    raw_score = base_score + exp_bonus + noise
    return int(np.clip(raw_score, 0.0, 1.0) >= 0.55)


def generate_synthetic_dataset(n_samples=2500, seed=42):
    np.random.seed(seed)
    records = []

    samples_per_role = n_samples // len(ROLES)

    for role in ROLES:
        role_skills = ROLE_SKILLS[role]
        role_weights_dict = ROLE_WEIGHTS[role]

        for i in range(samples_per_role):
            exp_level = np.random.choice(EXPERIENCE_LEVELS, p=[0.35, 0.40, 0.25])
            min_s, max_s = EXPERIENCE_SKILL_COUNTS[exp_level]
            n_skills = np.random.randint(min_s, max_s + 1)

            skill_weights_arr = np.array([role_weights_dict.get(s, 0.3) for s in role_skills])
            skill_probs = skill_weights_arr / skill_weights_arr.sum()

            n_role_skills = min(n_skills, len(role_skills))
            chosen_role_skills = np.random.choice(role_skills, size=n_role_skills,
                                                   replace=False, p=skill_probs).tolist()

            n_extra = np.random.randint(0, 3)
            other_skills = [s for s in ALL_SKILLS if s not in role_skills]
            extra_skills = np.random.choice(other_skills, size=min(n_extra, len(other_skills)),
                                            replace=False).tolist() if other_skills else []

            current_skills = list(set(chosen_role_skills + extra_skills))

            n_projects = np.random.randint(0, 4)
            projects_list = np.random.choice(ALL_PROJECTS, size=min(n_projects, len(ALL_PROJECTS)),
                                             replace=False).tolist()

            derived_skills = set(current_skills)
            for proj in projects_list:
                derived_skills.update(PROJECT_TO_SKILLS.get(proj, []))

            label = compute_fit_score(list(derived_skills), role, exp_level)

            records.append({
                "student_id": f"STU{len(records):05d}",
                "current_skills": "|".join(current_skills),
                "target_role": role,
                "projects": "|".join(projects_list),
                "experience_level": exp_level,
                "label_fit": label,
            })

    remainder = n_samples - len(records)
    if remainder > 0:
        for i in range(remainder):
            role = np.random.choice(ROLES)
            exp_level = np.random.choice(EXPERIENCE_LEVELS)
            role_skills = ROLE_SKILLS[role]
            min_s, max_s = EXPERIENCE_SKILL_COUNTS[exp_level]
            n_skills = np.random.randint(min_s, max_s + 1)
            current_skills = np.random.choice(role_skills, size=min(n_skills, len(role_skills)),
                                               replace=False).tolist()
            projects_list = np.random.choice(ALL_PROJECTS, size=np.random.randint(0, 4),
                                             replace=False).tolist()
            derived_skills = set(current_skills)
            for proj in projects_list:
                derived_skills.update(PROJECT_TO_SKILLS.get(proj, []))
            label = compute_fit_score(list(derived_skills), role, exp_level)
            records.append({
                "student_id": f"STU{len(records):05d}",
                "current_skills": "|".join(current_skills),
                "target_role": role,
                "projects": "|".join(projects_list),
                "experience_level": exp_level,
                "label_fit": label,
            })

    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


def parse_pipe_separated(series):
    return series.apply(lambda x: [s.strip() for s in x.split("|") if s.strip()] if isinstance(x, str) else [])


def derive_skills_from_projects(projects_list):
    derived = set()
    for proj in projects_list:
        derived.update(PROJECT_TO_SKILLS.get(proj, []))
    return list(derived)


def build_unified_skill_list(current_skills, project_derived_skills):
    return list(set(current_skills + project_derived_skills))


def preprocess_dataset(df):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    skill_lists = parse_pipe_separated(df["current_skills"])
    project_lists = parse_pipe_separated(df["projects"])

    project_derived = project_lists.apply(derive_skills_from_projects)
    unified_skills = skill_lists.combine(project_derived, func=build_unified_skill_list)

    skill_mlb = MultiLabelBinarizer()
    skill_mlb.fit([ALL_SKILLS])
    X_skills = skill_mlb.transform(unified_skills)

    role_enc = LabelEncoder()
    role_enc.fit(ROLES)
    X_role = role_enc.transform(df["target_role"]).reshape(-1, 1)

    exp_enc = LabelEncoder()
    exp_enc.fit(EXPERIENCE_LEVELS)
    X_exp = exp_enc.transform(df["experience_level"]).reshape(-1, 1)

    X = np.hstack([X_skills, X_role, X_exp])
    y = df["label_fit"].values

    joblib.dump(skill_mlb, os.path.join(ARTIFACTS_DIR, "skill_encoder.pkl"))
    joblib.dump(role_enc, os.path.join(ARTIFACTS_DIR, "role_encoder.pkl"))
    joblib.dump(exp_enc, os.path.join(ARTIFACTS_DIR, "exp_encoder.pkl"))

    return X, y, skill_mlb, role_enc, exp_enc


if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = generate_synthetic_dataset(n_samples=2500)
    output_path = os.path.join(PROCESSED_DIR, "training_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    print(df["label_fit"].value_counts())
    X, y, *_ = preprocess_dataset(df)
    print(f"Feature matrix shape: {X.shape}")
