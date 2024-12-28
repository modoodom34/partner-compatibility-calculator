
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Simulated demographic data (in real app, would load from CSV files)
def generate_sample_data(n=10000):
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 100, n),
        'height_inches': np.random.normal(67, 4, n),
        'income': np.random.lognormal(11, 0.7, n),
        'bmi': np.random.normal(26, 4, n),
        'marital_status': np.random.choice(['single', 'married'], n, p=[0.4, 0.6]),
        'race': np.random.choice(['white', 'black', 'asian', 'other'], n),
    }
    return pd.DataFrame(data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = generate_sample_data()
    criteria = request.json
    
    # Apply filters
    mask = (
        (data['age'].between(criteria['age_min'], criteria['age_max'])) &
        (data['height_inches'].between(criteria['height_min'], criteria['height_max'])) &
        (data['income'] >= criteria['income_min'])
    )
    
    if criteria['exclude_obese']:
        mask &= (data['bmi'] <= 30)
    
    if criteria['marital_status'] == 'single':
        mask &= (data['marital_status'] == 'single')
        
    if criteria['race'] != 'all':
        mask &= (data['race'] == criteria['race'])
    
    matches = data[mask]
    total_matches = len(matches)
    
    return jsonify({
        'percentage': round((total_matches / len(data)) * 100, 2),
        'total_matches': total_matches,
        'confidence_level': 95,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
