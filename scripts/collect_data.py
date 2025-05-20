from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from make_db import create_connection

username_to_topic = {
  "techcrunch" : "tech",
  "ESPN" : "sport",
}

def get_facebook_posts(username, post_count_break):
  options = Options()
  options.headless = True
  driver = webdriver.ChromiumEdge(options=options)
  driver.get(f"https://www.facebook.com/{username}/posts")

  insert_sql = """
    INSERT INTO topic_data (
      text, source, topic
    ) VALUES (
      %s, %s, %s
    )
    """
  conn,cursor = create_connection()
  conn.autocommit = True

  seen_posts = set()
  post_count = 0

  while post_count < post_count_break:
    for _ in range(10):
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(0.5)
    elements = driver.find_elements(By.XPATH, '//div[@data-ad-preview="message"]')
    for element in elements:
      content = element.text
      if (content and content not in seen_posts):
        seen_posts.add(content)
        try:
          cursor.execute(insert_sql,(content,username,username_to_topic[username]))
          post_count+=1
        except(Exception) as error:
          print(error)
          conn.rollback
      if post_count >= post_count_break: break
  
  driver.quit()
  conn.close()
  cursor.close()

if __name__ == "__main__":
  get_facebook_posts("techcrunch",2000)
