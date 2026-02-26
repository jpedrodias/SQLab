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

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    
    # many-to-many via association object (because enrollments has extra field: gpa)
    enrollments = db.relationship(
        "Enrollment",
        backref="student",
        cascade="all, delete-orphan",
        lazy=True,
    )
    
    def __repr__(self):
        return f"<Student {self.id} {self.name!r}>"

class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    enrollments = db.relationship(
        "Enrollment",
        backref="major",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Major {self.id} {self.name!r}>"
    
class Enrollment(db.Model):
    """
    Junction table (many-to-many) with extra attribute (gpa).
    Composite primary key: (student_id, major_id)
    """
    __tablename__ = "enrollments"

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), primary_key=True)   
    major_id = db.Column(db.Integer, db.ForeignKey("majors.id"), primary_key=True)

    gpa = db.Column(db.Numeric(4, 2), nullable=False)  # MySQL DECIMAL(4,2)

    __table_args__ = (
        db.CheckConstraint("gpa >= 0.00 AND gpa <= 20.00", name="chk_gpa_range"),
    )

    def __repr__(self):
        return f"<Enrollment student_id={self.student_id} major_id={self.major_id} gpa={self.gpa}>"

# T O O L S =============================================================================================
MODELS = {
    'Student': Student,    
    'Major': Major,
    'Enrollment': Enrollment,
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
        
        # Add sample Students + Enrollments if the table is empty

        sample_data_majors = [
                'Computer Science', 
                'Economics', 
                'Biology', 
                'Engineering', 
                'Mathematics', 
                'Physics', 
                'Chemistry'
        ]
        
        if Major.query.count() == 0:
            for major_name in sample_data_majors:
                major = Major(name=major_name)
                db.session.add(major)
            db.session.commit()
        #end of sample majors
        
        
        sample_data_students = [
            {'name': 'Ana Silva',          'birthdate': '2007-03-14'},
            {'name': 'Bruno Costa',        'birthdate': '2006-11-02'},
            {'name': 'Carla Mendes',       'birthdate': '2007-07-29'},
            {'name': 'Daniel Rocha',       'birthdate': '2006-01-18'},
            {'name': 'Eva Santos',         'birthdate': '2007-09-05'},
            {'name': 'Filipe Almeida',     'birthdate': '2006-05-21'},
            {'name': 'Guilherme Ferreira', 'birthdate': '2007-12-10'},
            {'name': 'Helena Sousa',       'birthdate': '2006-08-03'},
            {'name': 'Inês Pereira',       'birthdate': '2007-02-27'},
            {'name': 'João Martins',       'birthdate': '2006-04-16'}
        ]
            
        if Student.query.count() == 0:
            for student_dict in sample_data_students:
                student = Student(**student_dict)
                db.session.add(student)
            db.session.commit()
        #end of students
        
        sample_data_enrollments = [
            {'student_name': 'Ana Silva',          'major_name': 'Computer Science', 'gpa': 17.50},
            {'student_name': 'Ana Silva',          'major_name': 'Mathematics',      'gpa': 16.80},
            {'student_name': 'Bruno Costa',        'major_name': 'Economics',        'gpa': 14.20},
            {'student_name': 'Bruno Costa',        'major_name': 'Mathematics',      'gpa': 13.90},
            {'student_name': 'Carla Mendes',       'major_name': 'Biology',          'gpa': 16.10},
            {'student_name': 'Carla Mendes',       'major_name': 'Chemistry',        'gpa': 15.40},
            {'student_name': 'Daniel Rocha',       'major_name': 'Engineering',      'gpa': 13.80},
            {'student_name': 'Eva Santos',         'major_name': 'Mathematics',      'gpa': 18.30},
            {'student_name': 'Eva Santos',         'major_name': 'Physics',          'gpa': 17.10},
            {'student_name': 'Filipe Almeida',     'major_name': 'Mathematics',      'gpa': 12.60},
            {'student_name': 'Guilherme Ferreira', 'major_name': 'Mathematics',      'gpa': 15.70},
            {'student_name': 'Guilherme Ferreira', 'major_name': 'Economics',        'gpa': 15.10},
            {'student_name': 'Helena Sousa',       'major_name': 'Physics',          'gpa': 16.90},
            {'student_name': 'Inês Pereira',       'major_name': 'Biology',          'gpa': 13.10},
            {'student_name': 'João Martins',       'major_name': 'Chemistry',        'gpa': 14.90},
            {'student_name': 'João Martins',       'major_name': 'Computer Science', 'gpa': 14.40},
        ]
        
        if Enrollment.query.count() == 0:
            for enrollment_dict in sample_data_enrollments:
                student = Student.query.filter_by(name=enrollment_dict.get('student_name')).first()
                major = Major.query.filter_by(name=enrollment_dict.get('major_name')).first()
                gpa = enrollment_dict.get('gpa')
                
                if None in (student, major):
                    print(f"Warning: Student or Major not found for enrollment: {enrollment_dict}")
                    continue
                
                enrollment = Enrollment(student=student, major=major, gpa=gpa)
                # or enrollment = Enrollment(student_id=student.id, major_id=major.id, gpa=gpa)
                db.session.add(enrollment)
            db.session.commit()
        #end of enrollments
        
    # end of app context        
         
    app.run(debug=True, host='0.0.0.0', port=5000)