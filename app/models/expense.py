from app.models.initial_models import db  # Import db from initial_models to avoid circular import

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    split_method = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ExpenseSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount_owed = db.Column(db.Float, nullable=False)

def validate_percentage_split(splits):
    total_percentage = sum([split['percentage'] for split in splits])
    if total_percentage != 100:
        raise ValueError("Percentages do not add up to 100")
