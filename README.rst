rstwriter
=========
Report writing for Pandas using reStructuredTex

Installing
----------
.. code:: 
    pip install rstwriter

Usage
 
from rstwriter import RstWriter
report = RstWriter('sales.rst')
report.header('open')
report.paragraph('Some text in the header')
report.header('close')
report.title('h1', 'Awesome Report')
report.paragraph('Amazing text. Really cool.')
report.title('h2', 'Cool content')
#let's use some colors and styles... firts add a css file
report.css = 'ourstyles.css'`
# use classes from the added css to style paragraphs.
report.paragraph('I hope this is blue', style='blue-text')
data = pd.read_csv('sales.csv')
# .... do some statistics
# show your results in a table
report.table(data)
# Publish you report in html
report.publish('html')
```
