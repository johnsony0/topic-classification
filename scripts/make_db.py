import psycopg2
import os

def create_connection():
  conn = psycopg2.connect(
    database = os.getenv('DB_NAME'),
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    port = os.getenv('5432')
  )
  cursor = conn.cursor()
  return conn, cursor

def create_fb_data_table():
  #create connection to db
  conn, cursor = create_connection()

  table_check_sql = """
  SELECT EXISTS (
    SELECT FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename = 'topic_data'
  );
  """

  create_table_sql = """
    CREATE TABLE topic_data (
      id SERIAL PRIMARY KEY,
      text TEXT NOT NULL,
      source TEXT NOT NULL,
      topic TEXT NOT NULL,
      UNIQUE (text)
    );
    """
  try:
    cursor.execute(table_check_sql)
    table_exists = cursor.fetchone()[0]
    if not table_exists:
      cursor.execute(create_table_sql)
      conn.commit()
      print("Table created successfully")
    else:
      print("Table exists")
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

  cursor.close()
  conn.close()

if __name__ == "__main__":
  create_fb_data_table()

