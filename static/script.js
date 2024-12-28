
function calculate() {
    const data = {
        age_min: parseInt(document.getElementById('age_min').value),
        age_max: parseInt(document.getElementById('age_max').value),
        height_min: parseInt(document.getElementById('height_min').value),
        height_max: parseInt(document.getElementById('height_max').value),
        income_min: parseInt(document.getElementById('income_min').value),
        exclude_obese: document.getElementById('body_type').value === 'non_obese',
        marital_status: document.getElementById('marital_status').value,
        race: document.getElementById('race').value
    };

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('results').style.display = 'block';
        document.getElementById('percentage').textContent = result.percentage;
        document.getElementById('total_matches').textContent = result.total_matches.toLocaleString();
        document.getElementById('confidence').textContent = result.confidence_level;
    });
}
