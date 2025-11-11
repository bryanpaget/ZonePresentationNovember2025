# In RStudio - advanced database operations
library(RSQLite)
library(DBI)
library(dplyr)

# Connect to shared database
conn <- dbConnect(SQLite(), "/workspace/shared_data/employee_analytics.db")

# Check what's in the database
cat("Database Tables:\n")
print(dbListTables(conn))

# Query the insights view
insights <- dbGetQuery(conn, "SELECT * FROM employee_insights")
cat("\nPerformance Categories:\n")
print(table(insights$performance_category))

# Complex analysis using dplyr
analysis <- insights %>%
  group_by(performance_category, department) %>%
  summarise(
    count = n(),
    avg_salary = mean(salary),
    avg_experience = mean(years_experience),
    .groups = 'drop'
  )

cat("\nPerformance Analysis:\n")
print(analysis)

# Log R analysis
dbExecute(conn, "
INSERT INTO analysis_log (tool_used, analysis_type, notes)
VALUES ('RStudio', 'Performance Category Analysis', 'Analyzed employee performance categories across departments')
")

# Check analysis history
history <- dbGetQuery(conn, "
SELECT tool_used, analysis_type, timestamp, notes 
FROM analysis_log 
ORDER BY timestamp DESC
")

cat("\nAnalysis History:\n")
print(history)

dbDisconnect(conn)
