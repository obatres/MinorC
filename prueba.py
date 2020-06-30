import re 


lista = "as aS as aS As as As label: hola adios main: 1 2 2 3 4 5 6"

nuevo =lista.split("main:",1)

print(nuevo[1:])
print(nuevo[:1])