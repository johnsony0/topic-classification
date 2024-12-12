# Visualizing external data (such as twenty_newsgroups, ag_news, DBpedia, Reuters-21578, and BBC News Archive)

import matplotlib.pyplot as plt
from datasets import load_dataset
import pandas as pd
import numpy as np
import os

def get_external_data():
  ag_news_path = "data/ag_news.csv"
  bbc_news_path = "data/bbc-news-data.csv"
  news_dataset_path = "data/News-Dataset-Seq.csv"
  ad_dataset_path = "data/ad-data.csv"
  
  # create data folder if not yet exists
  if not os.path.exists("data"):
        os.mkdir("data")

  # download external data if it does not exist yet
  if not os.path.exists(ag_news_path):
    ds = load_dataset("SetFit/ag_news")
    df_train = pd.DataFrame(ds['train'])
    df_test = pd.DataFrame(ds['test'])
    df = pd.concat([df_train, df_test], ignore_index=True)
    df.to_csv(ag_news_path, index=False)

  if not os.path.exists(bbc_news_path):
    ds = load_dataset("SetFit/bbc-news")
    df_train = pd.DataFrame(ds['train'])
    df_test = pd.DataFrame(ds['test'])
    df = pd.concat([df_train, df_test], ignore_index=True)
    df.to_csv(bbc_news_path, index=False)

  if not os.path.exists(news_dataset_path):
    ds = load_dataset("prithivMLmods/News-Dataset-Seq")
    df = pd.DataFrame(ds['train'])
    df.to_csv(news_dataset_path, index=False)

  if not os.path.exists(ad_dataset_path):
    ds = load_dataset("PeterBrendan/Ads_Creative_Ad_Copy_Programmatic")
    df = pd.DataFrame(ds['train'])
    df.to_csv(ad_dataset_path, index=False)
  
  print("Data downloaded or already exists.")
  # visualize each to see the distribution of classes
  ag_news_df = pd.read_csv(ag_news_path)
  ag_news_df['label_text'] = ag_news_df['label_text'].replace({
    "Business": "business",
    "Sci/Tech": "tech",
    "Sports": "sport",
    "World": "politics"
  })
  bbc_news_df = pd.read_csv(bbc_news_path)
  news_dataset_df = pd.read_csv(news_dataset_path)
  ad_dataset_df = pd.read_csv(news_dataset_path)

  weight_counts = {
    "ag_news": ag_news_df['label_text'].value_counts(),
    "bbc_news": bbc_news_df['label_text'].value_counts(),
    "news_dataset": news_dataset_df['label_text'].value_counts(),
    "ad_dataset": pd.Series({"ads": len(ad_dataset_df)})
  }  
  all_categories = set()
  for counts in weight_counts.values():
      all_categories.update(counts.index)
  all_categories = sorted(all_categories)
  num_categories = len(all_categories)
  bottom = np.zeros(num_categories)
  fig, ax = plt.subplots(figsize=(10, 6))
  for dataset_name, weight_count in weight_counts.items():
      aligned_counts = [weight_count.get(cat, 0) for cat in all_categories]
      ax.bar(
          all_categories,
          aligned_counts,
          label=dataset_name,
          bottom=bottom
      )
      bottom += aligned_counts
  ax.set_title("Distribution of Labels")
  ax.set_ylabel("Count")
  ax.set_xlabel("Labels")
  ax.legend(loc="upper right")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.show()

if __name__ == "__main__":
  get_external_data()