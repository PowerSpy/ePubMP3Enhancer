import textract
import ebooklib
from ebooklib import epub

fileIn = "/Users/power_spy/Downloads/Spy School Goes South (Stuart Gibbs) (Z-Library).epub"
fileOut = "test.txt"

content = textract.process(fileIn, encoding='utf-8').decode()

with open(fileOut, 'w', encoding='utf-8') as fout:
        fout.write(content)