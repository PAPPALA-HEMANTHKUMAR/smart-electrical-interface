from flask import Flask
from models import db, Electrician, ServiceRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///electrical.db'
db.init_app(app)

@app.route('/')
def home():
    return "Smart Electrical Interface Home!"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    from flask import jsonify

@app.route('/electricians')
def list_electricians():
    electricians = Electrician.query.all()
    output = []
    for e in electricians:
        output.append({
            "name": e.name,
            "skills": e.skills,
            "rating": e.rating,
            "location": e.location,
            "available": e.availability
        })
    return jsonify(output)
from flask import request
from ml.test_recommend import recommend_electricians

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    job_type = data.get('job_type')
    location = data.get('location')
    recommended = recommend_electricians(job_type, location)
    return jsonify(recommended)
from flask import render_template, request

@app.route('/form')
def form_page():
    return render_template("index.html")

@app.route('/recommend_form', methods=['POST'])
def recommend_form():
    job_type = request.form.get('job_type')
    location = request.form.get('location')
    electricians = recommend_electricians(job_type, location)
    return render_template("index.html", electricians=electricians)
@app.route('/submit_request', methods=['POST'])
def submit_request():
    job_type = request.form.get('job_type')
    location = request.form.get('location')
    urgency = request.form.get('urgency')

    # Create new request
    new_request = ServiceRequest(
        description=job_type,
        location=location,
        urgency=urgency
    )
    db.session.add(new_request)
    db.session.commit()

    # Smart recommendation
    recommended = recommend_electricians(job_type, location)

    return render_template("index.html", electricians=recommended)
@app.route('/requests')
def view_requests():
    requests = ServiceRequest.query.all()
    output = []
    for r in requests:
        output.append({
            "description": r.description,
            "location": r.location,
            "urgency": r.urgency,
            "electrician_id": r.electrician_id
        })
    return jsonify(output)
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from flask import redirect, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/form')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
if user.role == 'electrician':
    return redirect('/dashboard/electrician')
elif user.role == 'consumer':
    return redirect('/dashboard/consumer')
from flask_login import current_user

@app.route('/dashboard/electrician')
@login_required
def electrician_dashboard():
    if current_user.role != 'electrician':
        return redirect('/')
    jobs = ServiceRequest.query.filter_by(electrician_id=current_user.id).all()
    return render_template('electrician_dashboard.html', jobs=jobs)

@app.route('/dashboard/consumer')
@login_required
def consumer_dashboard():
    if current_user.role != 'consumer':
        return redirect('/')
    requests = ServiceRequest.query.filter_by().all()  # Later: filter by user
    return render_template('consumer_dashboard.html', requests=requests)
@app.route('/feedback')
@login_required
def feedback_page():
    return render_template("feedback.html")

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    electrician_id = request.form.get('electrician_id')
    rating = float(request.form.get('rating'))
    comment = request.form.get('comment')

    new_feedback = Feedback(
        rating=rating,
        comment=comment,
        electrician_id=electrician_id,
        consumer_id=current_user.id
    )
    db.session.add(new_feedback)
    db.session.commit()

    return "Thanks for your feedback!"