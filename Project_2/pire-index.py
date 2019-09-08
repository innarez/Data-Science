import os 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json

punct_nums = '''!()-[]{};:'"\,<>./?@#$%^&*_~1234567890''' #define the forbidden chars
word_list = [] #stores the words that appear in the docs
doc_count= 0 #how many total documents we have

for file in os.listdir("input"): #iterate through all files in inpur directory
    with open("input/"+file, 'r') as f: #open our file for reading
        doc_count+=1
        lines = [line.lower() for line in f] #make all lines lowercase in the file
 
        new_line = ""    
        #iterate through our lowercase lines and remove forbidden characters
        for line in lines:
            for char in line:
                if char not in punct_nums:
                    new_line = new_line + char

        ps = PorterStemmer()
        looper = 0      
        words = word_tokenize(new_line)#tokenize our words
    with open(file, 'w') as out: #open our file for writing 
        for word in words: #iterate through our words and stem
            words[looper] = ps.stem(word)  
            out.write(words[looper] + " ")
            if words[looper] not in word_list:#add new words to the list of words in all files
                word_list.append(words[looper])
            looper += 1
            
dict = {'total_docs': doc_count} #add the total document count to our dict data structure

for word in word_list: #search for every word in our list in each document
    inv_ind = {}
    docs = 0
    for file in os.listdir("input"): #search through each file
        with open(file, 'r') as f: 
            num_appears = 0
            for line in f:
                line_count = line.split().count(word) #find out how many times the word appears in each line of the file
                if line_count > 0: #if it appears more than once.....
                    num_appears += line_count #increment the count of how many times it appears in document
                    docs +=1 #increment document count           
                    inv_ind[file]= num_appears #add the file and the count of word in file to list
                else:
                    continue
    inv_ind['docs_found_in']= docs #add how many documents the word appears in to our list
    dict[word] = inv_ind #index the word to all of the info we just found

#write our inverted index to a json file 
with open('inverted-index.json', 'w') as j:
    json.dump(dict, j)


