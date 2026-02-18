# pip install -r ./requirements.txt
from flask import Flask, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql_user:mysql_password@localhost:3306/mydatabase'

db = SQLAlchemy(app)

PAGE_TEMPLATE = '''
<!DOCTYPE html> 
<html lang="en">
<head>
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee List</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:hover { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Employee List</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Position</th>
            <th>Salary</th>
            <th>Hire Date</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Address</th>
        </tr>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.position }}</td>
            <td>{{ employee.salary }}</td>  
            <td>{{ employee.hire_date }}</td>
            <td>{{ employee.email }}</td>
            <td>{{ employee.phone }}</td>
            <td>{{ employee.address }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

class Employe(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    

    def __repr__(self):
        return f'<Employe {self.name}>'

@app.route('/')
def index():
    employees = Employe.query.all()
    return render_template_string(PAGE_TEMPLATE, employees=employees)

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.drop_all()  # Drop existing tables for a clean slate (optional)
        db.create_all()  # Create tables if they don't exist
        
        # Add a sample employee if the table is empty
        if Employe.query.count() == 0:
            
            sample_data = [
                {'name': 'Alice Johnson', 'position': 'Software Engineer', 'salary': 90000.00, 'hire_date': '2020-01-15', 'department': 'Engineering', 'email': 'alice.johnson@example.com', 'phone': '555-1234', 'address': '123 Elm St'},
                {'name': 'Bob Smith', 'position': 'Data Analyst', 'salary': 75000.00, 'hire_date': '2019-03-22', 'department': 'Data Science', 'email': 'bob.smith@example.com', 'phone': '555-5678', 'address': '456 Oak St'},
                {'name': 'Charlie Brown', 'position': 'Project Manager', 'salary': 85000.00, 'hire_date': '2018-07-30', 'department': 'Management', 'email': 'charlie.brown@example.com', 'phone': '555-8765', 'address': '789 Pine St'},
                {'name': "Diana Prince", "position": "UX Designer", "salary": 80000.0, "hire_date": "2021-05-10", "department": "Design", "email": "diana.prince@example.com", "phone": "555-4321", "address": "321 Maple St"},
                {'name': "Ethan Hunt", "position": "DevOps Engineer", "salary": 95000.0, "hire_date": "2017-11-05", "department": "Operations", "email": "ethan.hunt@example.com", "phone": "555-9876", "address": "654 Cedar St"},
                {'name': "Fiona Gallagher", "position": "HR Specialist", "salary": 70000.0, "hire_date": "2023-02-18", "department": "Human Resources", "email": "fiona.gallagher@example.com", "phone": "555-6543", "address":"987 Birch St"},
                {'name': 'George Martin', 'position': 'Marketing Manager', 'salary': 82000.00, 'hire_date': '2020-02-25', 'department': 'Marketing', 'email': 'george.martin@example.com', 'phone': '555-3210', 'address': '159 Spruce St'},
                {'name': 'Hannah Lee', 'position': 'Sales Representative', 'salary': 68000.00, 'hire_date': '2018-12-12', 'department': 'Sales', 'email': 'hannah.lee@example.com', 'phone': '555-7890', 'address': '753 Willow St'},
                {'name': 'Ian Wright', 'position': 'Financial Analyst', 'salary': 78000.00, 'hire_date': '2019-06-17', 'department': 'Finance', 'email': 'ian.wright@example.com', 'phone': '555-2345', 'address': '852 Cherry St'},
                {'name':"Jane Doe","position":"Customer Support","salary":65000.0,"hire_date":"2021-08-01","department":"Support","email":"jane.doe@example.com","phone":"555-3456","address":"951 Walnut St"}
            ]
            
            for data in sample_data:
                print('Adding employee:', data.get('name'))
                employee = Employe(**data)
                db.session.add(employee)
            db.session.commit()
        #end if no employees
        
    # end of app context        
         
    app.run(debug=True, host='0.0.0.0', port=5000)