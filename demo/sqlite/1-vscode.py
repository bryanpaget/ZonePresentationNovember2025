# In VS Code - create shared database
import sqlite3
import pandas as pd
from datetime import datetime

# Create SQLite database
conn = sqlite3.connect('/workspace/shared_data/employee_analytics.db')

# Create tables
conn.execute('''
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    department TEXT,
    salary REAL,
    performance_score INTEGER,
    years_experience INTEGER,
    bonus_eligible BOOLEAN,
    seniority TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS analysis_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_used TEXT,
    analysis_type TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
)
''')

# Insert sample data
employee_data = pd.read_csv('/workspace/shared_data/employee_analysis.csv')
employee_data.to_sql('employees', conn, if_exists='replace', index=False)

# Log the creation
conn.execute('''
INSERT INTO analysis_log (tool_used, analysis_type, notes)
VALUES (?, ?, ?)
''', ('VS Code', 'Database Setup', 'Created shared SQLite database with employee data'))

conn.commit()
print("SQLite database created and populated at /workspace/shared_data/employee_analytics.db")
print(f"Inserted {len(employee_data)} records")

conn.close()
