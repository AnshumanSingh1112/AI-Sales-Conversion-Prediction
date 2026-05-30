# 📈 AI-Based Sales Conversion Probability Prediction System

## Overview

This project predicts the probability of converting a sales lead into a customer using Machine Learning.

The system analyzes lead engagement metrics such as website activity, email interactions, downloads, response time, and social media engagement to estimate conversion probability.

A Random Forest Classifier was trained on 100,000 lead records and deployed using Streamlit for real-time predictions.

---

## Project Demo

### Dashboard

(Add Screenshot Here)

Example:

![Dashboard](images/dashboard.png)

---

## Features

✅ Lead Conversion Prediction

✅ Random Forest Machine Learning Model

✅ Interactive Streamlit Dashboard

✅ Real-Time Probability Prediction

✅ 100,000 Training Records

✅ User-Friendly Interface

---

## Dataset Information

Dataset Size: 100,000 Records

Target Variable:

* 0 = Not Converted
* 1 = Converted

Input Features:

* Age
* Time Spent on Website
* Pages Viewed
* Email Sent
* Form Submissions
* Downloads
* CTR Product Page
* Response Time
* Follow Up Emails
* Social Media Engagement

---

## Machine Learning Model

Algorithm Used:

* Random Forest Classifier

Performance:

* Accuracy: 99%
* Precision: 1.00
* Recall: 0.54
* F1 Score: 0.71

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* Joblib
* Streamlit

---

## Project Structure

Sales-Conversion-Prediction/

│

├── app.py

├── model.py

├── eda.py

├── rf_model.pkl

├── customer_conversion_training_dataset.csv

├── requirements.txt

├── README.md

│

└── images/

```
 └── dashboard.png
```

---

## Installation

Clone Repository

git clone YOUR_GITHUB_REPOSITORY_LINK

Move into Project Folder

cd Sales-Conversion-Prediction

Install Dependencies

pip install -r requirements.txt

Run Application

streamlit run app.py

---

## Future Improvements

* Advanced Feature Engineering
* Model Comparison (XGBoost, LightGBM)
* Cloud Deployment
* Lead Ranking System
* CRM Integration

---

## Author

Anshuman Singh

B.Tech CSE

Machine Learning Project
