import RAKE
import operator
import pandas as pd
import numpy as np


# rake doesn't understand ö,ä,ü as well as other characters
# turning markdown into one paragraph
def clean(texte):
    erg = texte.replace("ü","ue").replace("ä","ae").replace("ö","oe")
    specialChars = "!#$%^&*()" 
    for specialChar in specialChars:
        erg = erg.replace(specialChar, '')
    erg = erg.replace(',', '').replace('.','').replace('\n', ' ').replace('\t', ' ')
    erg = erg.replace('    ', ' ')
    rg = erg.replace('  ', ' ')
    erg = erg.lower()
    return erg

# order how results are listed
def Sort_Tupel(tup):

    # for sort: 0 = alphabetical, 1 = numerical
    tup.sort(key = lambda x: x[0])
    return tup


stop_dir = "stopwords_german.txt"
rake_object = RAKE.Rake(stop_dir)

# get csv
data = pd.read_csv("04_combine_clean_datasets.csv")


# get column text
col = data["text"]


lists = []


for i in range(len (col)):

    # select row
    row = col.iloc[i]

    # rake only works with string
    a = clean(str(row))
    #print(a)

    keywords = Sort_Tupel(rake_object.run(a))
    #print(keywords)

    neu = []
    # drop the rake-score
    for item in keywords:
        neu.append(item[0])
        

    lists.append(neu)

data['keyphrases'] = lists

# deletes all empty entries in column "text"
data.drop(data[data["text"].isna()].index, inplace=True)

print(data.head())

data.to_csv("05_offers_rake.csv", index=False)
