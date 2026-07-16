
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Diabetes Analytic System", page_icon=":notebook:", layout="wide")


PULSE_SVG = (
    '<svg class="pulse-line" viewBox="0 0 600 40" preserveAspectRatio="none" '
    'xmlns="http://www.w3.org/2000/svg"><polyline points="0,20 130,20 150,20 165,4 180,36 195,20 220,20 235,10 250,30 265,20 600,20" '
    'fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

:root{
    --bg:#DCEAE8;
    --bg-deep:#C9DEDB;
    --surface:#FFFFFF;
    --ink:#16333B;
    --muted:#5C7079;
    --accent:#1E7F7A;
    --accent-strong:#0F5C57;
    --accent-soft:#E4F2F1;
    --alert:#D64550;
    --alert-soft:#FBE8E9;
    --line:#E1E8E8;

    /* Sidebar — dark, soothing */
    --side-bg:#111A24;
    --side-bg-elev:#182432;
    --side-text:#E6EEF1;
    --side-muted:#8FA5B0;
    --side-accent:#5FD8C6;
    --side-accent-soft:rgba(95,216,198,0.16);
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
    color:var(--ink);
}

.stApp{
    background:linear-gradient(160deg, var(--bg) 0%, var(--bg-deep) 55%, var(--bg) 100%);
    background-attachment:fixed;
}

/* ---------- Headings ---------- */
h1, h2, h3, .app-title{
    font-family:'Space Grotesk', sans-serif !important;
    color:var(--ink) !important;
    letter-spacing:-0.01em;
}

/* ---------- Sidebar: dark, soothing ---------- */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg, var(--side-bg) 0%, #0C141C 100%);
    border-right:1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] *{
    color:var(--side-text) !important;
}
section[data-testid="stSidebar"] .sidebar-caption{
    color:var(--side-accent) !important;
    font-size:0.78rem;
    letter-spacing:0.08em;
    text-transform:uppercase;
    font-weight:600;
    margin-bottom:0.2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:var(--side-text) !important;
}

section[data-testid="stSidebar"] .nav-link,
section[data-testid="stSidebar"] .nav-link span,
section[data-testid="stSidebar"] .nav-link div,
section[data-testid="stSidebar"] .nav-link p{
    color:var(--side-text) !important;
    font-weight:500 !important;
    opacity:1 !important;
}
section[data-testid="stSidebar"] .nav-link i,
section[data-testid="stSidebar"] .nav-link svg{
    color:var(--side-accent) !important;
    fill:var(--side-accent) !important;
}
section[data-testid="stSidebar"] .nav-link{
    background-color:var(--side-bg-elev) !important;
    border:1px solid rgba(255,255,255,0.05) !important;
    margin:4px 0 !important;
    border-radius:10px !important;
    transition:background-color 0.15s ease;
}
section[data-testid="stSidebar"] .nav-link:hover{
    background-color:var(--side-accent-soft) !important;
}
section[data-testid="stSidebar"] .nav-link-selected,
section[data-testid="stSidebar"] .nav-link-selected span,
section[data-testid="stSidebar"] .nav-link-selected div,
section[data-testid="stSidebar"] .nav-link-selected p,
section[data-testid="stSidebar"] .nav-link-selected i,
section[data-testid="stSidebar"] .nav-link-selected svg{
    background-color:var(--side-accent) !important;
    color:#0C141C !important;
    fill:#0C141C !important;
    font-weight:600 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]{
    background-color:var(--side-accent) !important;
    color:#0C141C !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
    background-color:var(--side-bg-elev) !important;
    border-color:rgba(255,255,255,0.12) !important;
}

section[data-testid="stSidebar"] div[data-testid="stIFrame"],
section[data-testid="stSidebar"] iframe{
    background-color:var(--side-bg) !important;
}

