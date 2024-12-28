import json
import os
import psycopg2

# Get environment variables
host = os.getenv("POSTGRES_HOST", "db")
database = os.getenv("POSTGRES_DB", "tech_db")
user = os.getenv("POSTGRES_USER", "node-1")
password = os.getenv("POSTGRES_PASSWORD", "12345678")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)
cursor = conn.cursor()

# Fetch data from the PostgreSQL table
cursor.execute("SELECT id, name, description, category, care_instructions, available, created_at, updated_at FROM \"AAPlants_plant\"")
rows = cursor.fetchall()

# Prepare the bulk data for export (in JSON format)
bulk_data = []
for row in rows:
    bulk_data.append({
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "category": row[3],
        "care_instructions": row[4],
        "available": row[5],
        "created_at": row[6].isoformat() if row[6] else None,
        "updated_at": row[7].isoformat() if row[7] else None,
    })

# Write the bulk data to a JSON file
with open("/app/plants_export.json", "w") as file:
    json.dump(bulk_data, file)

# Close the database connection
cursor.close()
conn.close()

print("Export completed: 'plants_export.json' generated successfully.")
