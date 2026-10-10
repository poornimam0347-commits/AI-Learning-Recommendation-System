import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_courses(file_path="courses.csv"):
	courses = pd.read_csv(file_path)
	courses = courses.fillna("")

	courses["content"] = (
		courses["category"].astype(str) + " "
		+ courses["description"].astype(str) + " "
		+ courses["skills"].astype(str)
	)
	return courses


def recommend_courses(user_interests, courses, top_n=5):
	if not user_interests or not user_interests.strip():
		return pd.DataFrame()

	documents = [user_interests] + courses["content"].tolist()
	vectorizer = TfidfVectorizer(stop_words="english")
	tfidf_matrix = vectorizer.fit_transform(documents)

	similarity_scores = cosine_similarity(
		tfidf_matrix[0:1], tfidf_matrix[1:]
	).flatten()

	results = courses.copy()
	results["similarity_score"] = similarity_scores
	results = results[results["similarity_score"] > 0]
	results = results.sort_values(by="similarity_score", ascending=False)

	return results.head(top_n).reset_index(drop=True)
