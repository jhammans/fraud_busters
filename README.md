# Credit Card Fraud Detection Using Machine Learning

## Project Overview
The aim of this project is to develop and evaluate machine learning models to detect fraudulent credit card transactions. By leveraging historical transaction data and advanced algorithms, we provide insights into fraud patterns and create a fraud detection system. This project addresses a critical issue for financial institutions by improving the identification and prevention of fraudulent activities.

---

## Objectives
- **Build and evaluate models** for detecting fraudulent transactions.
- **Analyze fraud patterns** to understand common fraudulent activities.
- **Create interactive visualizations** using Tableau for better fraud insights.

---

## Features

### Machine Learning Models:
- **Random Forest**: For high-performance classification with ensemble learning.
- **Deep Learning**: Utilizing neural networks for advanced pattern recognition.
- **K-Means Clustering**: For unsupervised detection of anomalies.

### Visualization:
- Interactive dashboards built with Tableau showcasing:
  - Transaction trends.
  - Geographic distribution of fraud.
  - Fraud intensity by category.
  - Demographic analysis.

### Database Configuration and ETL:
- A configuration template (`JSON format`) for connecting to **PostgreSQL** and **MongoDB** databases.
- A script for loading data into MongoDB, demonstrating how fraud data is stored and managed.

---

## Project Workflow

1. **Data Preprocessing**:
   - Handle missing values, normalize data, and encode categorical features.

2. **Model Development**:
   - Train and test three machine learning models: Random Forest, Deep Learning, and K-Means Clustering.

3. **Visualization**:
   - Use Tableau to create dashboards for insights into fraud patterns.

4. **Database Management**:
   - Leverage a JSON configuration file to ensure secure and seamless database connections.
   - Use an ETL pipeline to load fraud data into MongoDB for efficient storage and retrieval.

5. **Evaluation**:
   - Compare model performance using metrics like accuracy, precision, recall, and F1 score.

---

## Tools and Technologies
- **Python**: Data preprocessing, model training, and evaluation.
- **Tableau**: For data visualization.
- **MongoDB**: For NoSQL database management.
- **PostgreSQL**: For relational database management.
- **Libraries**: Scikit-learn, TensorFlow/Keras, Matplotlib, Pandas, NumPy.

---

## Data Source
The dataset used for this project was sourced from **Kaggle**, a platform providing open datasets for analysis and machine learning tasks.

---

## Visualization
Below are examples of the dashboards created using Tableau:
- **Dashboard 1**: Transaction Trends and Fraud Distribution.
- **Dashboard 2**: Fraud Analysis by Demographics and Professions.

---

## Database Configuration
To facilitate database management, a configuration file (`config_template.json`) was created, which includes placeholders for securely connecting to **PostgreSQL** and **MongoDB** clusters:

```json
{
    "postgres_connection": {
        "user": "",
        "password": "",
        "server": "",
        "port": ""
    },
    "mongodb_cluster": {
        "user": "",
        "password": "",
        "server": ""
    },
    "mongodb_local": {
        "user": "",
        "password": ""
    }
}
```
