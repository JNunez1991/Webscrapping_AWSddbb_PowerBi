import mysql.connector

conn = mysql.connector.connect(
    host="estadisticas.ckn6oeiko8za.us-east-1.rds.amazonaws.com",
    port=3306,
    user="rds_superuser_role",
    password="432fdasfvd9uuvcx",
    database="INE"
)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()
for db in databases:
    print(db)

cursor.close()
conn.close()
