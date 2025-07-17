from models import db, Electrician
from app import app

sample_electricians = [
    {"name": "Amit Kumar", "skills": "Wiring, Fuse Replacement", "rating": 4.5, "location": "Hyderabad"},
    {"name": "Priya Reddy", "skills": "Appliance Installation", "rating": 4.8, "location": "Chennai"},
    {"name": "Rajesh Naidu", "skills": "Lighting Setup", "rating": 4.2, "location": "Nellore"},
    {"name": "Sneha Rao", "skills": "Troubleshooting", "rating": 4.9, "location": "Bangalore"}
]

with app.app_context():
    for e in sample_electricians:
        electrician = Electrician(**e)
        db.session.add(electrician)
    db.session.commit()
    print("Sample electricians added!")