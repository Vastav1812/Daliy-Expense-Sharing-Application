import csv
from io import BytesIO, StringIO
from tkinter import Canvas
from flask import Response, request, jsonify, send_file
from app.models.expense import Expense, ExpenseSplit, validate_percentage_split
from app.models.initial_models import db

# Add expense
def add_expense():
    data = request.get_json()

    # Validate input data
    required_fields = ['description', 'total_amount', 'split_method', 'created_by']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        # Create new expense
        new_expense = Expense(
            description=data['description'],
            total_amount=data['total_amount'],
            split_method=data['split_method'],
            created_by=data['created_by']
        )
        db.session.add(new_expense)
        db.session.commit()

        # Handle splits
        splits = data.get('splits', [])
        if data['split_method'] == 'percentage':
            validate_percentage_split(splits)

        for split in splits:
            new_split = ExpenseSplit(
                expense_id=new_expense.id,
                user_id=split['user_id'],
                amount_owed=split['amount_owed']
            )
            db.session.add(new_split)

        db.session.commit()
        return jsonify({"message": "Expense added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Retrieve user expenses
def get_user_expenses(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    expenses = Expense.query.filter_by(created_by=user_id).paginate(page=page, per_page=per_page, error_out=False)

    if not expenses:
        return jsonify({"error": "No expenses found for this user"}), 404

    return jsonify([{
        'id': expense.id,
        'description': expense.description,
        'total_amount': expense.total_amount,
        'split_method': expense.split_method,
        'created_at': expense.created_at
    } for expense in expenses]), 200

def get_overall_expenses():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    expenses = Expense.query.paginate(page=page, per_page=per_page, error_out=False)

    overall_expenses = []

    for expense in expenses.items:  # Fetch items for the current page
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
        split_data = [{"user_id": split.user_id, "amount_owed": split.amount_owed} for split in splits]

        overall_expenses.append({
            "id": expense.id,
            "description": expense.description,
            "total_amount": expense.total_amount,
            "split_method": expense.split_method,
            "created_by": expense.created_by,
            "splits": split_data
        })

    return jsonify({
        'expenses': overall_expenses,
        'total': expenses.total,
        'pages': expenses.pages,
        'current_page': expenses.page
    }), 200
    
# Export expenses to PDF
def export_expenses_pdf():
    expenses = Expense.query.all()

    if not expenses:
        return jsonify({"error": "No expenses found"}), 404

    # Create a BytesIO buffer to store PDF data
    pdf_buffer = BytesIO()

    # Create a canvas for the PDF
    pdf = Canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle("Expenses Report")

    # Title
    pdf.setFont("Helvetica", 16)
    pdf.drawString(30, 750, "Expenses Report")

    # Write header
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 720, "Expense ID")
    pdf.drawString(150, 720, "Description")
    pdf.drawString(300, 720, "Total Amount")
    pdf.drawString(450, 720, "Split Method")
    pdf.drawString(550, 720, "Created By")

    # Write expense rows
    y = 700
    for expense in expenses:
        pdf.drawString(30, y, str(expense.id))
        pdf.drawString(150, y, expense.description)
        pdf.drawString(300, y, str(expense.total_amount))
        pdf.drawString(450, y, expense.split_method)
        pdf.drawString(550, y, str(expense.created_by))
        y -= 20

        if y < 50:
            pdf.showPage()  # Create a new page if content exceeds the page size
            y = 750

    pdf.save()

    # Create a response with the PDF data
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name='expenses.pdf', mimetype='application/pdf')

# Export expenses to CSV
def export_expenses_csv():
    expenses = Expense.query.all()

    if not expenses:
        return jsonify({"error": "No expenses found"}), 404

    # Create a StringIO buffer to store CSV data
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)

    # Write header
    writer.writerow(['Expense ID', 'Description', 'Total Amount', 'Split Method', 'Created By'])

    # Write expense rows
    for expense in expenses:
        writer.writerow([expense.id, expense.description, expense.total_amount, expense.split_method, expense.created_by])

    # Create a response with the CSV data
    csv_data = csv_buffer.getvalue()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=expenses.csv'})

def download_balance_sheet(user_id):
    # Fetch expenses for the user
    expenses = Expense.query.filter_by(created_by=user_id).all()

    # Create a CSV output
    output = StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow(['Expense ID', 'Description', 'Total Amount', 'Split Method', 'Amount Owed', 'User ID'])

    # Write expense data rows
    for expense in expenses:
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
        for split in splits:
            writer.writerow([expense.id, expense.description, expense.total_amount, expense.split_method, split.amount_owed, split.user_id])

    # Set up response to download as a CSV file
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=balance_sheet.csv"}
    )

# expense_controller.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def download_balance_sheet_pdf(user_id):
    # Fetch expenses for the user
    expenses = Expense.query.filter_by(created_by=user_id).all()

    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Balance Sheet")

    # Set up basic PDF structure
    pdf.drawString(100, 750, f"Balance Sheet for User ID: {user_id}")
    pdf.drawString(100, 730, "-----------------------------------------")

    y = 710
    for expense in expenses:
        pdf.drawString(100, y, f"Expense ID: {expense.id}")
        pdf.drawString(100, y - 20, f"Description: {expense.description}")
        pdf.drawString(100, y - 40, f"Total Amount: {expense.total_amount}")
        pdf.drawString(100, y - 60, f"Split Method: {expense.split_method}")
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
        for split in splits:
            pdf.drawString(100, y - 80, f"User ID: {split.user_id}, Amount Owed: {split.amount_owed}")
            y -= 100

    pdf.save()
    buffer.seek(0)

    return Response(
        buffer,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=balance_sheet.pdf"}
    )
