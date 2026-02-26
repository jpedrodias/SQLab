# pip install -r ./requirements.txt
from datetime import date
from decimal import Decimal

from flask import Flask, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql_user:mysql_password@localhost:3306/mydatabase'

db = SQLAlchemy(app)


# T E M P L A T E S =====================================================================================
# This is a simple HTML template for displaying the data in a table format.
# The correct way should be to place a template file in the 'templates' directory and use render_template('template.html', ...) instead of render_template_string.

PAGE_TEMPLATE_INDEX = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Show Tables</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:hover { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Show Tables</h1>
    <table>
        <thead>
            <tr><th>Table Name</th> </tr>
        </thead>
        <tbody>
            {% for model_name in models %}
                <tr><td><a href="/show/{{ model_name }}">{{ model_name }}</a></td></tr>
            {% endfor %}
        </tbody>
    </table>
</body> 
</html>
"""

PAGE_TEMPLATE_SHOWTABLE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    tr:hover { background-color: #f5f5f5; }
  </style>
</head>
<body>
  <h1>{{ title }}</h1>

  <table>
    <thead>
      <tr>
        {% for col in columns %}
          <th>{{ col_labels.get(col, col) }}</th>
        {% endfor %}
      </tr>
    </thead>

    <tbody>
      {% for row in rows %}
        <tr>
          {% for col in columns %}
            <td>{{ row.get(col, "") }}</td>
          {% endfor %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


# M O D E L S ===========================================================================================
class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    # relationship to students (One-to-Many: One Major has many Students)
    students = db.relationship("Student", backref="major")
    
    def __repr__(self):
        return f"<Major {self.id} {self.name!r}>"
       

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Numeric(4, 2), nullable=False)  # MySQL DECIMAL(4,2)
    birthdate = db.Column(db.Date, nullable=False)
    
    major_id = db.Column(db.Integer, db.ForeignKey("majors.id"), nullable=True)
    
    __table_args__ = (
        db.CheckConstraint("gpa >= 0.00 AND gpa <= 20.00", name="chk_gpa_range"),
    )
        
    def __repr__(self):
        return f"<Student {self.id} {self.name!r}>"


# T O O L S =============================================================================================
MODELS = {
    'Student': Student,    
    'Major': Major,
}


def model_to_table(model, query, title=None, labels=None):
    columns = [c.key for c in model.__table__.columns]  # ordem do modelo
    rows = [
        {col: getattr(obj, col) for col in columns}
        for obj in query
    ]
    col_labels = labels or {c: c.replace("_", " ").title() for c in columns}
    col_labels = labels or {c: c for c in columns}
    return {
        "title": title or model.__tablename__,
        "columns": columns,
        "rows": rows,
        "col_labels": col_labels,
    }


# R O U T E S ===========================================================================================
@app.route('/')
def index():
    return render_template_string(PAGE_TEMPLATE_INDEX, models=MODELS.keys())


@app.route('/show/<model_name>')
def show_table(model_name):
    model = MODELS.get(model_name)
    if not model:
        return f'Model {model_name} not found', 404
    
    query = model.query.all()
    table_data = model_to_table(model, query)
    return render_template_string(PAGE_TEMPLATE_SHOWTABLE, **table_data)


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.drop_all()    # DANGER: Drop existing tables for a clean slate (optional)
        db.create_all()  # Create tables if they don't exist
        
        # Add a sample Majors if the table is empty
        if Major.query.count() == 0:    
            
            sample_data = [
                {'name': 'Computer Science'},
                {'name': 'Economics'},
                {'name': 'Biology'},
                {'name': 'Engineering'},
                {'name': 'Mathematics'},
                {'name': 'Physics'},
                {'name': 'Chemistry'},
            ]
            
            for data in sample_data:
                print('Adding major:', data.get('name'))
                major = Major(**data)
                db.session.add(major)
            db.session.commit()
        #end if no majors
        
        # Add a sample Student if the table is empty
        if Student.query.count() == 0:
            sample_data = [
                {"name": "Ana Silva", "gpa": 17.50, "birthdate": "2007-03-14", "major": "Computer Science"},
                {"name": "Bruno Costa", "gpa": 14.20, "birthdate": "2006-11-02", "major": "Economics"},
                {"name": "Carla Mendes", "gpa": 16.10, "birthdate": "2007-07-29", "major": "Biology"},
                {"name": "Daniel Rocha", "gpa": 13.80, "birthdate": "2006-01-18", "major": "Engineering"},
                {"name": "Eva Santos", "gpa": 18.30, "birthdate": "2007-09-05", "major": "Mathematics"},
                {"name": "Filipe Almeida", "gpa": 12.60, "birthdate": "2006-05-21", "major": "Mathematics"},
                {"name": "Guilherme Ferreira", "gpa": 15.70, "birthdate": "2007-12-10", "major": "Mathematics"},
                {"name": "Helena Sousa", "gpa": 16.90, "birthdate": "2006-08-03", "major": "Physics"},
                {"name": "Inês Pereira", "gpa": 13.10, "birthdate": "2007-02-27", "major": "Biology"},
                {"name": "João Martins", "gpa": 14.90, "birthdate": "2006-04-16", "major": "Chemistry"},
            ]
            for data in sample_data:
                print('Adding student:', data.get('name')) 
                major_name = data.pop("major")
                major = Major.query.filter_by(name=major_name).first()
                if not major:
                    print(f"Major '{major_name}' not found for student '{data.get('name')}'")
                    continue
                student = Student(**data, major=major)
                db.session.add(student)
            db.session.commit()
        #end if no students
        
    # end of app context        
         
    app.run(debug=True, host='0.0.0.0', port=5000)