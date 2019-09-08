import json 
import os 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math

#open our inverted index file
with open('inverted-index.json', 'r') as f:
    j_data = json.load(f) 

# get the total number of documents
N = j_data['total_docs'] #get the total number of docs

#open the file that contains our keywords
with open ('keywords.txt', 'r') as f: #open the keyword file
    for line in f: #read the lines
        
        search = [] #stores our line
        line = line.lower() #make lower case       
        ps = PorterStemmer() #intialize the stemmer

        for word in word_tokenize(line): #tokenize our words
            search.append(ps.stem(word)) #add the tockenized words to our search line
        
        #for storing the final score and the scores per word, one will be sorted later
        score_dict = {}
        sorted_dict = {}
          
        for f in os.listdir("input"): #seatch through all files in input
            tot_score = 0 #initialize the total score for the search
            scores = {} #this will store the scores per file
            scores['file'] = f #create this key
            for word in search: #iterate through each word
                n = j_data[word]["docs_found_in"] #the number of docs the word was found in
                if f in list(j_data[word].keys()): #if the file we are looking at contains our word
                    num = j_data[word][f]  #get the frequency
                    weight = (1+math.log(int(num), 2))*(math.log((N/n), 2)) #calculate the weight
                else:
                    weight = 0 #if does not have our word,weight = 0
                tot_score += weight #increment the score for the document
                scores[word] = weight #add this to our scores per file
            scores['score'] = tot_score #add our total score to the scores array
            sorted_dict[f] = tot_score #add for the dict that holds the total scores, to be sorted
            score_dict[f] = scores #add for the dict that holds the weights per word
        
        print(scores)
        #list that contains our scores per doc in sorted order
        in_order = sorted(sorted_dict, key=sorted_dict.get, reverse = True) 

        print('------------------------------------------------------------')
        print('keywords = ',' '.join(search), sep="" ) 
        print("")
        rank = 0 #the rank is inititally 0 
        curr_min = math.inf #used to keep track of whether or not to increment rank
        for file in in_order: #traverse through files in sorted order
            if score_dict[file]['score'] < curr_min: #if the score is less than the current min score
                curr_min = score_dict[file]['score'] #the new current min is set
                rank +=1 #we increment the rank
            if score_dict[file]['score'] > 0: #if the word appears in the doc, print the doc and score
                print("[",rank,"]", " ", "file=",file, " " ,"score=", "%.6f" % score_dict[file]['score'],  sep="")
                for word in search: #print weights for the words in docs
                    print("    weight(", word,")=","%.6f" % score_dict[file][word], sep="" )
                print(" ")


                    
        
        
        
        
        
        
        
        
        
        

            