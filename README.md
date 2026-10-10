# 🎯 LearnMatch AI
### AI-Powered Personalized Learning Recommendation System

LearnMatch AI is a content-based recommendation system that suggests learning resources according to a user's interests.

This project was developed as Project 3 for the Artificial Intelligence track at DecodeLabs.

## ✨ Features

- Personalized learning recommendations
- Multiple interest selection
- Custom interest input
- TF-IDF text vectorization
- Cosine similarity scoring
- Course category filters
- Difficulty-level filters
- Adjustable number of recommendations
- Similarity score visualization
- CSV download of recommendations

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF
- Cosine similarity

## 🧠 How It Works

1. The user selects or enters learning interests.
2. The system loads learning resources from `courses.csv`.
3. Course categories, descriptions, and skills are combined.
4. TF-IDF converts the text into numerical vectors.
5. Cosine similarity compares the user's interests with each learning resource.
6. Resources are ranked by similarity score.
7. The application displays the recommendations.

## 📁 Project Structure

```text
AI_Learning_Recommendation_System/
├── app.py
├── recommender.py
├── courses.csv
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd AI_Learning_Recommendation_System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 📊 Recommendation Method

This application uses content-based filtering with TF-IDF and cosine similarity.

Similarity scores represent textual similarity between user interests and learning resources. They are not probabilities of user satisfaction.

## 🎯 Project Objective

To demonstrate preference matching, text similarity, recommendation ranking, and interactive presentation of personalized learning resources.
