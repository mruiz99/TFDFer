# TFDFer
Python script to calculate term and document frequency, three text documents included.

To run from the terminal, one parameter is required (name of file).
i.e., python tfdfer.py "jantrump.txt"

To enable filters, see the code in the main() function below.

ex.

w=Words(args.file, stop=True, punc=True)  <-- creates object 'w' to run term and document frequency calculations, optional parameters enabled
love = w.retrieve(word="love")  <-- prints term and document frequency information in object 'w'
doc = w.retrieve(doc=70)  <-- prints relevant document by number in object 'w'
common = w.common(5)  <-- prints top 5 most common characters found in object 'w'

# OPTIONAL PARAMETERS

'stop' parameter enables a filter to remove stopwords.
'punc' parameter enables a filter to remove punctuation marks.

# RUNNING IN INTERACTIVE MODE

Enable interactive mode by entering 'python' or 'python3' in the terminal.  After entering interactive mode,
import the class from the script to create objects for calculating term and document frequency.

ex.

>>> from tfdfer import Words  <-- imports class Words from the script tfdfer.py
>>> w=Words("jantrump.txt", True, True)  <-- creates object 'w' to run term and document frequency calculations, optional parameters enabled
>>> w.retrieve(word="love")  <-- prints term and document frequency information in object 'w'
>>> w.retrieve(doc=81)  <-- prints relevant document by number in object 'w'
>>> w.common(5) <-- prints top 5 most common characters found in object 'w'
