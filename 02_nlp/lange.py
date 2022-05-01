import RAKE
import operator
import pandas as pd
import numpy as np

orginal = pd.read_csv("04_combine_clean_datasets.csv")

edited = pd.read_csv("05_offers_rake.csv")



print("Reihen alter Datensatz: ",len(orginal))

print("Reihen neuer Datensatz: ",len(edited))

