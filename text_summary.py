import spacy
#import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
#import punctuation
from string import punctuation

'''Heap data structure is mainly used to represent a priority queue. In Python, it is available using the “heapq” module. The property of this data structure in Python is that each time the smallest heap element is popped(min-heap). Whenever elements are pushed or popped, heap structure is maintained. The heap[0] element also returns the smallest element each time. Let’s see various Operations on the heap in Python.'''
from heapq import nlargest

text = """PM Kisan is a government initiative in the country, and its purpose is to provide financial assistance to small and marginal farmers throughout the country. Launched by the Government of India in December 2018, the scheme aims to enhance and upgrade farmers' livelihoods by providing direct income support through direct cash transfers. One can check the PM Kisan beneficiary status on the government website.

Under the PM Kisan scheme, eligible farmers get financial assistance of ₹6,000 per year in three equal instalments of ₹2,000 each. This initiative's primary goal is to provide farmers with financial stability and even support them in fulfilling their agricultural expenses. The scheme is implemented by the Ministry of Agriculture and even Farmers Welfare and is believed to be one of the largest initiatives of its kind in the world.

To make the most of the benefits under PM Kisan, farmers need to fulfil certain types of eligibility criteria. Firstly, the scheme is appropriate only for small and marginal farmers who possess cultivable land. The definition of small and marginal farmers differs from state to state, but generally, it encompasses farmers having landholding of up to two hectares. Secondly, the scheme is restricted to families, and each eligible family can receive the benefits for up to somewhat four hectares of land."""

def summarizer(raw_docs):
    raw_docs=raw_docs.lower()
    text=raw_docs
    #Save stopwords in list
    stopwords=list(STOP_WORDS)
    #print(stopwords)

    #load nlp module
    nlp = spacy.load('en_core_web_sm')

    #load text in document
    doc = nlp(text)

    #Tokenization
    tokens = [token.text for token in doc]
    #print(tokens)

    #Check frequency of words
    word_freq ={}
    for word in doc:
        #print("word.text- ",word.text)
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text.lower() not in word_freq:
                word_freq[word.text] =1
            else:
                word_freq[word.text] +=1

    #print(word_freq)

    #Maximum fequency of words
    max_freq = max(word_freq.values())
    #print(max_freq)

    #Normalize frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
        
    # print(word_freq)

    #Sentence Tokenization

    sent_tokens= [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
                    
    # print(sent_scores)

    select_len = int(len(sent_tokens)*0.5)
    # print(select_len)

    #nlargest will pick highest frequency
    summary = nlargest(select_len,iterable=sent_scores,key=sent_scores.get)
    # print(summary)

    #Proper text
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print("text- ",text)
    # print("Length of Original text - ",len(text.split(' ')))
    # print("___________________________________________________________")
    # print("summary- ",summary)
    # print("Length of summary text - ",len(summary.split(' ')))
    return summary,doc,len(raw_docs.split(' ')), len(summary.split(' '))
