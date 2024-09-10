import os
from multiprocessing import Pool
from nltk import word_tokenize
import nltk 

nltk.download('punkt_tab')

def load_stopwords(file_path):
    with open(file_path, encoding='utf-8') as f:
        stopwords = set(f.read().split('\n')[:-1])
    return stopwords

absolute_path = 'D:\\VHT\\TextProcessing\\business\\clustering\\stopwords.txt'

stopwords = load_stopwords(absolute_path)
puct_set = set([c for c in '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'])

def generateBigram(paper):
    words = paper.split()
    if len(words) == 1:
        return ''
    bigrams = [words[i] + '_' + words[i+1] for i in range(0,len(words) - 1)]
    return ' '.join(bigrams)

def removeRedundant(text,redundantSet):
    words = text.split()
    for i in range(0,len(words)):
        if words[i].count('_') == 0 and (words[i] in redundantSet or words[i].isdigit()):
            words[i] = ''
        else:
            sub_words = words[i].split('_')
            if any(w in redundantSet or w.isdigit() for w in sub_words):
                words[i] = ''
    words = [w for w in words if w != '']
    words = ' '.join(words)
    return words

def preprocessing(document):
    text = document.get('text', '')
    text = ' '.join(word_tokenize(text))
    text = text.lower()
    text = ' '.join(text.split())
    text = text + generateBigram(text)
    text = removeRedundant(text, puct_set | stopwords)
    return {
        'time': document.get('time'),
        'text': text
    }


def preprocess_documents(documents, num_workers=10):
    pool = Pool(num_workers)
    clean_documents = pool.map(preprocessing, documents)
    pool.terminate()
    return clean_documents
