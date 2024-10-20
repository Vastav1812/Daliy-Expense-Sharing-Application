# **Daily Expenses Sharing Application**

### **Objective**

This backend application allows users to manage and share their daily expenses by splitting them based on three methods: equal, exact amounts, and percentages. The application provides user management, expense management, and features to generate downloadable balance sheets.

---

### **Features**

- **User Management**: 
  - Users can register with their email, name, and mobile number.
  - User authentication via JWT tokens.
  
- **Expense Management**:
  - Users can add expenses.
  - Expenses can be split using three methods:
    - **Equal**: Split equally among all participants.
    - **Exact**: Specify the exact amount each participant owes.
    - **Percentage**: Specify the percentage each participant owes, ensuring the total equals 100%.
  
- **Balance Sheet**:
  - Show individual user expenses.
  - Show overall expenses for all users.
  - Downloadable balance sheet in CSV and PDF formats.

---

### **Technologies Used**

- **Flask**: Web framework
- **Flask-JWT-Extended**: Authentication using JWT
- **Flask-Migrate**: Database migrations
- **SQLite**: Database

---

### **Expense Calculation Examples**

1. **Equal Split**: 
   - Scenario: You go out with 3 friends. The total bill is 3000. Each friend owes 1000.
   
2. **Exact Split**: 
   - Scenario: You go shopping with 2 friends and pay 4299. Friend 1 owes 799, Friend 2 owes 2000, and you owe 1500.
   
3. **Percentage Split**: 
   - Scenario: You attend a party with 2 friends and one cousin. You owe 50%, Friend 1 owes 25%, and Friend 2 owes 25%.

---

### **API Endpoints**

#### **User Endpoints**:
1. **Register a new user**: `POST /api/auth/register`
   - Request body: 
     ```json
     { 
       "name": "Vastav", 
       "email": "vastav1812@gmail.com", 
       "password": "password123", 
       "mobile": "9876543210" 
     }
     ```
   
2. **User login**: `POST /api/auth/login`
   - Request body: 
     ```json
     { 
       "email": "vastav1812@gmail.com", 
       "password": "password123" 
     }
     ```
   
3. **Retrieve user details**: `GET /api/users/<user_id>`

#### **Expense Endpoints**:
1. **Create expense**: `POST /api/expenses`
   - Request body: 
     ```json
     {
       "description": "Lunch",
       "total_amount": 300,
       "split_method": "equal",
       "created_by": 1,
       "splits": [
         {"user_id": 1, "amount_owed": 150},
         {"user_id": 2, "amount_owed": 150}
       ]
     }
     ```

2. **Retrieve user expenses**: `GET /api/expenses/<user_id>`

3. **Retrieve overall expenses**: `GET /api/expenses/overall`

4. **Download balance sheet**:
   - CSV: `GET /api/expenses/export/csv`
   - PDF: `GET /api/expenses/export/pdf`

5. **Update expense**: `PUT /api/expenses/<expense_id>`
   - Request body:
     ```json
     {
       "description": "Dinner",
       "total_amount": 500,
       "split_method": "exact",
       "created_by": 1,
       "splits": [
         {"user_id": 1, "amount_owed": 200},
         {"user_id": 2, "amount_owed": 300}
       ]
     }
     ```

6. **Delete expense**: `DELETE /api/expenses/<expense_id>`

---

### **Data Validation**

- Validate user inputs (name, email, mobile, etc.).
- Ensure percentages in the percentage split method add up to 100%.

---

### **Installation and Usage**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/daily-expenses-app.git
   cd daily-expenses-app
