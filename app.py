from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email

app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Blessed@123@localhost:5432/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zqvnfkicejlmiq:2497c589a48743b8fdab03ac0eb10b7251e9bb2fcfa223c35eb0daf5288a419a@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d2p5h1pn4bu6m0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class feedback_form(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments




# Routes
@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(feedback_form).filter(feedback_form.customer == customer).count() == 0:
            data = feedback_form(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_email(customer,dealer,rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!')


if __name__ == "__main__":
    app.run()
