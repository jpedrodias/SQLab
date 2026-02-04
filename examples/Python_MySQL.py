import pymysql

# DEFINIÇÕES DA LIGAÇÃO
DB = {
    "host": "localhost",
    "port": 3306,
    "user": "mysql_user",
    "password": "mysql_password",
    "database": "mydatabase",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,
}

# Ligação à base de dados MySQL
conn = pymysql.connect(**DB)

with conn.cursor() as cur:
    # 1) Drop + Create (exemplo)
    cur.execute("DROP TABLE IF EXISTS employees;")
    cur.execute("""
        CREATE TABLE employees (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(50) NOT NULL,
            salary DECIMAL(10, 2) NOT NULL,
            hire_date DATE NOT NULL,
            department VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL,
            address VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    
    # 2) SELECT (vazio)
    cur.execute("SELECT * FROM employees;")
    print("Tabela vazia:", cur.fetchall())
    
    
    # 3) INSERT
    rows = [
        ("Alice Johnson", "Software Engineer", 90000.00, "2020-01-15", "Engineering", "alice.johnson@example.com", "555-1234", "123 Elm St"),
        ("Bob Smith", "Data Analyst", 75000.00, "2019-03-22", "Data Science", "bob.smith@example.com", "555-5678", "456 Oak St"),
        ("Charlie Brown", "Project Manager", 85000.00, "2018-07-30", "Management", "charlie.brown@example.com", "555-8765", "789 Pine St"),
        ("Diana Prince", "UX Designer", 80000.00, "2021-05-10", "Design", "diana.prince@example.com", "555-4321", "321 Maple St"),
        ("Ethan Hunt", "DevOps Engineer", 95000.00, "2017-11-05", "Operations", "ethan.hunt@example.com", "555-9876", "654 Cedar St"),
        ("Fiona Gallagher", "HR Specialist", 70000.00, "2019-09-18", "Human Resources", "fiona.gallagher@example.com", "555-6543", "987 Birch St"),
        ("George Martin", "Marketing Manager", 82000.00, "2020-02-25", "Marketing", "george.martin@example.com", "555-3210", "159 Spruce St"),
        ("Hannah Lee", "Sales Representative", 68000.00, "2018-12-12", "Sales", "hannah.lee@example.com", "555-7890", "753 Willow St"),
        ("Ian Wright", "Financial Analyst", 78000.00, "2019-06-17", "Finance", "ian.wright@example.com", "555-2345", "852 Cherry St"),
        ("Jane Doe", "Customer Support", 65000.00, "2021-08-01", "Support", "jane.doe@example.com", "555-3456", "951 Walnut St"),
    ]
    
    cur.executemany("""
        INSERT INTO employees (name, position, salary, hire_date, department, email, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, rows)
    
    
    # 4) COMMIT
    conn.commit()
    
    # 5) SELECT (com dados)
    cur.execute("SELECT * FROM employees;")
    print("Tabela com dados:", cur.fetchall())

conn.close()