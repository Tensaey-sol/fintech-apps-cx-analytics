# 📱 Customer Experience Analytics for Fintech Apps

This repository contains the setup and development for **Customer Experience Analytics for Fintech Apps**, a real-world data engineering challenge focused on analyzing user satisfaction for mobile banking apps in Ethiopia.

The project involves **Web scraping & text preprocessing for app reviews**, **Sentiment and thematic NLP analysis**, **Oracle-based data storage**, and **Visualization and reporting** for three major banks:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

It simulates the role of a Data Analyst, delivering insights to help these banks improve their mobile apps.

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Tensaey-sol/fintech-apps-cx-analytics.git
cd fintech-apps-cx-analytics
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:**

  ```bash
  .venv\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
fintech-apps-cx-analytics/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions workflow
├── .gitignore                 # Ignore rules for Git
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── notebooks/                 # Jupyter Notebooks
│   └── README.md
├── tests/                     # Unit tests for scripts and functions
│   └── __init__.py
├── scripts/                   # Scripts for scraping, cleaning, analysis
│   ├── __init__.py
│   └── README.md
├── data/                      # Raw and processed datasets (ignored via .gitignore)
└── .venv/                     # Local virtual environment (ignored via .gitignore)
```

---

## 📈 Methodology

This project was developed through the following phases:

### Phase 1: Scraping Google Play Reviews

- Extracted 400+ recent user reviews for each bank app using `google-play-scraper`.
- Collected the following fields: **review text**, **rating**, **review date**, **bank name**, and **source**.
- Saved raw reviews in structured format for each bank.

### Phase 2: Cleaning and Preprocessing

- Removed duplicates and handled missing values.
- Normalized dates to `YYYY-MM-DD` format.
- Standardized column names: `review`, `rating`, `date`, `bank`, `source`.
- Exported cleaned datasets as separate CSV files in `/data`.

### Phase 3: Data Validation

- Verified total number of reviews collected (target: 1,200+).
- Assessed data completeness (goal: <5% missing data).
- Produced summary statistics and per-bank health checks.

### Phase 4: Sentiment Analysis

- Applied VADER sentiment analyzer to classify reviews as positive, negative, or neutral based on compound scores (thresholds: >0.05 for positive, <-0.05 for negative, else neutral).
- Achieved sentiment scoring for 100% of reviews (exceeding 90% KPI).
- Aggregated mean sentiment scores by bank and rating (1–5 stars) to identify satisfaction trends.
- Saved results to per-bank CSV files with columns: `review_id`, `review_text`, `sentiment_label`, `sentiment_score`.

### Phase 5: Thematic Analysis

- Preprocessed review text using spaCy for tokenization, stop-word removal, and lemmatization.
- Extracted top 5 keywords and n-grams per review using TF-IDF vectorization.
- Mapped keywords to 3–5 themes per bank (e.g., Account Access, Performance, User Experience, Support, Transactions, Feature Request) using a rule-based approach.
- Saved thematic results to per-bank CSV files with an additional `themes` column.
- Documented theme examples to highlight user pain points and satisfaction drivers.

### Future Phases

- **Database Storage:** Design and insert cleaned data into Oracle DB tables.
- **Insights & Recommendations:** Create dashboards and reports for stakeholder decision-making.

---

## ⚙️ GitHub Actions CI

A CI workflow is configured to run on every push:

- Uses **Python 3.13.1**
- Installs dependencies from `requirements.txt`
- Runs unit tests in `/tests`

See `.github/workflows/ci.yml` for setup and **Actions** tab of the GitHub repository for its status.

---

## 🛠 Tools & Technologies

- Python **3.13.1**
- `venv` for isolated Python environments
- **VSCode** (Recommended editor)
- Google Play Scraper Libraries (google-play-scraper, play-scraper, etc.)
- NLP (VADER, TextBlob, or custom models)
- Oracle SQL for database design
- Matplotlib, Seaborn, Plotly for visualization
- Git & GitHub for version control
- GitHub Actions for automation
- Jupyter Notebooks for analysis & reporting

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♀️ Questions or Suggestions?

Feel free to open an issue or submit a pull request if you’d like to contribute or raise a question.
