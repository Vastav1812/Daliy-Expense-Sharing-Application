from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.expense_controller import add_expense, download_balance_sheet_pdf, export_expenses_csv, export_expenses_pdf, get_overall_expenses, get_user_expenses

# Define blueprint
expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json()
    return add_expense()

@expense_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_expenses_route(user_id):
    return get_user_expenses(user_id)

@expense_bp.route('/overall', methods=['GET'])
@jwt_required()
def overall_expenses():
    return get_overall_expenses()

# CSV export route
@expense_bp.route('/export/csv', methods=['GET'])
@jwt_required()
def download_csv():
    return export_expenses_csv()

# PDF export route
@expense_bp.route('/export/pdf', methods=['GET'])
@jwt_required()
def download_pdf():
    return export_expenses_pdf()

# expense_routes.py

from app.controllers.expense_controller import download_balance_sheet

@expense_bp.route('/balance_sheet/<int:user_id>', methods=['GET'])
def get_balance_sheet_csv(user_id):
    return download_balance_sheet(user_id)

@expense_bp.route('/balance_sheet_pdf/<int:user_id>', methods=['GET'])
def get_balance_sheet_pdf(user_id):
    return download_balance_sheet_pdf(user_id)