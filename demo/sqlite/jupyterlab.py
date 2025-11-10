# In JupyterLab - interact with shared database
import sqlite3
import pandas as pd

# Connect to shared database
conn = sqlite3.connect('/workspace/shared_data/employee_analytics.db')

# Query data
query = """
SELECT department, 
       COUNT(*) as count,
       AVG(salary) as avg_salary,
       AVG(performance_score) as avg_performance
FROM employees 
GROUP BY department
ORDER BY avg_salary DESC
"""

dept_summary = pd.read_sql_query(query, conn)
print("Department Summary from Shared Database:")
print(dept_summary)

# Log this analysis
conn.execute('''
INSERT INTO analysis_log (tool_used, analysis_type, notes)
VALUES (?, ?, ?)
''', ('JupyterLab', 'Department Analysis', 'Calculated department-level metrics'))

# Add a new calculated view
conn.execute('''
CREATE VIEW IF NOT EXISTS employee_insights AS
SELECT *,
       CASE 
           WHEN salary > (SELECT AVG(salary) FROM employees) AND performance_score > 7 THEN 'High Performer'
           WHEN salary < (SELECT AVG(salary) FROM employees) AND performance_score > 8 THEN 'Underpaid Star'
           ELSE 'Standard'
       END as performance_category
FROM employees
''')

conn.commit()

# Query the new view
insights = pd.read_sql_query("SELECT * FROM employee_insights LIMIT 10", conn)
print("\nEmployee Insights View:")
print(insights[['employee_id', 'department', 'salary', 'performance_category']])

conn.close()