/* ---------- Header banner ---------- */
.dashboard-header{
    background:linear-gradient(120deg, var(--accent-strong) 0%, var(--accent) 100%);
    padding:1.6rem 2rem;
    border-radius:16px;
    margin-bottom:1.4rem;
    box-shadow:0 8px 24px rgba(15,92,87,0.18);
}
.dashboard-header .app-title{
    color:#FFFFFF !important;
    font-size:2rem;
    font-weight:700;
    margin:0;
}
.dashboard-header .app-subtitle{
    color:#DCEFEE;
    font-size:0.95rem;
    margin-top:0.25rem;
}
.dashboard-header .pulse-line{
    color:#FFFFFF;
    opacity:0.85;
    width:100%;
    height:22px;
    margin-top:0.6rem;
}

/* ---------- Section header w/ pulse divider ---------- */
.section-header{
    margin-top:0.6rem;
    margin-bottom:0.4rem;
}
.section-header .section-title{
    font-family:'Space Grotesk', sans-serif;
    font-weight:600;
    font-size:1.25rem;
    color:var(--ink);
    display:flex;
    align-items:center;
    gap:0.5rem;
}
.section-header .pulse-line{
    color:var(--accent);
    width:100%;
    height:14px;
    margin:0.25rem 0 0.9rem 0;
    opacity:0.9;
}

/* ---------- Metric cards ---------- */
div[data-testid="stMetric"]{
    background:var(--surface);
    border:1px solid var(--line);
    border-left:4px solid var(--accent);
    border-radius:12px;
    padding:0.9rem 1rem 0.7rem 1rem;
    box-shadow:0 2px 10px rgba(22,51,59,0.05);
}
div[data-testid="stMetricLabel"]{
    color:var(--muted) !important;
    font-weight:500;
}
div[data-testid="stMetricValue"]{
    font-family:'JetBrains Mono', monospace !important;
    color:var(--accent-strong) !important;
}

/* ---------- Generic content card ----------
   FIX: this used to be applied via st.markdown('<div class="info-card">')
   opened in one call and closed in another. Streamlit renders every
   st.markdown() call as its own isolated HTML fragment, so the browser
   auto-closed that <div> immediately with nothing inside it — producing
   an empty white rounded box (this class's background/padding/shadow
   with no children), while the real subheader/chart/etc rendered as
   separate sibling elements right after it, unstyled.

   Real fix: use st.container(key=...) (a genuine DOM node Streamlit lets
   you nest content inside) and target the class Streamlit assigns to it
   ("st-key-<key>") instead of hand-rolled div tags. See info_card()
   helper below. */
div[class*="st-key-infocard_"]{
    background:var(--surface);
    border:1px solid var(--line);
    border-radius:14px;
    padding:1.1rem 1.3rem;
    margin-bottom:1rem;
    box-shadow:0 2px 10px rgba(22,51,59,0.05);
}
div[class*="st-key-infocard_"] h4{
    margin-top:0;
    font-family:'Space Grotesk', sans-serif;
    color:var(--accent-strong);
}
div[class*="st-key-infocard_"] p{
    color:var(--muted);
    margin-bottom:0.3rem;
}

/* ---------- Insight callouts ---------- */
.insight-note{
    background:var(--accent-soft);
    border-left:4px solid var(--accent);
    border-radius:8px;
    padding:0.6rem 0.9rem;
    color:var(--accent-strong);
    font-size:0.92rem;
    margin:0.4rem 0 1.1rem 0;
}
.risk-note{
    background:var(--alert-soft);
    border-left:4px solid var(--alert);
    border-radius:8px;
    padding:0.6rem 0.9rem;
    color:#8A2C33;
    font-size:0.92rem;
    margin:0.4rem 0 1.1rem 0;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"]{
    font-family:'Inter', sans-serif;
    font-weight:500;
    color:var(--muted);
}
button[data-baseweb="tab"][aria-selected="true"]{
    color:var(--accent-strong) !important;
    border-bottom-color:var(--accent) !important;
}

