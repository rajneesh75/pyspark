from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("DATABRICKS_HOST"), os.getenv("DATABRICKS_TOKEN"), os.getenv("DATABRICKS_CLUSTER_ID"))

connection = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOST"),
    http_path="/sql/1.0/warehouses/76ac6ed093e25402",
    access_token=os.getenv("DATABRICKS_TOKEN"))

print(connection)

cursor = connection.cursor()
cursor.execute("SELECT * from range(10)")
print(cursor.fetchall())

cursor.close()
connection.close()
