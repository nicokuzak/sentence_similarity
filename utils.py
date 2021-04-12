import re
from collections import Counter


def clean(s: str) -> str:
    """Returns a cleaned version of the input, removing punctuation and lowercasing.

    Args:
        s (str): A string to clean

    Returns:
        str: The cleaned string.
    """
    s = re.sub(r'[^\w\s]', '', s)
    return s.lower()


def bow(s: str) -> dict:
    """Returns a pseudo Bag of Words representation of the input. A dictionary (Counter) of amount of times words are used.

    i.e. 'buffalo buffalo in new york' -> {'buffalo':2, 'in':1, 'new':1, 'york':1}
    Args:
        s (str): The string to get the BoW representation for.

    Returns:
        dict: {word: amount of times seen in string}
    """
    return Counter(s.split())


def ngrams(s: str, n: int) -> dict:
    """Returns a dictionary of n-grams and how often they are seen in the string.

    i.e.: 'I am coding therefore I am', 2 -> {('I', 'am'): 2, ('am','coding'):1, ('coding', 'therefore'): 1, ('therefore', 'I'): 1}

    Args:
        s (str): A string to create the n-gram dictionary for.
        n (int): The n- in n-gram. 2 == bigram, 3 == trigram.

    Returns:
        dict: {(ngram tuple): times seen in string}
    """
    lst = s.split()
    dct = {}
    num = len(lst) - n + 1
    for i in range(num):
        tup = tuple(lst[i:i + n])
        if tup in dct.keys():
            dct[tup] += 1
        else:
            dct[tup] = 1
    return dct


def bow_similarity(t1: str, t2: str) -> float:
    """Returns the BoW similarity of two strings. 
    
    First computes the BoW dictionaries, then gets the overlap of the two dictionaries. The overlap is the same words/total amount of words.

    Args:
        t1 (str): A string being compared
        t2 (str): Another string being compared

    Returns:
        float: The BoW similarity of the two strings.
    """
    bow1, bow2 = bow(t1), bow(t2)
    return overlap(bow1, bow2)


def ngram_similarity(t1: str, t2: str, n: int) -> float:
    """Returns the ngram similarity of two strings and n-gram n. 
    
    First computes the ngram dictionaries from function ngrams, then gets the overlap of the two dictionaries. 
    
    The overlap is the same words/total amount of words.

    Args:
        t1 (str): A string being compared
        t2 (str): Another string being compared
        n (int): The n- in ngrams.

    Returns:
        float: The ngram similarity of the two strings.
    """
    ngram1, ngram2 = ngrams(t1, n), ngrams(t2, n)
    return overlap(ngram1, ngram2)


def overlap(dict1: dict, dict2: dict) -> float:
    """Returns the overlap, or similarity, of two dictionaries. 
    
    The overlap is computed as follows:
    - For each dictionary, the denominator is the sum of all values (i.e. all of the n-grams and how many times they appear)
    - The numerator is the minimum of that key in both dicts, or 0 if that key is not in the other dictionary. 
    As a reminder, a "key" is either a word (in BoW) or an ngram. 

    Here are a few examples of ngrams, their values in two dictionaries, and the resulting overlap. Assume we are iterating through dict1.

    dict1 = {('Rewards are'): 2}; dict2 = {('Rewards are'), 1} -> 1/2
    dict1 = {('Rewards are'): 2}; dict2 = {('Rewards are'), 3} -> 2/2
    dict1 = {('Rewards are'): 2}; dict2 = {} -> 0/2

    Args:
        dict1 (dict): A dictionary of ngram or word: occurences
        dict2 (dict): Another dictionary of ngram or word: occurences

    Returns:
        float: The 'overlap', or similarity, between these two dictionaries.
    """
    same12 = total12 = same21 = total21 = 0
    for k, v in dict1.items():
        total12 += v  # Total is total amount of words
        if k in dict2.keys():
            same12 += min(
                v, dict2[k])  # sum by minimum occurence of key in both dicts
    for k, v in dict2.items():
        total21 += v
        if k in dict1.keys():
            same21 += min(v, dict1[k])
    sim12 = same12 / total12
    sim21 = same21 / total21
    return (sim12 + sim21) / 2