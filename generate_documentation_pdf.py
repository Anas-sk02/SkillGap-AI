import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "SkillGap_AI_Complete_Documentation_Hinglish.pdf")

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to compute total page count dynamically"""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Cover page doesn't need header/footer
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Header
        self.drawString(54, 11 * inch - 36, "SkillGap AI — Complete Architecture & Implementation Manual (Hinglish)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Running Footer
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.drawString(54, 32, "Confidential & Proprietary — SkillGap AI Project Core Engine")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)
        self.restoreState()


def create_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#1e1b4b")     # Deep indigo
    SECONDARY = colors.HexColor("#4338ca")   # Indigo
    ACCENT = colors.HexColor("#0284c7")      # Sky blue
    DARK_TEXT = colors.HexColor("#0f172a")   # Slate 900
    MUTED_TEXT = colors.HexColor("#475569")  # Slate 600
    LIGHT_BG = colors.HexColor("#f8fafc")    # Slate 50
    CARD_BG = colors.HexColor("#f1f5f9")     # Slate 100
    BORDER_COLOR = colors.HexColor("#e2e8f0")# Slate 200
    SUCCESS_COLOR = colors.HexColor("#16a34a")

    # Typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=PRIMARY,
        spaceAfter=12,
        alignment=0,
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        spaceAfter=24,
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        'BodyHinglish',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=DARK_TEXT,
        spaceAfter=7,
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold',
    )
    bullet_style = ParagraphStyle(
        'BulletHinglish',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=DARK_TEXT,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4,
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceAfter=8,
    )
    callout_style = ParagraphStyle(
        'CalloutStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        backColor=colors.HexColor("#eff6ff"),
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=10,
    )

    story = []

    # ==========================================
    # COVER / TITLE BLOCK
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("SkillGap AI — Complete Project Documentation", title_style))
    story.append(Paragraph("Har ek Module, Algorithm, Preprocessing, aur Frontend-Backend Implementation ka Detailed Hinglish Breakdown", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=SECONDARY, spaceBefore=0, spaceAfter=15))

    meta_table_data = [
        [Paragraph("<b>Project Name:</b> SkillGap AI", body_style), Paragraph("<b>Tech Stack:</b> React + Vite, FastAPI, Scikit-Learn, SQLite", body_style)],
        [Paragraph("<b>Author / Team:</b> IDEA Lab", body_style), Paragraph("<b>Coverage:</b> 16 Tech Roles, 128 Skills, 36 Projects", body_style)],
        [Paragraph("<b>Dataset:</b> 8,000 Synthetic Samples", body_style), Paragraph("<b>Production Model:</b> Random Forest Classifier (88.4% Acc)", body_style)],
        [Paragraph("<b>Date:</b> March 2026", body_style), Paragraph("<b>Language:</b> Hinglish (Practical Explanations)", body_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[240, 260])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 1: INTRODUCTION & CORE PURPOSE
    # ==========================================
    story.append(Paragraph("1. Project ka Aim aur Core Problem Kya Hai?", h1_style))
    story.append(Paragraph(
        "<b>Asli Problem:</b> Aaj kal students aur freshers ko pata nahi hota ki kisi specific job role (jaise AI Engineer, DevOps Engineer, Full Stack Developer) ke liye unke paas kaun si skills missing hain. Wo random courses karte rehte hain jisse time waste hota hai.",
        body_style
    ))
    story.append(Paragraph(
        "<b>SkillGap AI ka Solution:</b> Ye system student ka current skill set, unke kiye hue projects, target role aur experience level input leta hai. Fir ek <b>Trained Machine Learning Model (Random Forest)</b> ke zariye ye pata lagata hai ki candidate us role ke liye kitne percent ready hai (Match Percentage). Saath hi ek <b>Role-Skill Taxonomy</b> se missing skills find karta hai aur 3 stages (Foundational, Intermediate, Applied) mein <b>Visual Learning Roadmap</b> deta hai jise student track bhi kar sakta hai.",
        body_style
    ))

    # ==========================================
    # SECTION 2: REPOSITORY ARCHITECTURE
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Project Folder Structure & File Responsibilities", h1_style))
    story.append(Paragraph(
        "Poora project 3 main layers mein divided hai: <b>Machine Learning (ml/)</b>, <b>Backend API (backend/)</b>, aur <b>Frontend (frontend/)</b>.",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>File / Folder Path</b>", body_bold), Paragraph("<b>Ye File Kya Kaam Karti Hai? (Role in Project)</b>", body_bold)],
        [Paragraph("<code>data/processed/role_skill_taxonomy.json</code>", body_style), Paragraph("Taxonomy file: Isme 16 roles, 128 skills, har skill ka stage aur importance weight define hai.", body_style)],
        [Paragraph("<code>data/processed/training_data.csv</code>", body_style), Paragraph("8,000 synthetic student profiles ka dataset (current_skills, target_role, projects, label_fit).", body_style)],
        [Paragraph("<code>ml/preprocessing.py</code>", body_style), Paragraph("Synthetic data generator + Project-to-skill mapper + MultiLabelBinarizer aur LabelEncoders.", body_style)],
        [Paragraph("<code>ml/train_model.py</code>", body_style), Paragraph("Random Forest, SVM, Naive Bayes ko train karke benchmark karta hai aur .pkl artifacts save karta hai.", body_style)],
        [Paragraph("<code>ml/model_artifacts/</code>", body_style), Paragraph("Saved models: random_forest_model.pkl, skill_encoder.pkl, role_encoder.pkl, exp_encoder.pkl.", body_style)],
        [Paragraph("<code>backend/main.py</code>", body_style), Paragraph("FastAPI app entry point: CORS setup, SQLite database initialization, aur API routes registration.", body_style)],
        [Paragraph("<code>backend/routes/</code>", body_style), Paragraph("API endpoints: /roles (catalogue), /skillgap (ML prediction), /roadmap, /progress (tracking).", body_style)],
        [Paragraph("<code>backend/services/prediction_service.py</code>", body_style), Paragraph("Real-time ML Inference: Encoders load karta hai aur Random Forest se match % calculate karta hai.", body_style)],
        [Paragraph("<code>backend/services/roadmap_service.py</code>", body_style), Paragraph("Roadmap generator: Missing skills ko Foundational -> Intermediate -> Applied mein group karta hai.", body_style)],
        [Paragraph("<code>frontend/src/pages/</code>", body_style), Paragraph("React UI pages: Home (landing & stats), Dashboard (gap analysis), Explore (roles catalogue).", body_style)],
        [Paragraph("<code>frontend/src/components/</code>", body_style), Paragraph("Reusable UI: ProfileForm, MatchGauge (animated radial gauge), VisualRoadmap, ProgressTracker.", body_style)],
    ]
    arch_table = Table(arch_data, colWidths=[175, 325])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)

    story.append(PageBreak())

    # ==========================================
    # SECTION 3: ROLE-SKILL TAXONOMY
    # ==========================================
    story.append(Paragraph("3. Role-Skill Taxonomy & Data Foundation", h1_style))
    story.append(Paragraph(
        "Taxonomy is project ka brain hai. Ye decide karti hai ki kaun si role ke liye kya-kya zaroori hai. Ye data <code>role_skill_taxonomy.json</code> mein store hota hai.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Har Role ke andar kya hota hai:</b><br/>"
        "• <b>Skills List:</b> Har skill ka naam (e.g. 'Docker', 'PyTorch', 'SQL').<br/>"
        "• <b>Stage:</b> Teen stages hoti hain — <i>Foundational</i> (Must-have basic), <i>Intermediate</i> (Core engineering), <i>Applied</i> (Production/Advanced tool).<br/>"
        "• <b>Weight:</b> 0.3 se lekar 1.0 tak importance score. Core skill ka weight 0.8-1.0 hota hai, jabki optional ka 0.3-0.5.",
        body_style
    ))

    taxonomy_roles_summary = [
        [Paragraph("<b>Category</b>", body_bold), Paragraph("<b>Roles Covered (Total 16 Roles)</b>", body_bold), Paragraph("<b>Key Benchmark Skills</b>", body_bold)],
        [Paragraph("AI & Data", body_style), Paragraph("Data Scientist, ML Engineer, AI Engineer, Data Engineer", body_style), Paragraph("Python, PyTorch, RAG, LLM Fine-Tuning, Spark, Airflow, Scikit-learn", body_style)],
        [Paragraph("Software & Web", body_style), Paragraph("Backend Developer, Frontend Developer, Full Stack, Java Developer", body_style), Paragraph("React, Node.js, Spring Boot, REST APIs, Microservices, TypeScript", body_style)],
        [Paragraph("Cloud & DevOps", body_style), Paragraph("DevOps Engineer, Cloud Engineer, Cybersecurity Analyst", body_style), Paragraph("Kubernetes, Docker, Terraform, AWS, SIEM, Wireshark, Linux/Bash", body_style)],
        [Paragraph("Specialized", body_style), Paragraph("Mobile App, QA Automation, Blockchain, Game, Embedded Systems", body_style), Paragraph("Flutter, Cypress, Solidity, Smart Contracts, Unity/C#, C/C++, FreeRTOS", body_style)],
    ]
    tax_table = Table(taxonomy_roles_summary, colWidths=[100, 210, 190])
    tax_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tax_table)
    story.append(Spacer(1, 10))

    # Project-to-skill mapping
    story.append(Paragraph("Project-to-Skill Implicit Deduction (Smart Inference):", h2_style))
    story.append(Paragraph(
        "Real life mein jab student bolta hai ki usne <i>'Kubernetes CI/CD Pipeline'</i> banaya hai, toh iska matlab use <code>Docker</code>, <code>CI/CD</code>, <code>Linux/Bash</code>, aur <code>Kubernetes</code> pehle se aate hain. Humara <code>PROJECT_TO_SKILLS</code> dictionary 36 projects ko map karke unke underlying skills automatically student ke profile mein include kar leta hai.",
        body_style
    ))

    # ==========================================
    # SECTION 4: SYNTHETIC DATA GENERATION & LABELING
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Dataset Kaise Bana? (Synthetic Generation & Ground Truth)", h1_style))
    story.append(Paragraph(
        "Real student data ka lack of label issue solve karne ke liye <code>generate_synthetic_dataset(n_samples=8000)</code> banaya gaya.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Step-by-step Generation Logic:</b><br/>"
        "1. <b>16 Roles x 500 Samples = 8,000 Rows:</b> Har role ke barabar samples generate hote hain taaki class imbalance na ho.<br/>"
        "2. <b>Experience Distribution:</b> 35% Beginner, 40% Intermediate, 25% Advanced.<br/>"
        "3. <b>Weighted Skill Sampling:</b> High-weight skills ke choose hone ki probability zyada hoti hai.<br/>"
        "4. <b>Realistic Noise:</b> Har profile mein 0 se 3 random non-role skills bhi add hoti hain (real students ki tarah).<br/>"
        "5. <b>Projects Assignment:</b> Har student ko 0 se 3 random projects assign hote hain.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Ground Truth Label Formula (Kaise decide hua ki student FIT hai ya nahi):", h2_style))
    story.append(Paragraph(
        "<code>compute_fit_score()</code> function niche diye formula se label 1 ya 0 assign karta hai:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Matched_Weight</b> = Student ke paas jo role skills hain unke weights ka sum<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Total_Weight</b> = Us role ke sabhi required skills ke weights ka sum<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Base_Score</b> = Matched_Weight / Total_Weight<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Exp_Bonus</b> = Beginner (+0.00), Intermediate (+0.05), Advanced (+0.10)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Noise</b> = Gaussian random noise ~ N(0, 0.05) [Interviews ki uncertainty simulate karne ke liye]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Final Score</b> = Base_Score + Exp_Bonus + Noise<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Agar Final Score &gt;= 0.55</b> -&gt; <b>label_fit = 1 (Ready)</b>, warna <b>0 (Gap Exists)</b>.",
        callout_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: FEATURE ENGINEERING & PREPROCESSING
    # ==========================================
    story.append(Paragraph("5. Feature Engineering: Machine Learning Input Matrix", h1_style))
    story.append(Paragraph(
        "Machine learning model raw strings (jaise 'Python|Docker') direct nahi padh sakta. Isliye <code>preprocess_dataset()</code> data ko mathematical form mein transform karta hai:",
        body_style
    ))

    fe_data = [
        [Paragraph("<b>Step</b>", body_bold), Paragraph("<b>Technique</b>", body_bold), Paragraph("<b>Dimensions</b>", body_bold), Paragraph("<b>Explanation (Hinglish)</b>", body_bold)],
        [
            Paragraph("1. Skills Vectorization", body_style),
            Paragraph("<code>MultiLabelBinarizer</code>", body_style),
            Paragraph("8,000 x 128", body_style),
            Paragraph("Sabhi 128 unique skills ka one-hot/multi-hot vector banta hai. Agar student ke paas skill hai toh column mein 1, nahi toh 0.", body_style)
        ],
        [
            Paragraph("2. Target Role Encoding", body_style),
            Paragraph("<code>LabelEncoder</code>", body_style),
            Paragraph("8,000 x 1", body_style),
            Paragraph("16 roles ko 0 se 15 ke integer codes mein convert karta hai (e.g. AI Engineer=0, Backend=1, etc.).", body_style)
        ],
        [
            Paragraph("3. Experience Level Encoding", body_style),
            Paragraph("<code>LabelEncoder</code>", body_style),
            Paragraph("8,000 x 1", body_style),
            Paragraph("Experience levels ko 0 (Beginner), 1 (Intermediate), 2 (Advanced) code deta hai.", body_style)
        ],
        [
            Paragraph("4. Feature Stacking", body_style),
            Paragraph("<code>np.hstack([X_skills, X_role, X_exp])</code>", body_style),
            Paragraph("<b>8,000 x 130</b>", body_style),
            Paragraph("Final Feature Matrix X banti hai jisme 130 columns hote hain (128 skills + 1 role + 1 experience).", body_style)
        ]
    ]
    fe_table = Table(fe_data, colWidths=[90, 110, 75, 225])
    fe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(fe_table)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 6: MODEL TRAINING & BENCHMARKING
    # ==========================================
    story.append(Paragraph("6. Model Training, Comparison aur Final Selection", h1_style))
    story.append(Paragraph(
        "8,000 samples ko <b>80% Train Set (6,400 rows)</b> aur <b>20% Test Set (1,600 rows)</b> mein split kiya gaya (<code>stratify=y</code> ke saath taaki class ratio maintain rahe). Humne 3 models ko benchmark kiya:",
        body_style
    ))

    bench_data = [
        [Paragraph("<b>Model Name</b>", body_bold), Paragraph("<b>Accuracy</b>", body_bold), Paragraph("<b>Precision</b>", body_bold), Paragraph("<b>Recall</b>", body_bold), Paragraph("<b>F1-Score</b>", body_bold), Paragraph("<b>Status & Verdict</b>", body_bold)],
        [Paragraph("<b>Random Forest</b>", body_style), Paragraph("<b>88.44%</b>", body_style), Paragraph("<b>92.61%</b>", body_style), Paragraph("<b>86.62%</b>", body_style), Paragraph("<b>89.52%</b>", body_style), Paragraph("<b>DEPLOYED (Winner)</b>", body_bold)],
        [Paragraph("SVM (RBF Kernel)", body_style), Paragraph("83.56%", body_style), Paragraph("83.98%", body_style), Paragraph("87.94%", body_style), Paragraph("85.91%", body_style), Paragraph("Good, but lacks calibrated proba", body_style)],
        [Paragraph("Naive Bayes", body_style), Paragraph("68.87%", body_style), Paragraph("74.24%", body_style), Paragraph("69.52%", body_style), Paragraph("71.80%", body_style), Paragraph("Baseline (Assumes feature independence)", body_style)],
    ]
    bench_table = Table(bench_data, colWidths=[100, 65, 65, 65, 65, 140])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Kyun Random Forest ko Production Model chuna gaya?", h2_style))
    story.append(Paragraph(
        "1. <b>Non-linear Interactions:</b> Real life mein skills akele kaam nahi karti — jaise <i>React + TypeScript</i> ya <i>Docker + Kubernetes</i> ka combination bohot powerful hota hai. Decision trees aisi combinations ko natural split se sikh lete hain.<br/>"
        "2. <b>predict_proba() Support:</b> Random Forest 200 decision trees ke votes ko average karke exact probability deta hai (e.g. 0.742). Yahi calibrated probability hamare frontend ka <b>74.2% Match Score Gauge</b> banati hai.<br/>"
        "3. <b>High Precision (92.6%):</b> Jab model kisi ko 'Fit' bolta hai, toh 92.6% chances hain ki candidate sach me fit hai (false positive risk minimal hai).",
        bullet_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 7: BACKEND API ARCHITECTURE
    # ==========================================
    story.append(Paragraph("7. Backend API Architecture (FastAPI + Services)", h1_style))
    story.append(Paragraph(
        "Backend <b>FastAPI</b> framework par bana hai jo bohot fast aur asynchronous execution provide karta hai. Isme 5 primary API endpoints hain:",
        body_style
    ))

    api_data = [
        [Paragraph("<b>Endpoint & Method</b>", body_bold), Paragraph("<b>Input Request</b>", body_bold), Paragraph("<b>Internal Service Logic</b>", body_bold), Paragraph("<b>Output Response</b>", body_bold)],
        [
            Paragraph("<code>GET /api/roles</code>", body_style),
            Paragraph("None", body_style),
            Paragraph("<code>_load_taxonomy()</code> cached JSON read karta hai.", body_style),
            Paragraph("16 roles ki full list with skills & stages.", body_style)
        ],
        [
            Paragraph("<code>POST /api/skillgap</code>", body_style),
            Paragraph("<code>student_id, current_skills, target_role, projects, experience_level</code>", body_style),
            Paragraph("<code>prediction_service.predict()</code>: 130-dim vector banata hai, <code>predict_proba</code> se match % nikalta hai, missing skills filter karta hai.", body_style),
            Paragraph("<code>match_percentage</code> (0-100%), <code>missing_skills</code> (with weights & stages).", body_style)
        ],
        [
            Paragraph("<code>POST /api/roadmap</code>", body_style),
            Paragraph("Same profile payload", body_style),
            Paragraph("<code>roadmap_service.generate_roadmap()</code>: Missing skills ko Foundational, Intermediate, Applied mein group karta hai.", body_style),
            Paragraph("Stage-wise learning sequence with estimated effort.", body_style)
        ],
        [
            Paragraph("<code>POST /api/progress</code>", body_style),
            Paragraph("<code>student_id, role, skill_name, completed</code>", body_style),
            Paragraph("SQLite database (<code>progress.db</code>) mein row insert ya update karta hai.", body_style),
            Paragraph("<code>success: true, updated_score</code>", body_style)
        ],
        [
            Paragraph("<code>GET /api/progress/{id}/{role}</code>", body_style),
            Paragraph("Path parameters", body_style),
            Paragraph("Database se student ke completed skills fetch karta hai.", body_style),
            Paragraph("List of completed skills for that role.", body_style)
        ]
    ]
    api_table = Table(api_data, colWidths=[110, 110, 160, 120])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(api_table)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 8: FRONTEND REACT ARCHITECTURE
    # ==========================================
    story.append(Paragraph("8. Frontend React Components & Dynamic UI", h1_style))
    story.append(Paragraph(
        "Frontend React 18 + Vite ke saath banaya gaya hai. Koi heavy CSS library nahi balki highly optimized, modern dark-mode vanilla CSS use ki gayi hai:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>ProfileForm.jsx:</b> Target Role dropdown (sab 16 roles dynamic load karta hai). Skills aur Projects ke liye TagInput with live auto-suggestions dropdown.<br/>"
        "• <b>MatchGauge.jsx:</b> Pure SVG-based radial circular progress meter jo 0% se target percentage tak smooth easeOutCubic transition animate karta hai.<br/>"
        "• <b>SkillGapReport.jsx:</b> Present skills ko green badges aur missing skills ko weight indicators ke saath display karta hai.<br/>"
        "• <b>VisualRoadmap.jsx:</b> 3-column stage layout (Foundational -> Intermediate -> Applied) jisme step-by-step milestones dikhte hain.<br/>"
        "• <b>ProgressTracker.jsx:</b> Har missing skill ke aage interactive checkbox. User tick karta hai toh real-time SQLite update hota hai aur readiness meter badhta hai.<br/>"
        "• <b>RolesCatalogue.jsx:</b> Explore page jisme 16 roles ke custom cards, emojis, descriptions aur skill distributions dikhte hain.",
        bullet_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 9: COMPLETE END-TO-END FLOW
    # ==========================================
    story.append(Paragraph("9. End-to-End Execution: Click Se Output Tak Kya Hota Hai?", h1_style))
    story.append(Paragraph(
        "Jab koi user website par aata hai aur apna gap analyze karta hai, toh background mein exact kya steps execute hote hain:",
        body_style
    ))

    flow_steps = [
        ("Step 1: User Profile Fill Karta Hai", "User Target Role (e.g. 'DevOps Engineer') select karta hai, experience 'Intermediate' chunta hai, aur skills ('Linux/Bash', 'Docker') add karta hai."),
        ("Step 2: Frontend API Call", "ProfileForm JSON payload banakar Axios client ke through <code>POST /api/skillgap</code> aur <code>POST /api/roadmap</code> ko parallel call karta hai."),
        ("Step 3: Project Deductions", "Backend service dekhti hai agar student ne koi project mention kiya hai, toh uske underlying skills ko extract karke <code>unified_skills</code> list mein merge kar deti hai."),
        ("Step 4: Vectorization & Encoding", "<code>skill_encoder.pkl</code> 128-dim binary array banata hai. <code>role_encoder.pkl</code> role ko integer code deta hai. Dono stack hokar 130-dim vector banate hain."),
        ("Step 5: Random Forest Predicts", "<code>random_forest_model.predict_proba(X)</code> probability nikalta hai. Class 1 ka probability float multiply by 100 bankar <code>match_percentage</code> ban jata hai (e.g. 68.5%)."),
        ("Step 6: Gap & Roadmap Computation", "Taxonomy se role ki required skills compare hoti hain. Jo skills student ke paas nahi hain unhe Foundational, Intermediate, Applied stages mein arrange kiya jata hai."),
        ("Step 7: UI Rendering & Tracking", "Frontend par Match Gauge animate hota hai, Gap analysis open hoti hai, aur Progress tracker activate ho jata hai."),
    ]
    for title, desc in flow_steps:
        story.append(Paragraph(f"<b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 10: RUNNING & TESTING COMMANDS
    # ==========================================
    story.append(Paragraph("10. Project Run, Retrain aur Test Karne Ke Commands", h1_style))
    story.append(Paragraph(
        "Project ko run aur manage karne ke liye ye standard commands use kiye jate hain:",
        body_style
    ))

    story.append(Paragraph("<b>1. Backend Start Karna (FastAPI on Port 8000):</b>", body_style))
    story.append(Paragraph("cd SkillGap-AI<br/>uvicorn backend.main:app --reload --port 8000", code_style))

    story.append(Paragraph("<b>2. Frontend Start Karna (Vite Dev Server on Port 5173):</b>", body_style))
    story.append(Paragraph("cd SkillGap-AI/frontend<br/>npm run dev", code_style))

    story.append(Paragraph("<b>3. Machine Learning Model Re-train Karna:</b>", body_style))
    story.append(Paragraph("cd SkillGap-AI<br/>python ml/train_model.py", code_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Summary:</b> Ye project sirf ek simple CRUD application nahi hai, balki ek complete <b>ML-integrated Career Intelligence Platform</b> hai jo realistic data synthesis, multi-label binarization, ensemble classification, aur dynamic reactive frontend ko seamlessly combine karta hai.",
        callout_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    create_pdf()