/* ---------- Dataframe / dividers ---------- */
hr{ border-color:var(--line) !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def section_header(icon: str, title: str, subtitle: str = ""):
    """Renders a titled section with the signature pulse-line divider.
    Built as one flush-left HTML string (no line breaks/indentation) so
    Streamlit's markdown parser can't mistake any of it for a code block."""
    subtitle_html = f'<div style="color:var(--muted); font-size:0.88rem; margin-bottom:0.3rem;">{subtitle}</div>' if subtitle else ""
    html = (
        f'<div class="section-header">'
        f'<div class="section-title">{icon} {title}</div>'
        f'{subtitle_html}'
        f'{PULSE_SVG}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

_card_counter = {"n": 0}


def info_card():
    """Use as: `with info_card(): st.subheader(...); st.plotly_chart(...)`.
    Returns a real st.container so content is genuinely nested inside the
    styled div — unlike the old markdown-open/markdown-close pattern,
    which left an empty white box on screen (see CSS comment above)."""
    _card_counter["n"] += 1
    return st.container(key=f"infocard_{_card_counter['n']}")


# ---------- Header banner ----------
header_html = (
    '<div class="dashboard-header">'
    '<div class="app-title">🩺 Diabetes Analytic System</div>'
    '<div class="app-subtitle">Smart data visualization for patient health monitoring</div>'
    f'{PULSE_SVG}'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

df = pd.read_csv("Dataset of Diabetes .csv")

with st.sidebar:
    st.markdown('<div class="sidebar-caption">Navigator</div>', unsafe_allow_html=True)
    st.markdown("## 📁 Control Deck")
    from streamlit_option_menu import option_menu
    opt = option_menu(
        None,
        ["📑 Preface", "🤖 Upload & Preview", "💡Cleaning & Processing", "📈 Graphs and charts", "🔎 Insights", "✏️ About"],

        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#5FD8C6", "font-size": "16px"},
            "nav-link": {
                "font-family": "Inter, sans-serif",
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "10px",
                "color": "#E6EEF1",
                "background-color": "#182432",
                "--hover-color": "rgba(95,216,198,0.16)",
            },
            "nav-link-selected": {"background-color": "#5FD8C6", "color": "#0C141C", "font-weight": "600"},
        },
    )

    components.html(
        """
        <script>
        function fixOptionMenuIframeBg() {
            const iframes = window.parent.document.querySelectorAll('section[data-testid="stSidebar"] iframe');
            iframes.forEach(function(f) {
                f.style.backgroundColor = 'transparent';
                try {
                    const doc = f.contentDocument || f.contentWindow.document;
                    if (doc && doc.body) {
                        doc.documentElement.style.backgroundColor = '#111A24';
                        doc.body.style.backgroundColor = '#111A24';
                    }
                } catch (e) {}
            });
        }
        [100, 300, 700, 1200, 2000].forEach(function(ms) {
            setTimeout(fixOptionMenuIframeBg, ms);
        });
        </script>
        """,
        height=0,
        width=0,
    )

if opt == "📑 Preface":
    section_header("📑", "Overview", "Key vitals across the full patient dataset")

    total_patients = len(df)
    avg_age = df["AGE"].mean() if "AGE" in df.columns else 0
    avg_bmi = df["BMI"].mean() if "BMI" in df.columns else 0
    avg_hba1c = df["HbA1c"].mean() if "HbA1c" in df.columns else 0
    avg_chol = df["Chol"].mean() if "Chol" in df.columns else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Total Patients", f"{total_patients}")
    col2.metric("🎂 Avg Age", f"{avg_age:.1f}")
    col3.metric("⚖️ Avg BMI", f"{avg_bmi:.1f}")
    col4.metric("🩸 Avg HbA1c", f"{avg_hba1c:.2f}")
    col5.metric("🧪 Avg Cholesterol", f"{avg_chol:.2f}")

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
    section_header("👥", "Patients with Diabetes by Age")

    import seaborn as sns
    import matplotlib.pyplot as plt

    diabetes_df = df[df["CLASS"] == "Y"]
    age_bins = [20, 30, 40, 50, 60, 70, 80]
    age_labels = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79"]
    diabetes_df["AgeGroup"] = pd.cut(diabetes_df["AGE"], bins=age_bins, labels=age_labels, right=False)

    with info_card():
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        plt.xticks(rotation=45)
        sns.histplot(df[df['CLASS'] == 'Y']['AGE'], bins=[20, 30, 40, 50, 60, 70, 80], color='#1E7F7A')
        plt.title("Number of Diabetic Patients by Age", fontfamily="sans-serif", color="#16333B")
        st.pyplot(fig)

elif opt == "🤖 Upload & Preview":
    section_header("🤖", "Upload & Preview", "Load a dataset and inspect its quality before analysis")

    t1, t2, t3 = st.tabs(["Data set", "Data info", "Data summary"])
    with t1:
        uploaded_file = st.file_uploader("📂 Upload your Diabetes Dataset (.xlsx or .csv)", type=["xlsx", "csv"])

        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
            st.markdown('<div class="insight-note">✅ Dataset uploaded successfully!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-note">⚠️ Please upload your dataset to begin analysis.</div>', unsafe_allow_html=True)

        st.markdown("#### 📌 Patients records")
        st.dataframe(df, use_container_width=True)
    with t2:
        st.markdown("#### 📜 Data Quality Check")
        dq1, dq2, dq3 = st.columns(3)
        dq1.metric("Missing Values", int(df.isna().sum().sum()))
        dq2.metric("Duplicate Rows", int(df.duplicated().sum()))
        dq3.metric("Columns", df.shape[1])

        st.dataframe(
            df.isna().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}),
            use_container_width=True,
        )
    with t3:
        with info_card():
            st.markdown("#### 📝 Data summary")
            st.write(f"**Total Records:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
            st.write("**Classes:** N = Normal, P = Prediabetes, Y = Diabetes")
            st.write(f"**Age Range:** {df['AGE'].min()} – {df['AGE'].max()} years")
            st.write(f"**Average BMI:** {round(df['BMI'].mean(), 2)}")
            st.write(f"**Average HbA1c:** {round(df['HbA1c'].mean(), 2)}")
            st.write(f"**Average HDL:** {round(df['HDL'].mean(), 2)}")
            st.write(f"**Average Chol:** {round(df['Chol'].mean(), 2)}")

elif opt == "📈 Graphs and charts":
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    section_header("📈", "Graphs and Charts", "Filter patients on the left, then explore each view")

    t1, t2, t3, t4, t5, t6, t7 = st.tabs([
        "Pie chart & Bar graph", "Histogram", "Boxplot & Scatter", "Heatmap",
        "Violin Plot", "3D View", "Trend & Area",
    ])
    st.sidebar.markdown('<div class="sidebar-caption" style="margin-top:1rem;">Filter Patients</div>', unsafe_allow_html=True)
    st.sidebar.header("🔎 Filter Patients")

    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].replace({"f": "F"})

    gender_options = sorted(df["Gender"].dropna().unique().tolist()) if "Gender" in df.columns else []
    class_options = sorted(df["CLASS"].dropna().unique().tolist()) if "CLASS" in df.columns else []

    selected_gender = st.sidebar.multiselect("Select Gender", gender_options, default=gender_options)
    selected_class = st.sidebar.multiselect("Select Class", class_options, default=class_options)

    min_age = int(df["AGE"].min()) if "AGE" in df.columns else 0
    max_age = int(df["AGE"].max()) if "AGE" in df.columns else 100
    age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

    df = df.copy()
    if "Gender" in df.columns:
        df = df[df["Gender"].isin(selected_gender)]
    if "CLASS" in df.columns:
        df = df[df["CLASS"].isin(selected_class)]
    if "AGE" in df.columns:
        df = df[(df["AGE"] >= age_range[0]) & (df["AGE"] <= age_range[1])]
        class_map = {"N": "Normal", "P": "Prediabetes", "Y": "Diabetes"}

    if "CLASS" in df.columns:
        df["Class Label"] = df["CLASS"].map(class_map).fillna(df["CLASS"])
    else:
        df["Class Label"] = "Unknown"

    THEME_SEQ = ["#1E7F7A", "#5FD8C6", "#0F5C57", "#E8A33D", "#3D7EA6", "#D64550"]

    with t1:
        with info_card():
            st.subheader("Class Distribution")
            if "Class Label" in df.columns:
                class_counts = df["Class Label"].value_counts().reset_index()
                class_counts.columns = ["Class", "Count"]
                fig_class = px.pie(class_counts, names="Class", values="Count", hole=0.45, color="Class",
                                    color_discrete_sequence=THEME_SEQ)
                fig_class.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_class, use_container_width=True)

        with info_card():
            st.subheader("Gender Distribution")
            if "Gender" in df.columns:
                df = df[df["Gender"] != "f"]
                gender_counts = df["Gender"].value_counts().reset_index()
                gender_counts.columns = ["Gender", "Count"]
                fig_gender = px.bar(gender_counts, x="Gender", y="Count", color="Gender", text_auto=True,
                                     color_discrete_sequence=THEME_SEQ)
                fig_gender.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_gender, use_container_width=True)

    with t2:
        with info_card():
            st.subheader("Age Distribution")
            if "AGE" in df.columns and "Class Label" in df.columns:
                fig_age = px.histogram(df, x="AGE", nbins=20, color="Class Label", barmode="overlay",
                                        color_discrete_sequence=THEME_SEQ)
                fig_age.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_age, use_container_width=True)

        with info_card():
            st.subheader("BMI Distribution")
            if "BMI" in df.columns and "Class Label" in df.columns:
                fig_bmi = px.histogram(df, x="BMI", nbins=20, color="Class Label", barmode="overlay",
                                        color_discrete_sequence=THEME_SEQ)
                fig_bmi.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_bmi, use_container_width=True)

    with t3:
        with info_card():
            st.subheader("HbA1c by Class")
            if "HbA1c" in df.columns and "Class Label" in df.columns:
                fig_hba1c = px.box(df, x="Class Label", y="HbA1c", color="Class Label",
                                    color_discrete_sequence=THEME_SEQ)
                fig_hba1c.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_hba1c, use_container_width=True)

        with info_card():
            st.subheader("HbA1c vs BMI")
            if {"BMI", "HbA1c", "Class Label"}.issubset(df.columns):
                hover_cols = [col for col in ["Gender", "Chol", "TG", "LDL", "HDL"] if col in df.columns]
                fig_scatter = px.scatter(df, x="BMI", y="HbA1c", color="Class Label",
                                          size="AGE" if "AGE" in df.columns else None,
                                          hover_data=hover_cols, color_discrete_sequence=THEME_SEQ)
                fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_scatter, use_container_width=True)

    with t4:
        with info_card():
            st.subheader("Lipid Profile Comparison")
            lipid_cols = ["Chol", "TG", "HDL", "LDL", "VLDL"]
            available_lipid_cols = [col for col in lipid_cols if col in df.columns]

            if available_lipid_cols and "Class Label" in df.columns:
                lipid_means = df.groupby("Class Label")[available_lipid_cols].mean().reset_index()
                lipid_long = lipid_means.melt(id_vars="Class Label", var_name="Marker", value_name="Average Value")
                fig_lipid = px.bar(lipid_long, x="Marker", y="Average Value", color="Class Label", barmode="group",
                                    color_discrete_sequence=THEME_SEQ)
                fig_lipid.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_lipid, use_container_width=True)

        numeric_cols = ["AGE", "Urea", "Cr", "HbA1c", "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"]
        heatmap_cols = [col for col in numeric_cols if col in df.columns]

        if len(heatmap_cols) > 1:
            with info_card():
                st.subheader("Correlation Heatmap")
                corr = df[heatmap_cols].corr()
                theme_cmap = LinearSegmentedColormap.from_list(
                    "theme_diverging", ["#D64550", "#FFFFFF", "#0F5C57"]
                )
                fig, ax = plt.subplots(figsize=(10, 6))
                fig.patch.set_facecolor("#FFFFFF")
                sns.heatmap(corr, annot=True, cmap=theme_cmap, fmt=".2f", ax=ax, linewidths=0.5, linecolor="#FFFFFF")
                st.pyplot(fig)

    with t5:
        with info_card():
            st.subheader("HbA1c Distribution by Class (Violin)")
            if "HbA1c" in df.columns and "Class Label" in df.columns:
                fig_violin_hba1c = px.violin(df, x="Class Label", y="HbA1c", color="Class Label",
                                              box=True, points="outliers", color_discrete_sequence=THEME_SEQ)
                fig_violin_hba1c.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter", showlegend=False)
                st.plotly_chart(fig_violin_hba1c, use_container_width=True)

        with info_card():
            st.subheader("BMI Distribution by Class (Violin)")
            if "BMI" in df.columns and "Class Label" in df.columns:
                fig_violin_bmi = px.violin(df, x="Class Label", y="BMI", color="Class Label",
                                            box=True, points="outliers", color_discrete_sequence=THEME_SEQ)
                fig_violin_bmi.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter", showlegend=False)
                st.plotly_chart(fig_violin_bmi, use_container_width=True)

    with t6:
        with info_card():
            st.subheader("3D View: BMI, HbA1c & Cholesterol")
            if {"BMI", "HbA1c", "Chol", "Class Label"}.issubset(df.columns):
                fig_3d = px.scatter_3d(
                    df, x="BMI", y="HbA1c", z="Chol", color="Class Label",
                    size="AGE" if "AGE" in df.columns else None,
                    color_discrete_sequence=THEME_SEQ, opacity=0.8,
                )
                fig_3d.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_family="Inter",
                    scene=dict(
                        xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#E1E8E8"),
                        yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#E1E8E8"),
                        zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#E1E8E8"),
                    ),
                    margin=dict(l=0, r=0, t=10, b=0),
                )
                st.plotly_chart(fig_3d, use_container_width=True)
                st.markdown(
                    '<div class="insight-note">Drag to rotate — point size reflects patient age.</div>',
                    unsafe_allow_html=True,
                )

    with t7:
        with info_card():
            st.subheader("Average Biomarkers by Age Group")
            if "AGE" in df.columns:
                trend_bins = [20, 30, 40, 50, 60, 70, 80]
                trend_labels = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79"]
                df_trend = df.copy()
                df_trend["AgeGroup"] = pd.cut(df_trend["AGE"], bins=trend_bins, labels=trend_labels, right=False)
                trend_cols = [c for c in ["HbA1c", "BMI", "Chol"] if c in df.columns]
                if trend_cols:
                    trend_data = df_trend.groupby("AgeGroup", observed=False)[trend_cols].mean().reset_index()
                    trend_long = trend_data.melt(id_vars="AgeGroup", var_name="Marker", value_name="Average Value")
                    fig_trend = px.line(trend_long, x="AgeGroup", y="Average Value", color="Marker", markers=True,
                                         color_discrete_sequence=THEME_SEQ)
                    fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                    st.plotly_chart(fig_trend, use_container_width=True)

        with info_card():
            st.subheader("Patient Volume by Age Group (Area)")
            if "AGE" in df.columns and "Class Label" in df.columns:
                vol_data = df_trend.groupby(["AgeGroup", "Class Label"], observed=False).size().reset_index(name="Count")
                fig_area = px.area(vol_data, x="AgeGroup", y="Count", color="Class Label",
                                    color_discrete_sequence=THEME_SEQ)
                fig_area.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter")
                st.plotly_chart(fig_area, use_container_width=True)

