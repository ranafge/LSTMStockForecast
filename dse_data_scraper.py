import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

url = "https://www.dsebd.org/latest_share_price_scroll_l.php"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"class": "table table-bordered background-white shares-table fixedHeader"})

# টেবিল না পেলে এরর হ্যান্ডেল করো
if table is None:
    print("Table not found on the webpage!")
    exit()

headers = [header.text.strip() for header in table.find_all('th')]

rows = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) > 0:
        rows.append([col.text.strip() for col in cols])

df_new = pd.DataFrame(rows, columns=headers)

# আজকের তারিখ যোগ করো
today_date = datetime.today().strftime('%Y-%m-%d')
df_new['Date'] = today_date

file_name = "dse_stock_data.csv"

# ফাইল আছে কি না চেক করো এবং খালি কিনা চেক করো
if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    df_existing = pd.read_csv(file_name)
    # নতুন ও পুরানো ডেটা একত্র করো
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    # ডুপ্লিকেট রো বাদ দাও (পুরো রো মিললে)
    df_combined.drop_duplicates(inplace=True)
    df_combined.to_csv(file_name, index=False)
else:
    # নতুন ফাইল তৈরি করো
    df_new.to_csv(file_name, index=False)

print(f"Data saved/appended to {file_name}")
