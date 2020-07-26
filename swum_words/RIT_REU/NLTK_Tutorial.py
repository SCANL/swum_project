import nltk
from nltk.corpus import wordnet, stopwords, state_union  
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import ConditionalFreqDist
example_sentence = "This is an example showing off stop word filitration"
example_text = "Hello there, how are you! I am solid"
#Stop_words
stop_words = set(stopwords.words("english"))
words = word_tokenize(example_sentence)
filtered_sentence = []
for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)
#Stem
ps = PorterStemmer()
example_words = ["python","pythoner","pythoning"]
for w in example_words:
    ps.stem(w)
#Part-Of-Speech Tagger
words = word_tokenize(example_sentence)
#Wordnet
syn = list()
ant = list()
for synset in wordnet.synsets("Book"):
   for lemma in synset.lemmas():
      syn.append(lemma.name())    #add the synonyms
      if lemma.antonyms():    #When antonyms are available, add them into the list
          ant.append(lemma.antonyms()[0].name())
print('Synonyms: ' + str(syn))
print('Antonyms: ' + str(ant))
arr = wordnet.synsets('Good')
print(arr[0].lemma_names())
# Conditional Frequency
# Create a reference variable for Class SExprTokenizer 
tk = ConditionalFreqDist()     
# Create a string input
tk = ConditionalFreqDist() 
gfg = "G F G"
for word in word_tokenize(gfg): 
   condition = len(word) 
   tk[condition][word] += 1     
print(tk)