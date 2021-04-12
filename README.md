# Sentence Similarity
Sentence similarity with only built-in libraries.

### Build the Docker Image

`sh build.sh`

### Run the container locally

`sh run.sh`

### Test out a few cURL requests

Test out a few requests. An example is in req.ipynb.

The data in the payload should contain two keys - "text1" and "text2", which are python strings. 

The model will return a string with the similarity of two strings, between 0 and 1.