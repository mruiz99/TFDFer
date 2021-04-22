import sys
from argparse import ArgumentParser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import string
import collections as co

"""  Class for calculating term and document frequency  """

class Words:
    """ Displaying term and document frequency for text documents.
    
    Attributes:
        file (str): text document
        stop (boolean):  enables filter to remove stopwords, default=False
        punc (boolean):  enables filter to remove punctuation marks, 
        default=False

    Side effects:
        prints results to the terminal       
    """
    
    def __init__(self, file, stop=False, punc=False):
        """
        Args:
            N (int):  total number of documents in the file
            count_docs (method):  counts the total number of documents
            in the file
        """
        self.file = file
        self.stop = True if stop is not False else False
        self.punc = True if punc is not False else False     
        self.N = 0
        self.count_docs()

    def open_file(self, all=None):
        """ Opens file to prepare for analysis.
        
        Side effects:
            generator expression sends the file records (words) to
            the retrieve() method for analysis
        """

        with open(self.file, encoding="utf-8") as f:
            for words in enumerate(f, 1):
                if len(words) > 0:
                    yield words

    def count_docs(self):
        """ Counts the number of documents in the text file.
        
        Side effects:
            file is re-opened and the attribute N records the
            counted documents.
        
        Returns:
            integer
        """

        with open(self.file, encoding="utf-8") as f:
            for words in f:
                self.N += 1
        
        return self.N
    
    def filter(self, data, filter=None):
        """ Filters stopwords and punctuation marks in the text file.
        
        Args:
            data (str):  text documents to be filtered
            filter (str):  filter options are 'stop','punc','both'

        Side effects:
            generator expression sends back filtered data (chars) to the
            retrieve() method for analysis
        """

        punc = set(string.punctuation)
        punc.add("”")
        punc.add("’")
        punc.add("“")
        stop_words = set(stopwords.words("english"))
        chars = co.deque()

        if filter == "stop":
            for words in data:
                if words not in stop_words:
                    chars.append(words)

        elif filter == "punc":
            for words in data:
                if words not in punc:
                    chars.append(words)

        else:
            if filter == "both":
                for words in data:
                    if words not in punc and words not in stop_words:
                        chars.append(words)

        yield chars

    def toke(self):
        """ Tokenizes the text documents to enable the term search.
        
        Side effects:
            all words found in the text document are transformed to
            lowercase format,
            filter() method is applied if attributes are True,
            generator expressions sends tokenized and filtered data
            (doc_num, words, toked) to the retrieve() method for analysis
        """

        for doc in self.open_file():
            doc_num = doc[0]
            docs = doc[1].strip()
            toked = nltk.word_tokenize(docs.lower())
        
            if self.stop == True and self.punc == False:
                stop = self.filter(toked, filter="stop")
                for words in stop:
                    yield doc_num, words
                
            elif self.punc == True and self.stop == False:
                punc = self.filter(toked, filter="punc")
                for words in punc:
                    yield doc_num, words
                
            else:
                if self.stop == True and self.punc == True:
                    both = self.filter(toked, filter="both")
                    for words in both:
                        yield doc_num, words
                else:
                    yield doc_num, toked

    def df(self, term):
        """ Calculates document frequency of the term entered by the user.
        
        Args:
            term (str):  the word to calculate document frequency
        
        Side effects:
            generator expressions sends data (checked) to the retrieve() method
            for analysis
        """

        checked = None

        for words in self.toke():
            doc_num = words[0]
            docs = set(words[1])
            if term in docs:
                checked = doc_num, term
                yield checked

    def tf(self, term):
        """ Calculates term frequency of the term entered by the user.
        
        Args:
            term (str):  the word to calculate term frequency
        
        Side effects:
            generator expressions sends data (checked) to the retrieve() 
            method for analysis
        """

        checked = None

        for words in self.toke():
            doc_num = words[0]
            docs = words[1]
            if term in docs:
                doc_counted = dict(co.Counter(docs))
                checked = doc_num, doc_counted[term]
                yield checked

    def word_check(self, term):
        """ Checks if the term entered by the user is found in the text documents.
        
        Args:
            term (str):  the word that is checked before frequency is calculated
        
        Side effects:
            only prints to the terminal if the word is not found in
            the text documents
        
        Returns:
            boolean
        """
        
        inside = False

        for num in self.toke():
            terms = set(num[1])
            if term in terms:
                inside = True
                return inside

        if inside == False:
            print("'" + term + "'", "NOT FOUND, TRY AGAIN.")

        return inside
    
    def k(self, data):
        """ Number of documents found with the term.
        
        Args:
            data (str):  contains the document number and the accompanied term
        
        Returns:
            integer
        """
        
        count = 0
        for freq in data:
            count += 1

        return count
    
    def common(self, n):
        """ Counts the terms found in the text documents.
        
        Args:
            n (str):  total number of text documents in the file
        
        Side effects:
            prints the document number and the total number of words
            found in the text document
        """

        for words in self.toke():
            doc_num = words[0]
            docs = words[1]
            counted_words = co.Counter(docs)
            print(doc_num, counted_words.most_common(n))

    def retrieve(self, doc=None, word=None):
        """ Number of documents found with the term.
        
        Args:
            data (str):  contains the document number and the accompanied term
        
        Side effects:
            if the term is found in the documents, it prints the document number, 
            the raw count of the term per document found,
            term frequency log normalization, 
            term frequency/inverse document frequency,
            document frequency and inverse document frequency,
            the term entered by the user,
            if the term is not found in the documents,
            it prints that no documents were found
        """

        if doc != None:
            pass
        else:
            word_check = self.word_check(word)

        if word != None and word_check == True:

            termf = self.tf(word)
            docf = self.df(word)
            IDF = co.namedtuple("IDF", ["norm_tf", "N", "k"])
            k = self.k(docf)

            print("WORD:", "'" + word + "'")

            for words in termf:
                docs = words[0]
                raw = words[1]

                norm_tf = round(math.log(raw + 1.0, 10), 6)
                print("DOC#:", docs, end=" ~ ")
                print("TF RAW COUNT:", raw, end=" ~ ")
                print("TF LOG NORMALIZATION:", norm_tf, end=" ~ ")
                idf = IDF(norm_tf, self.N, k)
                idf_comp = round(1.0 + math.log(idf[1]/idf[2], 10), 6)
                tfidf = round(idf[0]*idf_comp, 6)
                print("TF-IDF:", tfidf)

            idf2 = round(1.0 + math.log(idf[1]/idf[2], 10), 6)
            print("DOCUMENT FREQUENCY:", k, end=" ~ ")
            print("INVERSE DOCUMENT FREQUENCY:", idf2)
            print("WORD:", "'" + word + "'")

        else:

            if doc!= None:
                for words in self.open_file():
                    doc_num = words[0]
                    try:
                        if doc == doc_num:
                            print("DOC#:", doc_num)
                            docs = words[1]
                            print(docs)

                    except IndexError:
                        print("DOC NOT FOUND, TRY AGAIN.")
                        continue

def parse_args(arglist):

    parser = ArgumentParser()
    parser.add_argument("file", help="text to be analyzed",
                        type=str)
    args = parser.parse_args(arglist)

    return args

def main(arglist):

    args = parse_args(arglist)
    #w=Words(args.file)
    #love = w.retrieve(word="love")
    #doc = w.retrieve(doc=70)

    return None

if __name__ == "__main__":
    main(sys.argv[1:])