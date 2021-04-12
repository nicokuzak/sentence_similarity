import traceback

from flask import Flask, json, request, jsonify

from utils import clean, bow_similarity, ngram_similarity

# Instantiate an instance of a Flask application
app = Flask(__name__)


#Predict Route. POST Request to demonstrate power of wrapping model in a Flask app.
@app.route('/predict', methods=['POST'])
def predict():
    """
    Returns the similarity of the two strings in the payload.

    The data of the payload should have two key:value pairs, with the keys being named "text1" and "text2".
    """
    try:
        x = request.get_json(silent=True)
        t1, t2 = x['text1'], x['text2']
        res = similarity(t1, t2)
        return str(res)

    except Exception:
        return jsonify({'error': 'exception', 'trace': traceback.format_exc()})


def similarity(t1: str, t2: str) -> float:
    """Calculates the similarity of the two input strings. Does the following:
    - If the two strings are equal, returns 1.0.
    - If the two strings are equal AFTER removal of punctuation and lowercasing the strings, 
    it returns the length of the new strings / length of original strings
    - If none of the above, calculates the similarity of the bag of words, bigrams, and trigrams.
    Similarities are computed as seen in utils. 
    For the final "similarity" score, bag of words similarity is weighted twice as much as bigrams, 
    which is weighted twice as much as trigrams.

    Similarity will thus range from 0 to 1.
    Args:
        t1 (str): A string being compared
        t2 (str): Another string being compared

    Returns:
        float: The similarity of the two strings computed by my algorithm.
    """
    # If they are the same, similarity == 1.0
    if t1.strip() == '' or t2.strip() == '':
        if t1 == t2:
            return 1.0
        return 0.0
    if t1 == t2:
        return 1.0

    # Clean, then if similar, return similarity score
    # If they are the same after lowering and punctuation, make the similarity the new length/ original length
    lens = len(t1) + len(t2)
    t1, t2 = clean(t1), clean(t2)
    if t1 == t2:
        return (len(t1) + len(t2)) / lens

    # Compute the BoW, bigram, and trigram similarity. Then return a weighted average.
    bow_sim = bow_similarity(t1, t2)
    bigram_sim = ngram_similarity(t1, t2, 2)
    trigram_sim = ngram_similarity(t1, t2, 3)
    return (bow_sim * 4 + bigram_sim * 2 + trigram_sim) / 7  #weigh BoW more


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)