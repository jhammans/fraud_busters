import psycopg2
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_casualties_data():
    # Establish connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname='your_database',
        user='weather_wizards',
        password='',
        host='localhost',
        port='5432'
    )
    
    # Define your SQL query
    query = """
        SELECT
            year,
            event_type,
            SUM(casualties) AS total_casualties,
            COUNT(*) AS number_of_events
        FROM
            your_table_name  
        GROUP BY
            year, event_type
        ORDER BY
            year;
    """
    
    # Execute the query and fetch the data
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

@app.route('/api/casualties', methods=['GET'])
def get_casualties():
    data = fetch_casualties_data()
    return jsonify(data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
