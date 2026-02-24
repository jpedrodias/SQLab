# pip install -r ./requirements.txt
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
    major = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Student {self.name}>'


# T O O L S =============================================================================================
MODELS = {
    'Student': Student,    
}


def model_to_table(model, query, title=None, labels=None):
    columns = [c.key for c in model.__table__.columns]  # ordem do modelo
    rows = [
        {col: getattr(obj, col) for col in columns}
        for obj in query
    ]
    col_labels = labels or {c: c.replace("_", " ").title() for c in columns}
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
        db.drop_all()  # Drop existing tables for a clean slate (optional)
        db.create_all()  # Create tables if they don't exist
        
        # Add a sample student if the table is empty
        if Student.query.count() == 0:    
        
            sample_data = [
                {'name': 'Ana Silva', 'major': 'Computer Science', 'gpa': 17.5, 'birthdate': '2007-03-14'},
                {'name': 'Bruno Costa', 'major': 'Mathematics', 'gpa': 14.2, 'birthdate': '2006-11-02'},
                {'name': 'Carla Mendes', 'major': 'Biology', 'gpa': 16.1, 'birthdate': '2007-07-29'},
                {'name': 'Daniel Rocha', 'major': 'Engineering', 'gpa': 13.8, 'birthdate': '2006-01-18'},
                {'name': 'Eva Santos', 'major': 'Mathematics', 'gpa': 18.3, 'birthdate': '2007-09-05'},
                {'name': 'Filipe Almeida', 'major': 'Mathematics', 'gpa': 12.6, 'birthdate': '2006-05-21'},
                {'name': 'Guilherme Ferreira', 'major': 'Mathematics', 'gpa': 15.7, 'birthdate': '2007-12-10'},
                {'name': 'Helena Sousa', 'major': 'Physics', 'gpa': 16.9, 'birthdate': '2006-08-03'},
                {'name': 'Inês Pereira', 'major': 'Biology', 'gpa': 13.1, 'birthdate': '2007-02-27'},
                {'name': 'João Martins', 'major': 'Chemistry', 'gpa': 14.9, 'birthdate': '2006-04-16'},
            ]
            
            for data in sample_data:
                print('Adding student:', data.get('name'))
                student = Student(**data)
                db.session.add(student)
            db.session.commit()
        #end if no students
        
    # end of app context        
         
    app.run(debug=True, host='0.0.0.0', port=5000)