elif opt == "💡Cleaning & Processing":
    section_header("💡", "Cleaning & Processing", "Check data quality and remove duplicate records")

    t1, t2 = st.tabs(["Duplicates & records", "Statistical & class distribution"])
    with t1:
        with info_card():
            st.subheader("📍 Missing Values")
            st.write(df.isnull().sum())
            st.subheader("Duplicate Records")
            st.write(df.duplicated().sum())

        st.subheader("🪄 Cleaned Dataset")
        df = df.drop_duplicates()
        st.dataframe(df.head(20), use_container_width=True)

    with t2:
        with info_card():
            st.subheader("🔵 Summary Statistics")
            st.write(df.describe())

        st.subheader("🟣 Class Distribution")
        st.bar_chart(df['CLASS'].value_counts())

elif opt == "🔎 Insights":
    section_header("🔎", "Insights", "Key findings distilled from the dataset")

    with info_card():
        st.subheader("Class Distribution")
        class_counts = df['CLASS'].value_counts(normalize=True) * 100
        st.write(class_counts.round(2))
        st.markdown(
            f'<div class="insight-note">Most patients are {class_counts.idxmax()} ({class_counts.max():.2f}%).</div>',
            unsafe_allow_html=True,
        )

    with info_card():
        st.subheader("Age-Based Insights")
        avg_age = df.groupby("CLASS")["AGE"].mean()
        st.write(avg_age)
        st.markdown('<div class="insight-note">Diabetic patients tend to be older compared to non-diabetic.</div>', unsafe_allow_html=True)

    with info_card():
        st.subheader("Gender Insights")
        gender_class = df.groupby(["Gender", "CLASS"]).size().unstack(fill_value=0)
        st.write(gender_class)
        st.markdown('<div class="insight-note">Shows diabetes distribution across male and female patients.</div>', unsafe_allow_html=True)

    with info_card():
        st.subheader("Biochemical Parameter Insights")
        bio_means = df.groupby("CLASS")[["HbA1c", "BMI", "Chol", "LDL"]].mean()
        st.write(bio_means)
        st.markdown('<div class="insight-note">Diabetic patients have higher HbA1c, BMI, and LDL on average.</div>', unsafe_allow_html=True)

    with info_card():
        st.subheader("Correlation Insights")
        corr = df[["HbA1c", "BMI", "LDL", "Urea", "Cr"]].corr()
        st.write(corr)
        st.markdown('<div class="insight-note">HbA1c correlates positively with BMI and LDL.</div>', unsafe_allow_html=True)

    with info_card():
        st.subheader("Risk Factor Insights")
        high_risk = df[(df["HbA1c"] > 6.5) & (df["BMI"] > 30)]
        st.markdown(
            f'<div class="risk-note">⚠️ Patients at highest risk (HbA1c &gt; 6.5 and BMI &gt; 30): <b>{len(high_risk)}</b></div>',
            unsafe_allow_html=True,
        )

