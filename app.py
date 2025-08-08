from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Finances(db.Model):
    Item_Id = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.String(100), nullable=False)
    Item_Date = db.Column(db.String(20), nullable=False)
    Item_Price = db.Column(db.Float, nullable=False)
    Item_Description = db.Column(db.String(200))
    Item_Category = db.Column(db.String(20))

    def __repr__(self):
        return '<Task %r>' % self.Item_Id

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        task_request = request.form['content']
        date_request = request.form['date']
        price_request = request.form['price']

        description_request = request.form['description'] if request.form['description'] else "-"
        category_request = request.form['category']

        new_task = Finances(
            Item_Name=task_request,
            Item_Date=date_request,
            Item_Price=price_request,
            Item_Description=description_request,
            Item_Category=category_request
        )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the task.'

    else:
        tasks = Finances.query.order_by(Finances.Item_Id).all()
        total = sum(task.Item_Price for task in tasks)

        grocery_amount = Finances.query.filter_by(Item_Category='groseries').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
        restaurants_amount = Finances.query.filter_by(Item_Category='restaurants').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
        pharmacy_amount = Finances.query.filter_by(Item_Category='pharmacy').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
        public_transport_amount = Finances.query.filter_by(Item_Category='public_transport').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
        other_amount = Finances.query.filter_by(Item_Category='others').with_entities(func.sum(Finances.Item_Price)).scalar() or 0

        grocery_percent = (grocery_amount / total * 100) if total else 0
        restaurants_percent = (restaurants_amount / total * 100) if total else 0
        pharmacy_percent = (pharmacy_amount / total * 100) if total else 0
        public_transport_percent = (public_transport_amount / total * 100) if total else 0
        other_percent = (other_amount / total * 100) if total else 0

        return render_template(
            "index.html",
            tasks=tasks,
            total=total,
            grocery_percent=round(grocery_percent, 2),
            restourants_percent=round(restaurants_percent, 2),
            pharmacy_percent=round(pharmacy_percent, 2),
            public_transport_percent=round(public_transport_percent, 2),
            other_percent=round(other_percent, 2)
        )


@app.route('/delete/<int:id>')
def delete(id):
    purchase_to_delete = Finances.query.get_or_404(id)

    try:
        db.session.delete(purchase_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the purchase.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Finances.query.get_or_404(id)
    if request.method == 'POST':
        task.Item_Name = request.form['content']
        task.Item_Date = request.form['date']
        task.Item_Price = request.form['price']
        task.Item_Description = request.form['description']
        task.Item_Category = request.form['category']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task.'

    else:
        return render_template('edit.html', task=task)


@app.route('/chart-data')
def chart_data():
    grocery_amount = Finances.query.filter_by(Item_Category='groseries').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
    restaurants_amount = Finances.query.filter_by(Item_Category='restaurants').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
    pharmacy_amount = Finances.query.filter_by(Item_Category='pharmacy').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
    public_transport_amount = Finances.query.filter_by(Item_Category='public_transport').with_entities(func.sum(Finances.Item_Price)).scalar() or 0
    other_amount = Finances.query.filter_by(Item_Category='others').with_entities(func.sum(Finances.Item_Price)).scalar() or 0

    return jsonify({
        "labels": ["Groceries", "Restaurants", "Pharmacy", "Public Transport", "Others"],
        "amounts": [grocery_amount, restaurants_amount, pharmacy_amount, public_transport_amount, other_amount]
    })


if __name__ == "__main__":
    app.run(debug=True)
