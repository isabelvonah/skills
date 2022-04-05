import RAKE
import operator

stop_dir = "stopwords_german.txt"
rake_object = RAKE.Rake(stop_dir)

with open('job_example.txt', "r") as geoeffnete_datei:
    subtitles = geoeffnete_datei.read()

def Sort_Tupel(tup):

    tup.sort(key = lambda x: x[1])
    return tup

keywords = Sort_Tupel(rake_object.run(subtitles))

with open("rake_liste.txt", "w") as open_file:
    open_file.write(str(keywords))