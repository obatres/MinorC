class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  exp, linea=0 , columna=0 ) :
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Mientras(Instruccion) :
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self,tipo, listaid,linea=0 , columna=0) :
        self.tipo = tipo
        self.listaid = listaid
        self.linea = linea
        self.columna = columna

class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id,tipo, expNumerica,  linea=0 , columna=0) :
        self.id = id
        self.tipo = tipo
        self.expNumerica = expNumerica
        self.linea = linea
        self.columna = columna

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, exp, goto,  linea =0, columna=0) :
        self.exp = exp
        self.goto = goto
        self.linea = linea
        self.columna = columna

class IfSimple(Instruccion):
    '''
        Esta clase representa la instruccion if Simple
    '''

    def __init__(self, cond, bloqueSentenciasIf, linea, columna):
        self.cond = cond
        self.bloqueSentenciasIf = bloqueSentenciasIf
        self.linea = linea
        self.columna=columna
        
class IfAnidado(Instruccion):
    '''
        Esta clase representa la instruccion if anidado
    '''
    def __init__(self, IfIni, listaif, linea, columna):
        self.IfIni = IfIni
        self.listaif = listaif
        self.linea = linea
        self.columna=columna

class IfAnidadoElse(Instruccion):
    '''
        Esta clase representa la instruccion if anidado y un else
    '''
    def __init__(self, IfIni, listaif, instelse, linea, columna):
        self.IfIni = IfIni
        self.listaif = listaif
        self.instelse = instelse
        self.linea = linea
        self.columna=columna

class IfElse(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, ifinst, elseinst, linea, columna) :
        self.ifinst = ifinst
        self.elseinst = elseinst
        self.linea = linea
        self.columna=columna

class Else(Instruccion):
    '''
        Esta clase representa el bloque de sentencias de una instruccion else
    '''

    def __init__(self, bloqueSentenciasElse, linea =0, columna=0):
        self.bloqueSentenciasElse = bloqueSentenciasElse
        self.linea=linea
        self.columna=columna

class Unset(Instruccion):
    '''
        Esta clase representa la instrucción unset.
        La instrucción unset únicamente tiene como parámetro un registro
    '''

    def __init__(self,  exp,  linea =0, columna=0) :
        self.exp = exp    
        self.linea = linea
        self.columna = columna

class Return(Instruccion):
    '''
        Esta clase representa la instrucción return
    '''

    def __init__(self,  exp=0,  linea =0, columna=0) :
        self.exp = exp    
        self.linea = linea
        self.columna = columna

class Continue(Instruccion):
    '''
        Esta clase representa la instrucción return
    '''
    def __init__(self,  linea =0, columna=0) :   
        self.linea = linea
        self.columna = columna

class Break(Instruccion):
    '''
        Esta clase representa la instrucción break
    '''
    def __init__(self,  linea =0, columna=0) :   
        self.linea = linea
        self.columna = columna

class AsignaPunteroPila(Instruccion):
    '''
        Asigna puntero de  una pila
    '''
    def __init__(self,  id, exp,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp 
        self.linea = linea
        self.columna = columna

class AsignaValorPila(Instruccion):
    '''
        Asigna un valor a una posicion de  una pila
    '''
    def __init__(self,  id, exp, puntero,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp
        self.puntero = puntero 
        self.linea = linea
        self.columna = columna

class AsignacionExtra(Instruccion):
    '''
        Asigna un valor a un registro parametro, ra y retorno
    '''
    def __init__(self,  id, exp,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Main (Instruccion):
    '''
        Nodo de tipo main
   
    '''
    def __init__(self, sentencias, linea=0 , columna=0) :
        self.sentencias=sentencias
        self.linea = linea
        self.columna = columna

class Asigna_arreglo(Instruccion):
    '''
        Nodo de tipo asignacion de arreglo
   
    '''
    def __init__(self,id,lista,exp,  linea=0 , columna=0) :
        self.id = id 
        self.lista = lista
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Label(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id,  linea=0 , columna=0) :
        self.id = id 
        self.linea = linea
        self.columna = columna

class Goto(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id,  linea=0 , columna=0) :
        self.id = id 
        self.linea = linea
        self.columna = columna

class Exit():
    '''
        Nodo de tipo Exit
   
    '''
    def __init__(self,  linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna

class Read():
    '''
        Nodo de tipo Read
   
    '''
    def __init__(self,  linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna

class DefinicionConvalor():
    '''
        Nodo de tipo definicion de un id simple o un arreglo, con valor inicial
   
    '''
    def __init__(self,id,exp,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp
        self.linea = linea
        self.columna = columna

class DefinicionSinValor():
    '''
        Nodo de tipo definicion de un id simple o un arreglo, sin valor inicial
   
    '''
    def __init__(self,id,  linea=0 , columna=0) :
        self.id = id 
        self.linea = linea
        self.columna = columna

class Incremento(Instruccion):
    '''
        Esta clase representa la funcion incremento o decremento
    '''

    def __init__(self, exp, tipo,  linea =0, columna=0) :
        self.exp=exp   
        self.tipo=tipo 
        self.linea = linea
        self.columna = columna

class inc ():
    def __init__(self, exp, tipo,  linea =0, columna=0) :
        self.exp=exp   
        self.tipo=tipo 
        self.linea = linea
        self.columna = columna

class While(Instruccion):
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, condicion, instrucciones,linea =0, columna=0) :
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

class DefinicionFuncion(Instruccion):
    '''
        Esta clase representa la instrucción definicion de una funcion
    '''

    def __init__(self, id, parametros, sentencias,linea =0, columna=0) :
        self.id = id
        self.parametros = parametros
        self.sentencias = sentencias
        self.linea = linea
        self.columna = columna   

class ParametroDefinicionFuncion():
    '''
        Esta clase representa la un parametro
        dentro de la lista de parametros aceptados
        en la definicion de una funcion
    '''

    def __init__(self, tipo, exp,linea =0, columna=0) :
        self.tipo = tipo
        self.exp = exp
        self.linea = linea
        self.columna = columna   