elif opt == "✏️ About":
    section_header("✏️", "About Project")

    about_html = (
        '<div class="info-card">'
        
        '<p>This project is a <b>Diabetes Data Analysis Dashboard</b> built using Python and Streamlit.</p>'
        '<h4>Purpose</h4>'
        '<p>The goal is to analyze patient health data and visualize patterns related to diabetes.</p>'
        '<h4>Dataset</h4>'
        '<p>The dataset includes patient details such as Age, Gender, HbA1c, BMI, Cholesterol, LDL, HDL, and Class '
        '(N = Non-diabetic, P = Prediabetic, Y = Diabetic).</p>'
        '<h4>Tools &amp; Libraries</h4>'
        '<p>Pandas for data handling · Streamlit for the interactive dashboard · Plotly, Seaborn, and Matplotlib for visualizations.</p>'
        '<h4>Features</h4>'
        '<p>Upload and preview dataset · Data cleaning and processing · Graphs: heatmap, bar chart, pie chart, boxplot, histogram · Insights section with key findings.</p>'
        '<h4>Outcomes</h4>'
        '<p>Identify risk factors (high HbA1c, BMI, cholesterol) · Show age and gender trends · Provide correlations between health parameters.</p>'
        '</div>'
    )
    st.markdown(about_html, unsafe_allow_html=True)