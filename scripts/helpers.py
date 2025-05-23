import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def get_data():
  engine_name = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
  engine = create_engine(engine_name)

  query_sql = "SELECT * FROM topic_data"
  df = pd.read_sql_query(query_sql, con=engine)
  return df

def process_text(text):
  TAG_RE = re.compile(r'<[^>]+>')
  URL_RE = re.compile(r'http[s]?://\S+')
  text = URL_RE.sub('', text)
  text = TAG_RE.sub('',text)
  text = re.sub('[^a-zA-Z]', ' ', text)
  text = re.sub(r"\s+[a-zA-Z]\s+", ' ', text)
  text = re.sub(r'\s+', ' ', text).strip()
  return text

def process_data(df):
  df['text'] = df['text'].apply(process_text)
  df.drop(columns=['id'])
  return df

def display_data(df):
  label_counts = df['topic'].value_counts().sort_index()
  plt.bar(label_counts.index, label_counts.values, color=['blue','red','green','yellow','orange','purple'])
  plt.xticks(label_counts.index, ['tech','sport','politics','gaming','food','business'])  
  plt.xlabel('Label')
  plt.ylabel('Count')
  plt.title('Count of Labels')
  plt.show()