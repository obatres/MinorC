

lista = "prueba:	print($a0);	goto Label0; main: goto hola; Label1: print(\"ASDs\");"

nuevo =lista.split("main:",1)
print("main:",nuevo[1:][0])
print(nuevo[:-1][0])
