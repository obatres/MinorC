from PyQt5.QtGui import *
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextFormat, QColor, QTextCharFormat, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


lista = [2,3,4,6,5,7]
print(lista)



i=0
while i<=len(lista):
    if(lista[i]==5):
        break
    else:
        i+=1

print('este es el indice de 5: ',i)
lista.insert(0,lista.pop(3))



print(lista)