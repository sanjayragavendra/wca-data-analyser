<!-- ================= HEADER ================= -->

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,100:2c5364&height=250&section=header&text=WCA%20Data%20Analysis%20Suite&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=00F5FF&size=22&center=true&vCenter=true&width=900&lines=Advanced+WCA+Analytics+Engine;Competitor+Performance+Tracking;Podium+Prediction+System;Machine+Learning+Driven+Insights;Interactive+Visualization+Suite"/>
</p>

---

# WCA Data Analysis and Prediction Suite

A powerful menu-driven analytics engine for World Cube Association datasets, designed to deliver deep insights, predictive modeling, and advanced visualizations.

---

## System Overview

This system processes official WCA datasets and transforms them into:

- Competitor-level performance intelligence  
- Event-based statistical analysis  
- Country-level dominance insights  
- Predictive modeling (ML-powered)  
- Visual analytics dashboards  

---

## Architecture

```
WCADataLoader
   ├── Loads TSV datasets
   ├── Cleans + preprocesses data
   └── Converts time formats

CompetitorAnalyzer
   ├── Performance tracking
   ├── Improvement analysis
   ├── Podium probability prediction
   └── Visualization engine

WCAMenu
   ├── CLI interface
   ├── Navigation system
   └── Feature access layer
```

---

## Features

### Competitor Intelligence Engine
- Full competitor breakdown via WCA ID
- Event-wise performance tracking
- Improvement rate calculation using regression
- Future performance prediction
- Podium probability modeling

---

### Visualization System
- Dual-panel performance graphs (best vs average)
- Trend lines with regression analysis
- Numbered data points for clarity
- Pie charts for podium analysis
- Multi-panel dashboards

---

### Predictive Analytics
- Linear regression forecasting
- World record progression modeling
- Confidence interval estimation
- Trend-based probability adjustments

---

### Machine Learning Integration
- K-Means clustering for competitor segmentation
- PCA dimensionality reduction
- Performance grouping analysis

---

### Global & Country Insights
- Participation trends over time
- Country-wise performance dominance
- Event distribution analytics
- Time distribution modeling

---

## Tech Stack

- pandas — data processing  
- numpy — numerical computation  
- matplotlib — visualization  
- seaborn — statistical plots  
- scikit-learn — machine learning  
- scipy — statistical modeling  

---

## Data Requirements

Place WCA export files in the root directory:

```
WCA_export_persons.tsv
WCA_export_results.tsv
WCA_export_ranks_average.tsv
WCA_export_events.tsv
WCA_export_countries.tsv
WCA_export_continents.tsv
WCA_export_round_types.tsv
WCA_export_scrambles.tsv
WCA_export_result_attempts.tsv
WCA_export_competitions.tsv
WCA_export_championships.tsv
WCA_export_formats.tsv

```

---

## Installation

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```

---

## Execution

```bash
python main.py
```

---

## Menu System

```
1. Analyze Competitor
2. Global Statistics & Trends
3. Country Performance Analysis
4. Event Analysis
5. Predictive Models
6. Exit
```

---

## Core Algorithms

### Improvement Rate
- Linear regression on time vs year  
- Negative slope = improvement  
- R² used for confidence measurement  

---

### Podium Prediction
- Historical podium ratio  
- Recency-weighted scoring  
- Trend-based probability adjustment  

---

### Forecasting
- Linear regression on world records  
- Confidence interval estimation  
- Future performance projection  

---

## Visual Output

- Multi-window matplotlib dashboards  
- Annotated data points  
- Trend lines and regression overlays  
- Statistical distribution graphs  

---

## Performance Highlights

- Handles large WCA datasets efficiently  
- Modular architecture for scalability  
- Robust error handling  
- Clean CLI-driven interaction  

---

## Future Enhancements

- GUI interface (PyQt / Web dashboard)  
- Real-time WCA API integration  
- Neural network-based predictions  
- User account tracking system  

---

## License

MIT License

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,100:0f2027&height=120&section=footer"/>
</p>
