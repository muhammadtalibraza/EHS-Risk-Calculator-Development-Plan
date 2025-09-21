from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

# Industry-specific hazard templates
HAZARD_TEMPLATES = {
    "construction": [
        {"description": "Fall from height", "probability": 4, "severity": 5},
        {"description": "Struck by falling object", "probability": 3, "severity": 4},
        {"description": "Electrical hazard", "probability": 3, "severity": 4},
        {"description": "Caught in/between machinery", "probability": 2, "severity": 5},
        {"description": "Exposure to hazardous materials", "probability": 3, "severity": 3}
    ],
    "manufacturing": [
        {"description": "Machine entanglement", "probability": 3, "severity": 5},
        {"description": "Repetitive strain injury", "probability": 4, "severity": 3},
        {"description": "Exposure to loud noise", "probability": 4, "severity": 3},
        {"description": "Chemical exposure", "probability": 3, "severity": 4},
        {"description": "Slip and trip hazards", "probability": 4, "severity": 2}
    ],
    "healthcare": [
        {"description": "Needlestick injury", "probability": 3, "severity": 3},
        {"description": "Exposure to infectious diseases", "probability": 3, "severity": 4},
        {"description": "Patient handling injury", "probability": 4, "severity": 3},
        {"description": "Workplace violence", "probability": 2, "severity": 4},
        {"description": "Slip and fall on wet floors", "probability": 3, "severity": 2}
    ],
    "laboratory": [
        {"description": "Chemical exposure", "probability": 3, "severity": 4},
        {"description": "Fire/explosion risk", "probability": 2, "severity": 5},
        {"description": "Biological exposure", "probability": 2, "severity": 4},
        {"description": "Sharp object injury", "probability": 3, "severity": 2},
        {"description": "Radiation exposure", "probability": 1, "severity": 5}
    ],
    "office": [
        {"description": "Ergonomic injuries", "probability": 4, "severity": 2},
        {"description": "Eye strain from screens", "probability": 4, "severity": 2},
        {"description": "Slip and trip hazards", "probability": 3, "severity": 2},
        {"description": "Electrical hazards", "probability": 2, "severity": 3},
        {"description": "Stress and burnout", "probability": 4, "severity": 3}
    ]
}

# Control measures by risk level
CONTROL_MEASURES = {
    "low": [
        "Ensure good housekeeping practices",
        "Maintain clear warning signs",
        "Provide basic training and awareness"
    ],
    "medium": [
        "Implement administrative controls",
        "Develop safe work procedures",
        "Provide specific training",
        "Schedule regular inspections"
    ],
    "high": [
        "Implement engineering controls",
        "Use personal protective equipment",
        "Develop emergency procedures",
        "Conduct regular safety audits",
        "Provide specialized training"
    ],
    "extreme": [
        "Eliminate hazard if possible",
        "Implement multiple control layers",
        "Use highest level of PPE",
        "Implement continuous monitoring",
        "Establish strict access controls",
        "Develop comprehensive emergency response plans"
    ]
}

# Industry-specific control measures
INDUSTRY_CONTROL_MEASURES = {
    "construction": {
        "extreme": [
            "Implement fall protection systems",
            "Use safety harnesses and guardrails",
            "Establish exclusion zones",
            "Conduct daily safety meetings",
            "Provide specialized equipment training"
        ]
    },
    "manufacturing": {
        "extreme": [
            "Install machine guards and safety interlocks",
            "Implement lockout/tagout procedures",
            "Use appropriate PPE for each task",
            "Establish equipment maintenance schedules",
            "Provide hazard-specific training"
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    data = request.json
    probability = data.get('probability', 1)
    severity = data.get('severity', 1)
    industry = data.get('industry', 'general')
    
    risk_score = probability * severity
    
    if risk_score <= 3:
        risk_level = 'low'
    elif risk_score <= 8:
        risk_level = 'medium'
    elif risk_score <= 12:
        risk_level = 'high'
    else:
        risk_level = 'extreme'
    
    # Get control measures
    measures = CONTROL_MEASURES.get(risk_level, [])
    
    # Add industry-specific measures if available
    if industry in INDUSTRY_CONTROL_MEASURES and risk_level in INDUSTRY_CONTROL_MEASURES[industry]:
        measures.extend(INDUSTRY_CONTROL_MEASURES[industry][risk_level])
    
    return jsonify({
        'risk_level': risk_level,
        'risk_score': risk_score,
        'measures': measures
    })

@app.route('/get_template/<industry>')
def get_template(industry):
    hazards = HAZARD_TEMPLATES.get(industry, [])
    return jsonify(hazards)

@app.route('/export_report', methods=['POST'])
def export_report():
    data = request.json
    # In a real application, you would generate a PDF or Excel file here
    # For this example, we'll just return a success message
    return jsonify({
        'status': 'success',
        'message': 'Report exported successfully (simulated)',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)