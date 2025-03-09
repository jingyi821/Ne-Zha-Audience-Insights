from flask import Flask, render_template, jsonify
import pandas as pd
import os

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Read box office data
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'box_office.csv')

# Load data
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

print("File loaded successfully!")

# Convert data format for ECharts
def get_chart_data():
    regions = df['Region'].unique()
    dates = df['Date'].dt.strftime('%Y-%m-%d').unique().tolist()
    series_data = []

    for region in regions:
        region_data = df[df['Region'] == region]

        # Key part: Use .tolist() to convert nested arrays into plain lists!
        series_data.append({
            'name': region,
            'type': 'line',
            'showSymbol': False,
            'smooth': True,
            'data': region_data['BoxOffice'].tolist()  # Use .tolist() here
        })

    return {
        'dates': dates,
        'series': series_data
    }

# Route for the homepage
@app.route('/')
def index():
    return render_template('box_office.html')

# API endpoint to get data
@app.route('/data')
def data():
    return jsonify(get_chart_data())

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
