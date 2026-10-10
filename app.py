import streamlit as st
import pandas as pd
from recommender import load_courses, recommend_courses

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
	page_title="LearnMatch AI",
	page_icon="🎯",
	layout="wide",
	initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
	font-family: 'Inter', sans-serif;
}

.stApp {
	background: linear-gradient(135deg, #0b1020 0%, #111827 55%, #172554 100%);
	color: #f8fafc;
}

.block-container {
	padding-top: 2rem;
	padding-bottom: 3rem;
	max-width: 1200px;
}

.hero {
	padding: 35px;
	border: 1px solid rgba(148, 163, 184, 0.2);
	border-radius: 24px;
	background: linear-gradient(120deg, rgba(30,41,59,.95), rgba(30,58,138,.65));
	margin-bottom: 25px;
}

.eyebrow {
	color: #93c5fd;
	font-size: 13px;
	font-weight: 700;
	letter-spacing: 2px;
	text-transform: uppercase;
}

.hero h1 {
	color: #ffffff;
	font-size: clamp(32px, 5vw, 52px);
	font-weight: 800;
	margin: 12px 0;
}

.hero p {
	color: #cbd5e1;
	font-size: 16px;
	line-height: 1.8;
}

.section-title {
	color: #f8fafc;
	font-size: 24px;
	font-weight: 750;
	margin: 28px 0 15px 0;
}

.metric-card {
	padding: 20px;
	border: 1px solid rgba(148,163,184,.2);
	border-radius: 18px;
	background: rgba(30,41,59,.7);
	min-height: 110px;
}

.metric-label {
	color: #94a3b8;
	font-size: 13px;
}

.metric-value {
	color: #ffffff;
	font-size: 27px;
	font-weight: 800;
	margin-top: 8px;
}

.course-card {
	padding: 22px;
	margin: 12px 0;
	border: 1px solid rgba(148,163,184,.2);
	border-radius: 18px;
	background: rgba(30,41,59,.72);
}

.course-card h3 {
	color: #ffffff;
	font-size: 20px;
	margin: 8px 0;
}

.course-card p {
	color: #cbd5e1;
	line-height: 1.6;
}

.badge {
	display: inline-block;
	padding: 5px 10px;
	margin: 3px 5px 3px 0;
	border-radius: 20px;
	background: rgba(59,130,246,.15);
	border: 1px solid rgba(96,165,250,.35);
	color: #bfdbfe;
	font-size: 12px;
}

.score {
	color: #6ee7b7;
	font-size: 24px;
	font-weight: 800;
}

div.stButton > button {
	border-radius: 10px;
	font-weight: 700;
	min-height: 45px;
}

[data-testid="stSidebar"] {
	background: #0f172a;
	border-right: 1px solid rgba(148,163,184,.15);
}

[data-testid="stSidebar"] * {
	color: #e2e8f0;
}

footer {
	visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------
@st.cache_data
def get_courses():
	return load_courses("courses.csv")


try:
	courses = get_courses()
except Exception as error:
	st.error(f"Could not load the learning resources: {error}")
	st.stop()


# ---------------- SIDEBAR ----------------
with st.sidebar:
	st.markdown("## 🎯 LearnMatch AI")
	st.caption("PERSONALIZED LEARNING")

	st.markdown("---")
	st.markdown("### ⚙️ Preferences")

	categories = sorted(courses["category"].unique().tolist())

	selected_categories = st.multiselect(
		"Preferred categories",
		categories,
		help="Choose the areas you want to explore."
	)

	selected_level = st.selectbox(
		"Difficulty level",
		["All Levels", "Beginner", "Intermediate", "Advanced"]
	)

	number_of_recommendations = st.slider(
		"Number of recommendations",
		min_value=3,
		max_value=10,
		value=5
	)

	st.markdown("---")
	st.caption("Built with Python, Streamlit & Scikit-learn")


# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
	<div class="eyebrow">YOUR PERSONAL LEARNING COMPANION</div>
	<h1>Find what you should<br>learn next. ✨</h1>
	<p>
		Discover learning resources tailored to your interests.
		Our content-based recommendation engine compares your
		preferences with course descriptions and skills to find
		relevant learning opportunities.
	</p>
</div>
""", unsafe_allow_html=True)


# ---------------- USER INPUT ----------------
st.markdown(
	'<div class="section-title">01 / Tell us what interests you</div>',
	unsafe_allow_html=True
)

interest_options = [
	"Python",
	"Java",
	"Artificial Intelligence",
	"Machine Learning",
	"Deep Learning",
	"Data Science",
	"Data Analysis",
	"Web Development",
	"Cybersecurity",
	"Cloud Computing",
	"Databases",
	"Computer Networks",
	"Generative AI",
	"Natural Language Processing",
	"UI UX Design",
	"Mobile App Development",
	"Software Testing",
	"Statistics",
]

selected_interests = st.multiselect(
	"Choose your interests",
	interest_options,
	placeholder="Select one or more interests...",
)

custom_interests = st.text_input(
	"Or add your own interests",
	placeholder="e.g. neural networks, pandas, ethical hacking"
)

user_interests = ", ".join(selected_interests)

if custom_interests.strip():
	user_interests = (
		user_interests + ", " + custom_interests.strip()
	).strip(", ")


# ---------------- RECOMMENDATION ACTION ----------------
col_button, col_info = st.columns([1, 2])

with col_button:
	generate = st.button(
		"✨ Find My Recommendations",
		type="primary",
		use_container_width=True
	)

with col_info:
	st.caption(
		"Your recommendations are calculated from the interests you select."
	)


# ---------------- RESULTS ----------------
if generate:
	if not user_interests.strip():
		st.warning("Please select or enter at least one interest.")
	else:
		recommendations = recommend_courses(
			user_interests,
			courses,
			top_n=len(courses)
		)

		if selected_categories:
			recommendations = recommendations[
				recommendations["category"].isin(selected_categories)
			]

		if selected_level != "All Levels":
			recommendations = recommendations[
				recommendations["level"] == selected_level
			]

		recommendations = recommendations.head(
			number_of_recommendations
		).reset_index(drop=True)

		st.session_state["recommendations"] = recommendations
		st.session_state["searched_interests"] = user_interests


if "recommendations" in st.session_state:
	recommendations = st.session_state["recommendations"]
	searched_interests = st.session_state["searched_interests"]

	st.markdown(
		'<div class="section-title">02 / Your personalized results</div>',
		unsafe_allow_html=True
	)

	metric1, metric2, metric3 = st.columns(3)

	with metric1:
		st.markdown(f"""
		<div class="metric-card">
			<div class="metric-label">MATCHING RESOURCES</div>
			<div class="metric-value">{len(recommendations)}</div>
		</div>
		""", unsafe_allow_html=True)

	with metric2:
		st.markdown(f"""
		<div class="metric-card">
			<div class="metric-label">INTERESTS ENTERED</div>
			<div class="metric-value">{len([x for x in searched_interests.split(",") if x.strip()])}</div>
		</div>
		""", unsafe_allow_html=True)

	with metric3:
		if not recommendations.empty:
			average_score = recommendations["similarity_score"].mean() * 100
		else:
			average_score = 0

		st.markdown(f"""
		<div class="metric-card">
			<div class="metric-label">AVERAGE SIMILARITY</div>
			<div class="metric-value">{average_score:.1f}%</div>
		</div>
		""", unsafe_allow_html=True)

	if recommendations.empty:
		st.info(
			"No resources matched your preferences and filters. "
			"Try different interests or adjust the sidebar filters."
		)
	else:
		st.caption(
			"Results are ranked by text similarity. "
			"A higher score means greater textual similarity, "
			"not a guaranteed measure of learning quality."
		)

		for index, course in recommendations.iterrows():
			score = course["similarity_score"] * 100

			st.markdown(f"""
			<div class="course-card">
				<div class="badge">#{index + 1} RECOMMENDATION</div>
				<div class="badge">{course['category']}</div>
				<div class="badge">{course['level']}</div>
				<h3>{course['title']}</h3>
				<p>{course['description']}</p>
				<p><b>Skills:</b> {course['skills']}</p>
				<div class="score">{score:.1f}% similarity</div>
			</div>
			""", unsafe_allow_html=True)

			st.progress(
				min(max(float(course["similarity_score"]), 0.0), 1.0),
				text="Text similarity score"
			)

		csv_data = recommendations.to_csv(index=False).encode("utf-8")

		st.download_button(
			"⬇️ Download recommendations as CSV",
			data=csv_data,
			file_name="my_learning_recommendations.csv",
			mime="text/csv"
		)

else:
	st.markdown("""
	<div class="course-card">
		<h3>👋 Your next learning adventure starts here.</h3>
		<p>
			Select your interests above and click
			<b>Find My Recommendations</b> to discover
			learning resources ranked for your preferences.
		</p>
	</div>
	""", unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
	"LEARNMATCH AI · DecodeLabs Project 3 · "
	"Content-based recommendation using TF-IDF and cosine similarity"
)
