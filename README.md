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
- **Dashboard 1**: <img width="1230" alt="Screenshot 2024-12-05 at 5 40 52 PM" src="https://github.com/user-attachments/assets/faff5bc0-f6e9-4f2f-9f7c-3ab85d2d7c0a">
.
- **Dashboard 2**: <img width="1230" alt="Screenshot 2024-12-05 at 5 40 22 PM" src="https://github.com/user-attachments/assets/749bc691-a20c-45fd-ac7b-42f9b0425d4d">


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
# Results
- **Random Forest Model**: Achieved high accuracy due to its ability to handle large datasets and imbalanced classes effectively.
- **Deep Learning Model**: Demonstrated robust fraud detection in complex patterns.
- **K-Means Clustering Model**: Provided valuable insights into anomalies, despite being unsupervised.

# Conclusion
This project successfully demonstrates how machine learning, visualization tools, and database management can enhance fraud detection in financial transactions. The combination of predictive models, actionable insights, and efficient data handling aims to reduce the financial losses caused by credit card fraud.

# Contributors
- **Manahil Rashid** – [manahilr701@gmail.com](mailto:manahilr701@gmail.com)
- **Andrew Sanchez** – [agsanchez2022@gmail.com](mailto:agsanchez2022@gmail.com)
- **David Bui** – [davidnbui@yahoo.com](mailto:davidnbui@yahoo.com)
- **Jeff Hammans** – [hef1125@hotmail.com](mailto:hef1125@hotmail.com)
- **Deelan Patel** – [deelanp93@gmail.com](mailto:deelanp93@gmail.com)

# Files
### Code:
- `RandomForestClassifier.ipynb`
- `load_fraud_busters_mongodb.ipynb`

### Configuration:
- `config_template.json`

### Visualizations:
- Dashboards (see screenshots above)
