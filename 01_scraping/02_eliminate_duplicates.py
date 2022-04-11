import pandas as pd 
import glob 
import os

# tutorial: https://www.tutorialspoint.com/how-to-merge-all-csv-files-into-a-single-dataframe-python-pandas

files = os.path.join("~/Documents/github/skills/01_scraping/01_scrape_meta", "result*.csv")

files = glob.glob(files)

df = pd.concat(map(pd.read_csv, files), ignore_index=True) 
print(df)