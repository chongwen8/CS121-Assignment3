
import time
from collections import defaultdict
from nltk.stem import PorterStemmer
import json
directory = "indices"

def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_token_index()->dict:
    file = open("token_index.txt", "r")
    result = dict()
    for line in file:
        line = line.split(",")
        result[line[0]] = int(line[1])
    return result


def return_docids(token:str, token_index:dict)->set:
    position = token_index[token]
    initial = token[0]
    if initial.isdigit():
        initial = "numeric"
    path = directory + "/" + initial + ".txt"
    file = open(path, "r")
    file.seek(position)
    file.readline()
    temp = file.readline().strip()
    file.close()
    return eval(temp)


def andquery(query):
    listx = list()
    for i in query: 
        word = stem(i)
        listx.append(return_docids(word,index_of_index))


    listx = sorted(listx, key = lambda x: len(x)) 
    if len(listx)==1:
        return listx[0]
    

    set1 = listx[0]
    for i in range(1,len(listx)):
        set2 = listx[i]
        set1 = set1.intersection(set2)
    return set1


def rank(doc_set,query,token_index):
    doc_freq = dict()
    for id in doc_set:
        doc_freq[id] = 0
    for word in query: 
        position = token_index[stem(word)]
        initial = word[0]
        if initial.isdigit():
            initial = "numeric"
        path = directory + "/" + initial + ".txt"
        file = open(path, "r")
        file.seek(position)
        file.readline()
        file.readline() 
        line = file.readline()
        while "#@" in line:
            line = line.split(',')
            frequency = int(line[1])
            docid = int(line[0])
            if docid in doc_set:
                doc_freq[docid] += frequency
            line = file.readline()
    return doc_freq




if __name__ == "__main__":
    index_of_index = read_token_index()


    query = ""
    while query== "":
        query = input("ENTER QUERY: ") 

    start_timer = time.time() #start timer
    query = query.split(" ")
    final_doc_ids = andquery(query)
    rank_dict = rank(final_doc_ids,query, index_of_index)
    with open('book_keeping.txt','r') as file:
        url_docid_dict = json.load(file)
        file.close()
    top_n = 5
    i = 0
    for docid in sorted(rank_dict, key = rank_dict.get, reverse = True): 
        if i < top_n:
            print(url_docid_dict[str(docid)])
            i += 1
    print("Search done in", time.time()-start_timer, "seconds")

