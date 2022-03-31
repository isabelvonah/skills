import RAKE
import operator

stop_dir = "stopwords_german.txt"
rake_object = RAKE.Rake(stop_dir)

with open('example_text.txt', "r") as geoeffnete_datei:
    subtitles = geoeffnete_datei.read()

def Sort_Tupel(tup):

    tup.sort(key = lambda x: x[1])
    return tup

keywords = Sort_Tupel(rake_object.run(subtitles))
print ("keywords: ", keywords)