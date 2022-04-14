import pandas as pd 
import glob 
import os

# tutorial: https://www.tutorialspoint.com/how-to-merge-all-csv-files-into-a-single-dataframe-python-pandas

files = os.path.join("01_scrape_meta", "result*.csv")
files = glob.glob(files)

df = pd.concat(map(pd.read_csv, files), ignore_index=True)
print(df.info())
df.drop_duplicates(subset="id", inplace=True)
print(df.info())
print(df.value_counts("id"))
df.to_csv('02_eliminate_duplicates.csv', index=False) 