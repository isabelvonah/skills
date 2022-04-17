import pandas as pd 
import glob 
import os

# tutorial: https://www.tutorialspoint.com/how-to-merge-all-csv-files-into-a-single-dataframe-python-pandas

files = os.path.join(".", "03_scrape_offers_*.csv")
files = glob.glob(files)

df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.drop_duplicates(subset="id", inplace=True)
df.to_csv('03_scrape_offers.csv', index=False) 