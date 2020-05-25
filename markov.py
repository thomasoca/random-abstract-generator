from collections import defaultdict
import pandas as pd
import random
import re
import string

df = pd.read_csv('data/ArXiv.csv')

def try_search(p, x):
    try:
        return bool(p.search(x))
    except TypeError:
        return False

def set_var(keywords):
    keywords_list = keywords.split(',')
    separator = '|'
    joined_keywords = separator.join(keywords_list)
    regex_pattern = r'{}'.format(joined_keywords)
    p = re.compile(regex_pattern)
    df_reduced = df[[try_search(p, x) for x in df['title']]]
    titles = df_reduced['title']
    abstract = df_reduced['abstract']
    return titles, abstract

def create_chain(sentences):
    chain = defaultdict(list)
    dict = {"(": "", ")": ""}
    translator = str.maketrans(dict)
    for line in sentences:
        line = line.split()
        for i,word in enumerate(line):
            if (re.search('(\([\w\s]+)', word) or re.search('([\w\s]\)$)', word)) and not re.search('\(.+\)$', word):
                word = word.translate(translator)
            if i < len(line)-1:
                if i == 0 :
                    chain['START'].append(word)
                if (re.search('(\([\w\s]+)', line[i+1]) or re.search('([\w\s]\)$)', line[i+1])) and not re.search('\(.+\)$', line[i+1]):
                    line[i+1] = line[i+1].translate(translator)
                chain[word].append(line[i+1])
            else:
                chain['END'].append(word)
    return chain

def create_sentences(chain, N):
    quote = [random.choice(chain['START'])]
    i = 0
    M = 0
    final_quote = quote[0] + " "
    while True:
        if len(chain[quote[i]]) == 0:
            choice = random.choice(chain['START'])
        else:
            choice = random.choice(chain[quote[i]])
        quote.append(choice)
        final_quote += choice + " "
        if choice not in chain['END'] and M > N:
            final_quote += random.choice(chain['END'])
            break
        elif choice in chain['END'] and M > N:
            break
        else:
            i += 1
            M += 1
    return final_quote
