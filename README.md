# =========================
# 📄 README.md
# =========================

# UNIVERSITY-ETL

An end-to-end ETL (Extract, Transform, Load) project that fetches data from a public university domain API, processes and enriches it, stores it in Google BigQuery, and visualizes key insights using Looker Studio.

---

## 📌 Project Structure
```
.
├── README.md                   # Project overview and setup instructions
├── extract.py                  # Script to fetch data from API
├── transform.py                # Script for cleaning and transforming data
├── load.py                     # Script to load data into Google BigQuery
├── etl-deployment.py           # Script to Registering and scheduling your ETL workflow (flow) automatically
├── etl-main.py                 # Script to Identify the flow for automatically
├── dashboard_link.txt          # URL to the Looker Studio dashboard
├── presentation_slides.txt     # Final presentation slides
└── requirements.txt            # Required Python packages
```

## 🔧 Setup Instructions
1. **Clone the repository**
```bash
git clone https://github.com/AldhiNF/UNIVERSITY-ETL.git
cd UNIVERSITY-ETL
```

2. **Create virtual environment and install dependencies**
```bash
conda create -n university-etl python=3.10 -y
conda activate university-etl
pip install -r requirements.txt
```

3. **Prepare Google Cloud Credentials**
- Create a service account in Google Cloud.
- Download the `gcp_key.json` file and place it in `config/` directory.

4. **Run ETL Pipeline Manually**
```bash
python etl-deployment.py
```
Or trigger via **Prefect Cloud** if deployed.

---

## 📈 Dashboard
The interactive dashboard is built with Looker Studio:

**🔗 [View Dashboard](https://lookerstudio.google.com/reporting/322e7931-d2f6-4a82-b80e-fc4352682db2)**

Contains:
- Top 10 Countries by University Count
- University Distribution by Country
- Top-Level Domain Usage
- Domain Count Statistics
- Searchable University Table

---

## 🧠 Key Learnings
- Practical usage of ETL pattern
- Using public APIs
- Data cleaning and enrichment in Python
- Google BigQuery as cloud data warehouse
- Automated scheduling with Prefect
- Visualization storytelling in Looker Studio

---

## 🚀 Optional Enhancements
- Integrate scheduling via Prefect Cloud (monthly updates)
- Add additional data enrichment (ranking, region, etc.)
- Include ML classification for research-type universities