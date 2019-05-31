import psycopg2

conn = psycopg2.connect('host=192.168.1.31 user=pi password=PzFhr2017 dbname=plantguardian_test')


# conn = psycopg2.connect('host=192.168.1.31 user=pi password=PzFhr2017 dbname=test')

cur = conn.cursor()


def get_all_people():
    query = """
    SELECT
        measurementtime
    FROM
        measurements
    """
    cur.execute(query)
    return cur.fetchall()


def sendMeasurements(measurements):
    conn = psycopg2.connect('host=192.168.1.31 user=pi password=PzFhr2017 dbname=plantguardian_test')
    cursor = conn.cursor()
    query = """
    INSERT INTO
        measurements
    VALUES
        (%s, %s, %s)
    """
    for measurement in measurements:
        values = (measurement.measurementTime, measurement.measurementType, measurement.measurementValue)
        cur.execute(query, values)
        conn.commit()
    conn.close()
    cursor.close()


print(get_all_people())
