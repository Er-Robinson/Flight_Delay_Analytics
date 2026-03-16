# ✈️ Flight Delay Analytics — Real‑Time Dashboard & ML Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-green)
![ML](https://img.shields.io/badge/Machine%20Learning-Real%20Time-red)
![Plotly](https://img.shields.io/badge/Visualisation-Plotly-orange)

---

##  Project Summary

**Flight Delay Analytics** is an industry‑grade, real‑time flight operations analytics system built in Python. It collects live flight data, cleans and preprocesses it, detects anomalies, identifies patterns and trends, and uses machine learning models to predict delays — all while providing rich, interactive visualisations.

This solution is suitable for:

* Airline operations analytics
* Real-time monitoring dashboards
* Data-driven decision-making
* Executive dashboards and reporting

---

##  Key Features

✔️ Real-time flight data ingestion and preprocessing
✔️ Machine learning models (Random Forest, Gradient Boosting, XGBoost)
✔️ Anomaly detection on flight behaviour
✔️ Exploration of traffic patterns and busiest airports
✔️ Interactive data visualisations with Map, Heatmap & Animated movement
✔️ Automatic saving of high-quality images for documentation
✔️ Exportable charts that can be reused for reports or presentations

---

##  Project Structure

```
Flight_Delay_Analytics/
├── dashboard/
│   ├── app.py
│   ├── images/             ← Auto-generated chart captures
├── data/                   ← Sample or static data (optional)
├── notebooks/              ← Exploration & prototype notebooks
├── plots/                  ← Saved plot outputs
├── pipeline/               ← Real-time processing scripts
├── src/
│   ├── ingest_live_data.py
│   ├── preprocess.py
│   ├── anomaly_detection.py
│   ├── pattern_discovery.py
│   ├── graph_analysis.py
│   ├── delay_prediction.py
│   ├── logger.py
├── README.md               ← *You are here*
├── requirements.txt
```

---

##  Live Dashboard Visualisations

### 🔹 Preprocessed Flight Table

This shows the first few rows after preprocessing, cleaned and ready for modelling.

![Preprocessed Data](dashboard/images/preprocessed_data.png)

---

### 🔹 Top Airlines in Air

Flight counts by airline, colour coded by intensity.

![Top Airlines](dashboard/images/top_airlines.png)

---

### 🔹 Live Flight Map

Positions are plotted with altitude and velocity.

![Live Flight Map](dashboard/images/live_map.png)

---

### 🔹 Flight Traffic Heatmap

Shows crowd intensity across the globe.

![Traffic Heatmap](dashboard/images/traffic_heatmap.png)

---

### 🔹 Animated Aircraft Movement

Shows positional evolution across time.

![Aircraft Animation](dashboard/images/aircraft_animation.png)

---

##  ML & Patterns Insights

###  Busiest Airports

Flights aggregated by origin airport.

![Busiest Airports](dashboard/images/busiest_airports.png)

---

###  Delay Risk Distribution

Shows proportion of flights at risk of delay.

![Delay Risk Distribution](dashboard/images/delay_distribution.png)

---

##  How It Works (End-to-End Pipeline)

1. **Fetch Live Flight Data**
   Pulls real-time inputs from live ADS-B feeds.

2. **Preprocess Data**
   Clean, transform and engineer features for use in ML.

3. **Detect Anomalies**
   Finds unusual flight behaviour such as altitude spikes or irregular motion.

4. **Pattern Discovery**
   Uses graph-based and statistical methods to find busiest routes and airports.

5. **Machine Learning Models**
   Train and evaluate predictive models for delay forecasting.

6. **Interactive Dashboard**
   Generate actionable insights using Streamlit.

---

##  Machine Learning Results

| Model             | RMSE (mins) | MAE (mins) | R² Score |
| ----------------- | ----------- | ---------- | -------- |
| Random Forest     | 21.54       | 14.68      | 0.937    |
| Gradient Boosting | 22.33       | 16.10      | 0.933    |
| XGBoost           | 21.03       | 14.01      | 0.940    |

> Models achieve strong performance on predicting flight delays in near-real time.

---

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Er-Robinson/Flight_Delay_Analytics.git
cd Flight_Delay_Analytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install kaleido streamlit plotly matplotlib pandas
```

> *Note: Kaleido is required to export high-quality Plotly images.*

---

## 🏃‍♂️ Running the Dashboard

To launch the interactive dashboard:

```bash
streamlit run dashboard/app.py
```

Open your browser at:

```
http://localhost:8501
```

---

##  How Images Are Generated

To support README visuals and documentation, `app.py` includes automatic image export functions:

✔️ Saves plots as PNGs to `dashboard/images/`
✔️ Each key visualization is stored with descriptive filenames
✔️ Images are aligned for easy inclusion in reports

---

##  Usage Scenarios

This project can be used for:

* **Business Intelligence Dashboards**
* **Operations Monitoring for Airlines**
* **Executive Reporting for Airport Authority**
* **Academic Research & Case Studies**
* **Machine Learning Pipelines for Decision-Making**

---

##  Future Enhancements

🔹 Add weather and meteorological integration
🔹 Add multi-hour delay forecasting
🔹 Deploy as cloud API for real-time monitoring
🔹 Add user authentication and role-based views
🔹 Produce exportable PDF reports

---

##  Methodology & Concepts

This project applies industry-recommended techniques from **Charu C. Aggarwal’s *Data Mining: The Textbook*** including:

✔ Feature engineering
✔ Anomaly detection
✔ Exploratory visual patterns
✔ Model selection with filter, wrapper, and embedded methods
✔ Real-time data processing architectures

These principles ensure robust, scalable analytics suitable for production-level datasets.

---

##  About the Author

**Robinson** — M.Tech in Data Science
Deep expertise in real-time analytics, ML modelling, and business impact insights.
