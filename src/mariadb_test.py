import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.1.31",
    user="gardenguardian",
    passwd="Passwort123",
    database="gardenguardian_test"
)

mycursor = mydb.cursor()

sql = "Insert INTO measurements (measurementTime, measurementType, measurementValue) VALUES (%s, %s, %s)"
val = ("2019", "temperature", "12.0")

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
