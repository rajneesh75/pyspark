from databricks import sql
import os

connection = sql.connect(
    server_hostname="dbc-c379cba2-8489.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/76ac6ed093e25402",
    access_token="")



cursor = connection.cursor()

cursor.execute("SELECT * from range(10)")
print(cursor.fetchall())

cursor.close()
connection.close()
