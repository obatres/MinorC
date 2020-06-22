#-------------------------------------------------ANALIZADOR LEXICO
reservadas = {
    'numero' : 'NUMERO',
    'imprimir' : 'IMPRIMIR',
    'mientras' : 'MIENTRAS',
    'if' : 'IF',
    'else' : 'ELSE',
    'main' : 'MAIN',
    'goto':'GOTO',
    'unset':'UNSET',
    'printf':'PRINT',
    'scanf':'SCAN',
    'read':'READ',
    'exit':'EXIT',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'array':'ARRAY',
    'abs':'ABS',
    'xor':'XORLOG',
    'auto':'AUTO',
    'break':'BREAK',
    'case':'CASE',
    'continue':'CONTINUE',
    'default':'DEFAULT',
    'do':'DO',
    'double':'DOUBLE',
    'enum':'ENUM',
    'for':'FOR',
    'extern':'EXTERN',
    'register':'REGISTER',
    'return':'RETURN',
    'sizeof':'SIZEOF',
    'struct':'STRUCT',
    'switch':'SWITCH',
    'void':'VOID',
    'while':'WHILE',
    'void':'VOID'
}

tokens  = [
    'PTCOMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ANDBIT',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'RES',
    'DOSP',
    'TEMPORAL',
    'NOTLOG',
    'ANDLOG',
    'ORLOG',
    'NOTBIT',
    'ORBIT',
    'XORBIT',
    'IZQBIT',
    'DERBIT',
    'MAYORIG',
    'MENORIG',
    'LABEL',
    'PTEMPORAL',
    'CADE',
    'CORIZQ',
    'CORDER',
    'PILAPOS',
    'PILAPUNTERO',
    'VALORDEVUELTO',
    'DIRRETORNO',
    'MASIGUAL',
    'MENOSIGUAL' ,
    'PORIGUAL' , 
    'DIVIGUAL' , 
    'RESIGUAL' , 
    'IZQIGUAL' ,
    'DERIGUAL' , 
    'ANDIGUAL' , 
    'NOTIGUAL' , 
    'ORIGUAL',
    'INTERRO',
    'COMA'

    
    
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MASIGUAL  = r'\+='
t_MENOSIGUAL = r'-='
t_PORIGUAL  = r'\*='
t_DIVIGUAL  = r'/='
t_RESIGUAL  = r'%='
t_IZQIGUAL  = r'<<='
t_DERIGUAL  = r'>>='
t_ANDIGUAL  = r'&='
t_NOTIGUAL  = r'\^='
t_ORIGUAL   = r'\|='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_RES       = r'%'
t_MAYORIG   = r'>='
t_MENORIG   = r'<='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_DOSP      = r':'
t_NOTLOG    = r'!'
t_ANDLOG    = r'&&'
t_ORLOG     = r'\|\|'
t_NOTBIT    = r'~'
t_ANDBIT    = r'&'
t_ORBIT     = r'\|'
t_XORBIT    = r'\^'
t_IZQBIT    = r'<<'
t_DERBIT    = r'>>'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_INTERRO   = r'\?'
t_COMA      = r','


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t



def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADE(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple #...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\"\r\'"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
#OBTENIENDO LA COLUMNA 
def get_clomuna(input, token):
    #try:
        line_star = input.rfind('\n', 0 ,token.lexpos) + 1
        return (token.lexpos - line_star)+1
    #except :
     #   return 0
     #     
def t_error(t):
    print("Error Lexico en el token: '%s'" % t.value[0])
    err = "Error Lexico en el token: '%s'" % t.value[0]
    lista_errores.append(err)
    t.lexer.skip(1)





# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()



# Asociación de operadores y precedencia
precedence = (
    ('right','NOTLOG'),
    ('left','ANDLOG','ORLOG','XORLOG'),
    ('left','IGUALQUE','NIGUALQUE'),
    ('left','MENQUE','MAYQUE'),
    ('left','MAYORIG','MENORIG'),
    ('right','NOTBIT'),
    ('left','XORBIT'),
    ('left','ANDBIT','ORBIT'),
    ('left','IZQBIT','DERBIT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','RES','ABS'),
    ('right','UMENOS'),
    )

# Definición de la gramática
from graphviz import Digraph
from expresiones import *
from instrucciones import *

asc =[]

def p_init(t) :
    'init            : instrucciones'
    asc.append("init - instrucciones")
    t[0] = t[1]  

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    asc.append('instrucciones - instrucciones instruccion')
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]
    asc.append('instrucciones - instruccion')

def p_instruccion(t) :
    '''instruccion     : definicion_instr
                        | asignacion_instr
                        | STRUCTDEF
                        | FUNCION
                        | FUNCMAIN'''
    t[0] = t[1]
    if isinstance(t[1],Label): asc.append("instruccion - DEFINEL")
    elif isinstance(t[1],Imprimir): asc.append('instruccion - imprimir_instr')
    elif isinstance(t[1],Asignacion): asc.append('instruccion - asignacion_instr')
    elif isinstance(t[1],If): asc.append('instruccion - if_instr')
    elif isinstance(t[1],Main): asc.append('instruccion - INICIO')
    elif isinstance(t[1],Unset): asc.append('instruccion - UNSETF')
    elif isinstance(t[1],Exit): asc.append('instruccion - EXITF')
    elif isinstance(t[1],Asigna_arreglo): asc.append('instruccion - ASIGNAARREGLO')
    elif isinstance(t[1],IniciaPila): asc.append('instruccion - INICIAPILA')
    elif isinstance(t[1],AsignaPunteroPila): asc.append('instruccion - ASIGNAPUNTERO')
    elif isinstance(t[1],AsignaValorPila): asc.append('instruccion - ASIGNAPILA')
    elif isinstance(t[1],AsignacionExtra): asc.append('instruccion - ASIGNACIONEXTRA')
    elif isinstance(t[1],Goto): asc.append('instruccion - DEFINEGOTO')
    else:
        asc.append('instruccion - OTRO')

def p_funcion_main(t):
    'FUNCMAIN : TIPO_VAR MAIN PARIZQ PARDER BLOQUE '
def p_Label(t):
    'DEFINEL : ID DOSP'
    t[0] = Label(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('DEFINEL - ID DOSP')

def p_Goto(t):
    'DEFINEGOTO : GOTO ID PTCOMA'
    t[0] = Goto(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('DEFINEGOTO - GOTO ID PTCOMA')

#Recibe: print($t1);
def p_instruccion_imprimir(t) :
    'imprimir_instr     : PRINT PARIZQ expresion_log_relacional PARDER PTCOMA'
    t[0] =Imprimir(t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('imprimir_instr  - PRINT PARIZQ expresion_log_relacional PARDER PTCOMA')

def p_instruccion_definicion(t) :
    'definicion_instr   : TIPO_VAR LISTAID PTCOMA'
    #t[0] =Definicion(t[2])

def p_lista_id(t):
    'LISTAID : LISTAID COMA IDDECLA'
    t[1].append(t[2])
    t[0]=t[1]

def  p_id_de_lista(t):
    'LISTAID : IDDECLA'
    t[0]=[t[1]]

def p_id_decla(t):
    'IDDECLA  : IDT'
    t[0]=t[1]
    
def p_id_decla2(t):
    'IDDECLA  : IDT IGUAL expresion_log_relacional'
    t[0]=t[1]

def p_idt_1(t):
    'IDT : ID'

def p_idt_2(t):
    'IDT : ID LIND'

def p_lista_indices(t):
    'LIND : LIND IND'

def p_lista_indice(t):
    'LIND : IND'

def p_indice_vacio(t):
    'IND : CORIZQ CORDER'

def p_indice_lleno(t):
    'IND : CORIZQ expresion_log_relacional CORDER ' 

def p_struct_definicion(t):
    'STRUCTDEF : STRUCT ID LLAVIZQ IDSTRUCT  LLAVDER PTCOMA'

def p_lista_id_struct(t):
    'IDSTRUCT : IDSTRUCT TIPO_VAR ID PTCOMA'
    t[1].append(t[3])
    t[0] = t[1]
def p_id_struct_def(t):
    'IDSTRUCT :  TIPO_VAR ID PTCOMA'
    t[0]=[t[2]]

def p_tipo_variable(t):
    '''TIPO_VAR :  INT
                | DOUBLE
                | FLOAT
                | CHAR
                | VOID'''

def p_asignacion_instr(t) :
    'asignacion_instr   : ID TIPO_AS expresion_log_relacional PTCOMA'
    #t[0] =Asignacion(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('asignacion_instr   : TEMPORAL IGUAL expresion_log_relacional PTCOMA')

def p_tipo_asigna(t):
    '''TIPO_AS :  IGUAL
                | MASIGUAL
                | MENOSIGUAL
                | PORIGUAL  
                | DIVIGUAL  
                | RESIGUAL  
                | IZQIGUAL  
                | DERIGUAL  
                | ANDIGUAL  
                | NOTIGUAL  
                | ORIGUAL   '''
                
def p_Funcion(t):
    'FUNCION : TIPO_VAR ID PARIZQ PARAMETROS PARDER BLOQUE'

def p_Funcion_parametros(t):
    'PARAMETROS : PARAMETROS COMA PARAMETRO'

def p_Funcion_parametros_1(t):
    'PARAMETROS : PARAMETRO'

def p_Parametro(t):
    'PARAMETRO : TIPO_VAR ID'

def p_Parametro_vacio(t):
    'PARAMETRO : '

def p_bloque(t):
    '''BLOQUE : LLAVIZQ SENTENCIAS LLAVDER
                | SENTENCIAS'''

def p_Sentencias(t):
    'SENTENCIAS : SENTENCIAS SENTENCIA'

def p_Sentencias_sentencias(t):
    'SENTENCIAS : SENTENCIA'

def p_Sentencia(t):
    '''SENTENCIA :    definicion_instr 
                    | asignacion_instr
                    | imprimir_instr
                    | DEFINEL
                    | DEFINEGOTO
                    | IFFUN
                    | SWITCHFUN
                    | BREAKF
                    | WHILEF
                    '''

def p_while_fun(t):
    'WHILEF : WHILE expresion_numerica LLAVIZQ SENTENCIAS LLAVDER'
    print("reconoce while")
def p_switch_fun(t):
    'SWITCHFUN : SWITCH expresion_numerica LLAVIZQ LISTACASE LLAVDER'
    
def p_listacase(t):
    'LISTACASE : LISTACASE CASES '

def p_listacase_case(t):
    'LISTACASE : CASES'

def p_cases_case(t):
    'CASES : CASE expresion_log_relacional DOSP SENTENCIAS'

def p_cases_def(t):
    'CASES : DEFAULT DOSP SENTENCIAS'

def p_break(t):
    'BREAKF : BREAK PTCOMA'

def p_instrucciones_if(t):
    '''IFFUN :   if_instr
            | if_instr LISTA_ELSEIF
            | if_instr LISTA_ELSEIF else_instr
            | if_instr else_instr'''

def p_if_instr(t) :
    'if_instr           : IF expresion_numerica BLOQUE'
    #t[0] =If(t[2], t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('if_instr  - IF expresion_numerica DEFINEGOTO')

def p_lista_else_if(t):
    'LISTA_ELSEIF : LISTA_ELSEIF if_else_instr'

def p_lista_else_if_1(t):
    'LISTA_ELSEIF : if_else_instr'

def p_if_else_instr(t) :
    'if_else_instr      : ELSE if_instr '

def p_else_instr(t):
    'else_instr : ELSE BLOQUE'

#RECIBE: expresiones aritmeticas y bit a bit
def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        | expresion_numerica RES expresion_numerica
                        | expresion_numerica ANDBIT expresion_numerica
                        | expresion_numerica ORBIT expresion_numerica
                        | expresion_numerica XORBIT expresion_numerica
                        | expresion_numerica IZQBIT expresion_numerica
                        | expresion_numerica DERBIT expresion_numerica'''
    if t[2] == '+'  : 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica MAS expresion_numerica')
    elif t[2] == '-': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica MENOS expresion_numerica')
    elif t[2] == '*': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica POR expresion_numerica')
    elif t[2] == '/': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica DIVIDIDO expresion_numerica')
    elif t[2] == '%': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.RESIDUO,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica RES expresion_numerica')
    elif t[2] == '&': 
        t[0] = ExpresionBitAnd(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica ANDBIT expresion_numerica')
    elif t[2] == '|': 
        t[0] = ExpresionBitOr(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica ORBIT expresion_numerica')
    elif t[2] == '^': 
        t[0] = ExpresionBitXor(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica XORBIT expresion_numerica')
    elif t[2] == '<<': 
        t[0] = ExpresionBitIzq(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica IZQBIT expresion_numerica')
    elif t[2] == '>>': 
        t[0] = ExpresionBitDer(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_numerica - expresion_numerica DERBIT expresion_numerica')

def p_expresion_bit_not(t):
    'expresion_numerica : NOTBIT expresion_numerica'
    t[0] = ExpresionBitNot(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - NOTBIT expresion_numerica')

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - MENOS expresion_numerica UMENOS')

#Recibe (Expresion)
def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_log_relacional PARDER'
    t[0] = t[2]
    asc.append('expresion_numerica - PARIZQ expresion_log_relacional PARDER')

def p_expresion_number(t):
    '''expresion_numerica : ENTERO  '''
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.INT,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ENTERO ')

def p_expresion_decimal(t):
    'expresion_numerica : DECIMAL'
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.FLOAT,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - DECIMAL ')

def p_expresion_id(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionNumero(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ID ')

#recibe: cadena 'hola'
def p_expresion_cadena(t) :
    'expresion_numerica     : CADENA'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - CADENA ')
#recibe: cadena "hola"
def p_expresion_cade(t) :
    'expresion_numerica     : CADE'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - CADE ')
#recibe: read()
def p_expresion_read(t):
    'expresion_numerica : READ PARIZQ PARDER'
    t[0] = Read (t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - READ PARIZQ PARDER ')

def p_inicializacion_array(t):
    'expresion_numerica : ARRAY PARIZQ PARDER'
    t[0]= InicioArray(t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ARRAY PARIZQ PARDER')

def p_acceso_array_expresion(t):
    'expresion_numerica : TEMPORAL ACCESO'
    t[0] = AccesoValorArray(t[1],t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - TEMPORAL ACCESO')

def p_acceso_lista_array(t):
    'ACCESO : ACCESO CORIZQ expresion_numerica CORDER'
    t[1].append(t[3])
    t[0] = t[1]
    asc.append('ACCESO - ACCESO CORIZQ expresion_numerica CORDER')

def p_acceso_array(t):
    'ACCESO : CORIZQ expresion_numerica CORDER '
    t[0] = [t[2]]
    asc.append('ACCESO - CORIZQ expresion_numerica CORDER ')

#recibe: conversiones TIPOCONVERSION $t1 
def p_expresion_conversion(t):
    'expresion_numerica : TIPOCONVERSION expresion_numerica'
    t[0] = ExpresionConversion(t[1],t[2],t.lineno(1),0)
    asc.append('expresion_numerica - TIPOCONVERSION expresion_numerica ')
#recibe: tipo de conversion (int) (float) (char)
def p_expresion_tipoConversion(t):
    '''TIPOCONVERSION : PARIZQ INT PARDER
                    | PARIZQ FLOAT PARDER
                    | PARIZQ CHAR PARDER '''
    t[0]=t[2]
    asc.append('TIPOCONVERSION  - PARIZQ TIPOC PARDER ')
#Recibe: valor absoluto
def p_expresion_valorabs(t):
    'expresion_numerica : ABS PARIZQ expresion_numerica PARDER'
    t[0] =  ExpresionValorAbsoluto(t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ABS PARIZQ expresion_numerica PARDER ')
#Recibe expresiones logicas y relacionales
def p_expresion_log_relacional(t) :
    '''expresion_log_relacional : expresion_numerica MAYQUE expresion_numerica
                            | expresion_numerica MENQUE expresion_numerica
                            | expresion_numerica IGUALQUE expresion_numerica
                            | expresion_numerica NIGUALQUE expresion_numerica
                            | expresion_numerica MAYORIG expresion_numerica
                            | expresion_numerica MENORIG expresion_numerica
                            | expresion_log_relacional ANDLOG expresion_log_relacional
                            | expresion_log_relacional ORLOG expresion_log_relacional
                            | expresion_log_relacional XORLOG expresion_log_relacional'''
    if t[2] == '>'    : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica MAYQUE expresion_numerica')
    elif t[2] == '<'  : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENOR_QUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica MENQUE expresion_numerica')
    elif t[2] == '==' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.IGUAL,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica IGUALQUE expresion_numerica')
    elif t[2] == '!=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.DIFERENTE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica NIGUALQUE expresion_numerica')
    elif t[2] == '>=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYORQUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica MAYORIG expresion_numerica')
    elif t[2] == '<=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENORQUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica MENORIG expresion_numerica')
    elif t[2] == 'xor' :
        t[0] = ExpresionLogicaXOR(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica XOR expresion_numerica') 
    elif t[2] == '&&' : 
        t[0] = ExpresionLogicaAND(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica ANDLOG expresion_numerica') 
    elif t[2] == '||' : 
        t[0] = ExpresionLogicaOR(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion_log_relacional : expresion_numerica ORLOG expresion_numerica') 

#RECIBE !$t3
def p_expresion_logica_not(t):
    'expresion_log_relacional : NOTLOG expresion_log_relacional'
    t[0] = ExpresionLogicaNot(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_log_relacional - NOTLOG expresion_log_relacional') 
#Sintetiza la expresion de expresion_log_relacional
def p_expresion_expresionnumerica(t):
    'expresion_log_relacional :  expresion_numerica'
    t[0]=t[1]
    asc.append('expresion_log_relacional -  expresion_numerica') 

def p_error(t):
     # Read ahead looking for a terminating ";"
    while True:
         tok = pars.token() 
                     # Get the next token
         if not tok or tok.type == 'PTCOMA': break
    pars.errok()
    err = "Error en el token \'" + str(t.value) +"\' en la linea: "+ str(t.lineno) + ' de tipo: SINTACTICO'
    lista_errores.append(err)
    print("Error sintactico en el token ",t.value,t.lineno)
     # Return SEMI to the parser as the next lookahead token
    return tok 
    #print(t)
    #print("Error sintáctico en '%s'" % t.value,'> ',str(t.lineno))
  
 

import ts as TS
import ply.yacc as yacc
parser = yacc.yacc()
pars = yacc.yacc()
lista_errores = []
entry = ''
def parse(input) :
    global entry
    entry = input
    return pars.parse(input)

def retornalista():
    return lista_errores

def verGramatica():
    return asc