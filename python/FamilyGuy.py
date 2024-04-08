import spacy
import os, shutil
# Our challenge: read in multiple text files from a directory:
# What is os? This is a library that allows Python to read your operating system (os).
# This will let Python read and interpret file paths on your local computer.
# shutil will let us remove unwanted files from a directory.

# FOR XML OUTPUT: You'll need to install dicttoxml
# pip install dicttoxml, or use the Pycharm package manager
from dicttoxml import dicttoxml
# xml.dom.minidom comes with Python so you have it already
from xml.dom.minidom import parseString

# FOR DATAFRAMES OUTPUT
# You'll need to install pandas
# pip install pandas, or use the Pycharm package manager
import pandas as pd

# FOR JSON OUTPUT
import json

nlp = spacy.cli.download("en_core_web_md")
nlp = spacy.load('en_core_web_md')

workingDir = os.getcwd()
print("current working directory: " + workingDir)

# os.listdir lists files and folders inside a path:
insideDir = os.listdir(workingDir)
print("inside this directory are the following files AND directories: " + str(insideDir))

# use os.path.join to connect the subdirectory to the working directory:
CollPath = os.path.join(workingDir, 'TXT_files')
print(CollPath)


def readTextFiles(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        readFile = f.read()
        # print(readFile)
        stringFile = str(readFile)
        lengthFile = len(readFile)
        print(lengthFile)
        # ebb: add that utf8 encoding argument to the open() function to ensure that reading works on everyone's systems
        # this all succeeds if you see the text of your files printed in the console.
        tokens = nlp(stringFile)
        # playing with vectors here
        vectors = tokens.vector

        wordOfInterest = nlp(u'joking')
        # print(wordOfInterest, ': ', wordOfInterest.vector_norm)

        # Now, let's open an empty dictionary! We'll fill it up with the for loop just after it.
        # The for-loop goes over each token and gets its values
        highSimilarityDict = {}
        for token in tokens:
            if (token and token.vector_norm):
                # if token not in highSimilarityDict.keys(): # Alas, this did not work to remove duplicates from my dictionary. :-(
                if wordOfInterest.similarity(token) > .3:
                    highSimilarityDict[token] = wordOfInterest.similarity(token)
                    # The line above creates the structure for each entry in my dictionary.
                    # print(token.text, "about this much similar to", wordOfInterest, ": ", wordOfInterest.similarity(token))
        print("This is a dictionary of words most similar to the word " + wordOfInterest.text + " in this file.")
        print(highSimilarityDict)
        switcheroo = {val: key for key, val in highSimilarityDict.items()}
        deduped = {val: key for key, val in switcheroo.items()}
        print(str(len(switcheroo)) + ' **** ' + f'{switcheroo=}')

        print(len(deduped), ' **** ', f'{deduped=}')
        print(len(deduped.items()), " vs ", len(highSimilarityDict.items()))

        highSimilarityReduced = {}
        for key, value in highSimilarityDict.items():
            if value not in highSimilarityReduced.values():
                highSimilarityReduced[key] = value
        print(highSimilarityReduced)
        print(len(highSimilarityReduced.items()), " vs ", len(highSimilarityDict.items()))


        sortedSimValues = sorted(deduped.items(), key=lambda x: x[1], reverse=True)
        print(type(sortedSimValues), f'{sortedSimValues=}')

        sortedSimDict = dict(sortedSimValues)
        print(type(sortedSimValues), f'{sortedSimValues=}')

        return sortedSimDict


# ebb: This controls our file handling as a for loop over the directory:
with open('similarityReadings.txt', 'a', encoding='utf8') as f:
    for file in sorted(os.listdir(CollPath)):
        # My filenames are numbered, so I controlled the order of the for loop by sorting them.
        if file.endswith(".txt"):
            filepath = f"{CollPath}/{file}"
            print(filepath)
            similarityData = readTextFiles(filepath)
            f.write(filepath + '\n')
            f.write(str(similarityData) + '\n\n')
    # ***************  HOW TO OUTPUT DICTIONARY STRUCTURES  ****************
    # If we convert it to a string, it comes out as a list of tuples.
    # That's okay, but it's not a great data structure to work with.
    # Let's try outputting a few different data structures from a dictionary
    if os.path.exists("JSON-output"):
        shutil.rmtree("JSON-output")
    if os.path.exists("csv-output"):
        shutil.rmtree("csv-output")
    if os.path.exists("xml-output"):
        shutil.rmtree("xml-output")
    os.mkdir('JSON-output')
    os.mkdir('csv-output')
    os.mkdir('xml-output')

    df = pd.DataFrame.from_dict(similarityData.items(), orient="columns")
    df.columns = ['token', 'similarity']
    print(df)
    df.to_csv(f'csv-output/{file}.tsv', sep='\t', index=False, encoding='utf-8')

if os.path.exists("JSON-output"):
    shutil.rmtree("JSON-output")
if os.path.exists("csv-output"):
    shutil.rmtree("csv-output")
if os.path.exists("xml-output"):
    shutil.rmtree("xml-output")

os.mkdir('JSON-output')
os.mkdir('csv-output')
os.mkdir('xml-output')

for file in sorted(os.listdir(CollPath)):
    # My filenames are numbered, so I controlled the order of the for loop by sorting them.
    if file.endswith(".txt"):
        filepath = f"{CollPath}/{file}"
        print(filepath)
        filenameTxt = os.path.basename(filepath).split('/')[-1]
        filename = filenameTxt[:-4]
        print(filename)
        similarityData = readTextFiles(filepath)

        # ============================================ #
        # JSON: DICTIONARY OUTPUT METHOD 2
        # JSON stands for JavaScript Object Notation
        # It's an adaptable file serialization format for dictionary structures used for web programming
        stringKeys = {str(key): val for key, val in similarityData.items()}
        print(f'{stringKeys=}')
        with open(f'JSON-output/{filename}.json', 'w') as fp:
            JSON = json.dumps(stringKeys)
            print(f'{JSON=}')
            json.dump(stringKeys, fp)
        # ============================================ #
        # JSON stands for JavaScript Object Notation
        # It's an adaptable file serialization format for dictionary structures used for web programming
        # ============================================ #
        # PANDAS DATA FRAMES: DICTIONARY OUTPUT METHOD 3
        stringKeys = {str(key): val for key, val in similarityData.items()}
        print(f'{stringKeys=}')
        with open(f'JSON-output/{filename}.json', 'w') as fp:
            JSON = json.dumps(stringKeys)
            print(f'{JSON=}')
            json.dump(stringKeys, fp)
        # ============================================ #
        # Data Frames are used heavily in data analytics.
        # They make a tabular (table) structure and are easily output as a CSV or TSV text file
        df = pd.DataFrame.from_dict(similarityData.items(), orient="columns")
        df.columns = ['token', 'similarity']
        print(df)
        df.to_csv(f'csv-output/{filename}.tsv', sep='\t', index=False, encoding='utf-8')
        # I want to make a tsv file (tab-separated values), so I'm using the \t here.
        # to make a comma-separated values csv, put in a ','

    # ============================================ #
    # XML: DICTIONARY OUTPUT METHOD 4
    # ============================================ #
    # This tutorial is good: https://www.geeksforgeeks.org/serialize-python-dictionary-to-xml/
        xml = dicttoxml(similarityData)
        dom = parseString(xml)
        # dom is just a string. We can pretty print it in the console,
        # but this is not good for writing to an XML file.
        print(dom.toprettyxml())
        with open(f'xml-output/{filename}.xml', 'w') as xmlFile:
            xml_decode = xml.decode()
            xmlFile.write(xml_decode)
            xmlFile.close()
