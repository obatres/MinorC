import ts as TS
import sys
from expresiones import *
from instrucciones import *
from graphviz import Digraph
from ts import TIPO_DATO as td
from _pydecimal import Decimal
import copy
import re


class Ejecucion_MinorC ():
    
#----------------------------------------VARIABLES GLOBALES
    ts_global = TS.TablaDeSimbolos()
    gram = []
    instrucciones=[]
    errores= []
    dot = Digraph('AST',filename='AST')
    resultado = ''
    true = 1
    false = 0
    Etiqueta = ''
    CodigoGenerado=''
    cont = 0
    contLabel=0
    contPar =0
    contRet =0
    salidaParcial=''
    salidaTotal =''
    Global=''
#--------------------------------------METODOS/FUNCIONES DE EJECUCION EN INTERFAZ
    def ejecutar_asc(self, input):
        import gramaticaM as g
        #self.gram = g.verGramatica()
        self.instrucciones = g.parse(input) 
        #print(self.instrucciones)

        self.procesar_instrucciones(self.instrucciones, self.ts_global)   
        self.salidaParcial =self.CodigoGenerado.split("main:",1)
        self.salidaTotal+="main:"+"\n"
        self.salidaTotal+=self.Global
        self.salidaTotal +=self.salidaParcial[1:][0]
        self.salidaTotal +=self.salidaParcial[:-1][0]
    
    def GenerarAST(self):
        try:
            DibujarAST(self.instrucciones)
            dot.view()
        except :
            print('error al imprimir arbol')
            pass

    def errores_asc(self):
        import gramaticaM as g
        self.errores = g.retornalista()
        return self.errores 

    def RecibirSalida(self):
        nuevo = copy.copy(self.CodigoGenerado)
        return nuevo

    def ejecutar_debug(self,input,i):
        import gramaticaM as l
        try:
            self.gram = l.verGramatica()
            self.instrucciones = l.parse(input) 
            procesar_instrucciones_debugger(self.instrucciones,self.ts_global,i)
        except :
            print('sad')
            #s = M()
            #s.OkMessage()
            #s.cerrar()
#----------------------------------------------------------------------REPORTES
    def ReporteGramatical(self):
        generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'2\'>REPORTE GRAMATICAL</td></tr><tr><td>No.</td><td>Producciones</td></tr>'
        cont = 0

        aux = list(reversed(self.gram))
        for i in aux:
            generado += '<tr><td>'+str(cont)+'</td><td align = \'left\'>'+str(i)+'</td></tr>'
            cont +=1
        generado +=' </table>>'

        dotTS = Digraph('Reporte Gramatical',filename='ReporteGramatical')

        dotTS.attr('node',shape='plaintext')
        dotTS.node('node',label=generado)
        dotTS.view()
    
    def GenerarAST(self):
        try:
            self.DibujarAST(self.instrucciones)
            self.dot.view()
        except :
            print('error al imprimir arbol')
            pass

    def ReporteErrores(self):
        generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'2\'>LISTADO DE ERRORES</td></tr><tr><td>No.</td><td>Error</td></tr>'
        cont = 0

        for i in self.errores:
            generado +='<tr><td>'+str(cont)+'</td><td>'+str(i)+'</td></tr>'
            cont +=1
        
        generado +=' </table>>'
        dotErr = Digraph('Errores',filename='ListadoDeErrores')
        dotErr.attr('node',shape='plaintext')
        dotErr.node('node',label=generado)
        dotErr.view()

    def ReporteTS(self):
        generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'5\'>TABLA DE SIMBOLOS</td></tr><tr><td>No.</td><td>identificador</td><td>valor</td><td>tipo</td><td>Etiqueta</td></tr>'
        cont = 0

        for i in self.ts_global.simbolos:
            generado += '<tr><td>'+str(cont)+'</td><td>'+str(self.ts_global.obtener(i).id)+'</td><td>'+str(self.ts_global.obtener(i).valor)+'</td><td>'+str(self.ts_global.obtener(i).tipo.name)+'</td><td>'+str(self.ts_global.obtener(i).amb)+'</td></tr>'
            cont +=1
        generado +=' </table>>'

        dotTS = Digraph('Tabla de simbolos',filename='TablaSimbolos')
        #print(generado)
        dotTS.attr('node',shape='plaintext')
        dotTS.node('node',label=generado)
        dotTS.view()
#--------------------------------------------------------------------DIBUJAR ARBOL
    def dibujar_exit(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Exit')
        self.dot.edge(root, nodo)

        return cont

    def dibujar_Goto(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Goto')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)
        return cont

    def dibujar_Label(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Etiqueta')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)
        return cont

    def dibujar_Asigna_arreglo(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'AsignaArreglo')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)

        self.dot.node(nodo1,instr.id)
        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,"acceso")
        self.dot.edge(nodo,nodo2)

        for i in instr.lista:
            cont = self.dibujar_expresion(i,nodo2,cont)
        cont = self.dibujar_expresion(instr.exp,nodo,cont)
        return cont  

    def dibujar_main(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Main')
        self.dot.edge(root, nodo)


        cont=cont+1
        nodo3 = 'nodo'+ str(cont)
        self.dot.node(nodo3,"Sentencias Main")
        self.dot.edge(nodo, nodo3)
        #BLOQUE DE SENTENCIAS

        cont = self.dibujar_Sentencias(instr.sentencias,nodo3,cont)

        return cont

    def dibujar_funcion(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Metodo/Fun')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)
        
        cont=cont+1
        nodo2 = 'nodo'+ str(cont)
        self.dot.node(nodo2,"Parametros")
        self.dot.edge(nodo, nodo2)
        for par in instr.parametros:
            if par.tipo!=0:
                cont=cont+1
                nodo1 = 'nodo'+ str(cont)
                self.dot.node(nodo1,str(par.tipo.name))
                self.dot.edge(nodo2, nodo1)
                cont=cont+1
                nodo1 = 'nodo'+ str(cont)
                self.dot.node(nodo1,str(par.exp))
                self.dot.edge(nodo2, nodo1)

        cont=cont+1
        nodo3 = 'nodo'+ str(cont)
        self.dot.node(nodo3,"Sentencias")
        self.dot.edge(nodo, nodo3)

        #BLOQUE DE SENTENCIAS
        return cont 
    

    def dibujar_Sentencias(self,instr, root,cont):

        for sent in instr:
            if isinstance(sent,Imprimir): cont = self.dibujar_print(sent,root,cont)
        return cont

    def dibujar_AsignaRegistro(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'AsignaRegistro')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

        return cont

    def dibujar_AsignaValorPila(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'AsignaValorPila')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)

        cont=cont+1
        nodo2 = 'nodo'+ str(cont)
        self.dot.node(nodo2,str(instr.puntero))
        self.dot.edge(nodo, nodo2)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)
        return cont

    def dibujar_AsignaPunteroPila(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'AsignaPunteroPila')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

        return cont

    def dibujar_unset(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Unset')
        self.dot.edge(root, nodo)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

        return cont

    def dibujar_IniciaPila(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'IniciaPila')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,str(instr.id))
        self.dot.edge(nodo, nodo1)
        return cont

    def dibujar_if(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'If')
        self.dot.edge(root, nodo)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

        cont= self.dibujar_Goto(instr.goto,nodo,cont)

        return cont

    def dibujar_asignacion(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Asignacion')
        self.dot.edge(root, nodo)
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.id.id)
        self.dot.edge(nodo,nodo1)
        
        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,str(instr.tipo))
        self.dot.edge(nodo,nodo2)

        cont = self.dibujar_expresion(instr.expNumerica,nodo,cont)
        return cont

    def dibujar_definicion(self,instr,root,cont):
        cont = cont+1
        nodo = 'nodo'+str(cont)
        self.dot.node(nodo,'Definicion')
        self.dot.edge(root, nodo)
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.tipo.name)
        self.dot.edge(nodo,nodo1)

        for d in instr.listaid:
            if isinstance (d,DefinicionSinValor): cont = self.dibujar_definicion_sinValor(d,nodo,cont)
            elif isinstance(d,DefinicionConvalor): cont = self.dibujar_definicion_conValor(d,nodo,cont)   
       
        return cont

    def dibujar_definicion_sinValor(self,instr,root,cont):
        cont = cont+1
        nodo = 'nodo'+str(cont)
        self.dot.node(nodo,'SinValor')
        self.dot.edge(root, nodo)
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,str(instr.id.id))
        self.dot.edge(nodo,nodo1)

        return cont

    def dibujar_definicion_conValor(self,instr,root,cont):
        cont = cont+1
        nodo = 'nodo'+str(cont)
        self.dot.node(nodo,'ConValor')
        self.dot.edge(root, nodo)
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,str(instr.id.id))
        self.dot.edge(nodo,nodo1)

        if not isinstance(instr.exp,list):
            cont = self.dibujar_expresion(instr.exp,nodo,cont)
        else:
            for i in instr.exp:
                if isinstance(i,list):
                        for j in i:
                            cont=self.dibujar_expresion(j,nodo,cont)
                else:
                    cont=self.dibujar_expresion(i,nodo,cont)

        return cont
    
    def dibujar_incremento(self, instr, root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Incre/decre')
        self.dot.edge(root, nodo)
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.exp)
        self.dot.edge(nodo,nodo1)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,instr.tipo)
        self.dot.edge(nodo,nodo2)
        return cont

    def dibujar_def_struct(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Def Struct')
        self.dot.edge(root, nodo)

        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.ide)
        self.dot.edge(nodo,nodo1)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,'elementos')
        self.dot.edge(nodo,nodo2)

        for i in instr.elementos:
            cont = self.dibujar_elemento_struct(i,nodo2,cont)

        return cont

    def dibujar_elemento_struct(self,instr,root,cont):
        cont = cont +1
        nodo3= 'nodo'+str(cont)
        self.dot.node(nodo3,instr.tipo.name)
        self.dot.edge(root,nodo3)

        
        for i in instr.ide:
            cont = cont +1
            nodo1= 'nodo'+str(cont)
            self.dot.node(nodo1,i.id.id)
            self.dot.edge(nodo3,nodo1)
        return cont

    def dibujar_decla_struct(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Decla Struct')
        self.dot.edge(root, nodo)

        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.TipoStruct)
        self.dot.edge(nodo,nodo1)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,instr.ide)
        self.dot.edge(nodo,nodo2)
        return cont

    def dibujar_decla_struct_arr(self,instr, root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Decla Struct Arr')
        self.dot.edge(root, nodo)

        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.TipoStruct)
        self.dot.edge(nodo,nodo1)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,instr.ide)
        self.dot.edge(nodo,nodo2)
        return cont

    def dibujar_asignacion_struct(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Asig Struct')
        self.dot.edge(root, nodo)

        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.TipoStruct)
        self.dot.edge(nodo,nodo1)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,instr.ide)
        self.dot.edge(nodo,nodo2)

        cont = self.dibujar_expresion(instr.valor,nodo,cont)
        return cont
    
    def dibujar_asignacion_struct_arr(self,instr, root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Asig Struct Arr')
        self.dot.edge(root, nodo)

        cont = cont +1
        nodo1= 'nodo'+str(cont)
        self.dot.node(nodo1,instr.Struct)
        self.dot.edge(nodo,nodo1)

        cont = self.dibujar_expresion(instr.indice,nodo,cont)

        cont = cont +1
        nodo2= 'nodo'+str(cont)
        self.dot.node(nodo2,instr.ide)
        self.dot.edge(nodo,nodo2)

        cont = self.dibujar_expresion(instr.valor,nodo,cont)
        return cont
    
    def dibujar_print(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Print')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,'expresiones print')
        self.dot.edge(root, nodo1)
        for i in instr.exp:
            cont = self.dibujar_expresion(i,nodo1,cont)

        return cont

    def dibujar_expresion(self,instr,root,cont):
        cont +=1
        nodo = 'nodo'+str(cont)
        self.dot.node(nodo,'Exp')
        self.dot.edge(root,nodo)
        
        cont = cont +1
        nodo1= 'nodo'+str(cont)
        
        if isinstance(instr,ExpresionNumero):
            self.dot.node(nodo1,str(instr.val))  
        elif isinstance(instr, ExpresionTemporal):  
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr,ExpresionId):
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr,ExpresionBinaria):    
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,str(instr.operador.name))
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionNegativo):
            self.dot.node(nodo1,'-')
            cont = self.dibujar_expresion(instr.exp,nodo1,cont)
        elif isinstance(instr,ExpresionBitNot):
            self.dot.node(nodo1,'~')
            cont = self.dibujar_expresion(instr.exp,nodo1,cont)
        elif isinstance(instr,ExpresionBitAnd):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'And bit')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionBitOr):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Or bit')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionBitXor):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Xor bit')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionBitIzq):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Corr Izq')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionBitDer):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Corr Der')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)     
        elif isinstance(instr, ExpresionPila):  
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr, ExpresionPunteroPila):  
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr, Expresion_Pop_pila):  
            self.dot.node(nodo1,instr.idPila)
            self.dot.node(nodo1,instr.puntero)
        elif isinstance(instr, InicioArray):
            self.dot.node(nodo1,"Inicia Array") 
        elif isinstance(instr, ExpresionValorAbsoluto):
            self.dot.node(nodo1,'ABS')
            cont = self.dibujar_expresion(instr.exp,nodo1,cont) 
        elif isinstance(instr, ExpresionLogica):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,str(instr.operador.name))
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)
        elif isinstance(instr,ExpresionLogicaXOR):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Xor')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)  
        elif isinstance(instr,ExpresionLogicaAND):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'And')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)    
        elif isinstance(instr,ExpresionLogicaOR):
            cont = self.dibujar_expresion(instr.exp1,nodo1,cont) 
            self.dot.node(nodo1,'Or')
            cont = self.dibujar_expresion(instr.exp2,nodo1,cont)  
        elif isinstance(instr,ExpresionLogicaNot):
            self.dot.node(nodo1,'!')
            cont = dibujar_expresion(instr.exp,nodo1,cont)
        elif isinstance(instr,Expresion_param):
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr,AccesoValorArray):
            self.dot.node(nodo1,instr.id)
            cont = cont +1
            nodo2= 'nodo'+str(cont)
            self.dot.node(nodo2,"acceso")
            self.dot.edge(nodo,nodo2)

            for i in instr.lista:
                cont = self.dibujar_expresion(i,nodo2,cont)
        elif isinstance(instr,Read):
            self.dot.node(nodo1,"Read ( )") 
        elif isinstance(instr,ExpresionInicioSimple):
            self.dot.node(nodo1,instr.id)
        elif isinstance(instr,ExpresionAccesoStruct):
            self.dot.node(nodo1,instr.idPadre+"."+instr.idHijo)
        else:
            print(instr)
        self.dot.edge(nodo,nodo1)

        return cont

    def dibujar_return(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Return')
        self.dot.edge(root, nodo)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

        return cont

    def DibujarAST(self,instrucciones):
        cont = 1
        root = 'nodo'+ str(cont)
        self.dot.node(root, 'MINORC')
        for instr in instrucciones:
            if isinstance(instr, Definicion) : cont = self.dibujar_definicion(instr, root,cont)
            elif isinstance(instr, Asignacion) : cont = self.dibujar_asignacion(instr, root,cont)
            elif isinstance(instr, inc) : cont = self.dibujar_incremento(instr, root,cont)
            elif isinstance(instr, DefinicionFuncion) : cont = self.dibujar_funcion(instr, root,cont)
            elif isinstance(instr, DefStruct) : cont = self.dibujar_def_struct(instr, root,cont)
            elif isinstance(instr, DeclaracionStruct) : cont = self.dibujar_decla_struct(instr, root,cont)
            elif isinstance(instr, AsignacionStruct) : cont = self.dibujar_asignacion_struct(instr, root,cont)
            elif isinstance(instr, DeclaracionStructArr) : cont =self.dibujar_decla_struct_arr(instr, root,cont)
            elif isinstance(instr, AsignacionStructArray): cont= self.dibujar_asignacion_struct_arr(instr, root,cont)
            elif isinstance(instr, Return): cont = self.dibujar_return(instr, root,cont)
            elif isinstance(instr, Main): cont = self.dibujar_main(instr,root,cont)
            else : 
                print('')
        #print(dot.source)

#--------------------------------------------------------------------PROCESAR INSTRUCCIONES
    def procesar_imprimir(self,instr, ts) :

        try: 

            for i in instr.exp:
                res = self.resolver_expresion_aritmetica(i,ts)
                patronTemporal = re.compile('\$(t[0-9]+)')
                patronParametro = re.compile('\$[a]([0-9]+)')
                patronRetorno = re.compile('\$[r][a]')
                if not (patronTemporal.match(res) or patronParametro.match(res) or patronRetorno.match(res) ):

                    self.CodigoGenerado += '\t'+'print('+str(res)+');'+"\n" 
                else:
                    self.CodigoGenerado += '\t'+'print('+str(res)+');'+"\n"    
            #print(instr.exp)         
            #salida = self.resolver_expresion_aritmetica(instr.exp,ts)
            #self.CodigoGenerado += '\t'+'print('+str(salida)+');'+"\n"    
            return 
        except:
            print('error de impresion, valor o variabe no encontrados: ',instr.exp.id ) 
            print(instr.linea,instr.columna)
            err = 'Error de impresion, valor o variabe no encontrados: ',instr.exp.id ,'En la linea: ',instr.linea,'En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            self.errores.append(err)
            pass
    
    def resolver_registro(self,exp,ts):
        
        return ts.obtener(exp.id).valor

    def procesar_definicion(self,instr, ts) :
        tipoReg = instr.tipo
        
        for d in instr.listaid:
            if isinstance (d,DefinicionSinValor): self.procesar_definicion_sinValor(d,ts,tipoReg)
            elif isinstance(d,DefinicionConvalor): self.procesar_definicion_conValor(d,ts,tipoReg)
            
        return 

    def procesar_definicion_sinValor(self, instr, ts, tipo):
        temp = instr.id
        if isinstance (temp,ExpresionInicioSimple):
            registro =self.generarTemp()
            if tipo ==td.INT:
                nuevo = TS.Simbolo(temp.id,tipo,0,registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.CodigoGenerado += '\t' + registro + '= 0;'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.CodigoGenerado += '\t' + registro + '= 0;'+'\n'
                    ts.actualizar(nuevo)
            elif tipo == td.FLOAT:
                nuevo = TS.Simbolo(temp.id,tipo,0.0,registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.CodigoGenerado += '\t' + registro + '= 0.0;'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.CodigoGenerado += '\t' + registro + '= 0.0;'+'\n'
                    ts.actualizar(nuevo)
            elif tipo == td.CADENA:
                nuevo = TS.Simbolo(temp.id,tipo,"0",registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.CodigoGenerado += '\t' + registro + '= \'0 \';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.CodigoGenerado += '\t' + registro + '= \' 0\';'+'\n'
                    ts.actualizar(nuevo)
            else:
                print('Error, tipo '+str(tipo)+' no aplicable en la definicion')
        
        elif isinstance (temp,ExpresionListaIndices):
            
            if temp.listaindices[0]!=0:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,{},registro)
                self.CodigoGenerado += '\t'+registro+'='+'array()'+';'+'\n'
                dim=1
                ind=[]
                for i in temp.listaindices:
                    ind.append(self.resolver_expresion_aritmetica(i,ts))
                    dim *=self.resolver_expresion_aritmetica(i,ts)
                if tipo==td.INT:
                    for j in range(dim):
                        self.CodigoGenerado+='\t'+registro+"["+str(j)+"]"+"=0;"+"\n"
                elif tipo==td.FLOAT:
                    for j in range(dim):
                        self.CodigoGenerado+='\t'+registro+"["+str(j)+"]"+"=0.0;"+"\n"
                elif tipo==td.CADENA:
                    for j in range(dim):
                        self.CodigoGenerado+='\t'+registro+"["+str(j)+"]"+"=\'0\';"+"\n"
                nuevo.valor=ind
                ts.agregar(nuevo)
            else:
                print('Error, esta variable: '+temp.id+' debe contener un valor para ser inicializada')
            return
        else:
            print(type(instr.id))
        return
    
    def procesar_definicion_conValor(self,instr,ts,tipo):
        temp = instr.id
        if isinstance(temp,ExpresionInicioSimple):
            registro = self.generarTemp()
            valor  = self.resolver_expresion_aritmetica(instr.exp,ts)
            nuevo = TS.Simbolo(temp.id,tipo,valor,registro)
            if ts.existeSimbolo(nuevo)==False:
                self.CodigoGenerado += '\t' + registro + '='+str(valor)+';'+'\n'
                ts.agregar(nuevo)
            elif ts.existeSimbolo(nuevo)==True:
                self.CodigoGenerado += '\t' + registro + '='+str(valor)+';'+'\n'
                ts.actualizar(nuevo)
            return
        elif isinstance(temp,ExpresionListaIndices):            
            if temp.listaindices[0]==0:
                valor = self.resolver_expresion_aritmetica(instr.exp,ts)
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,valor,registro)
                if ts.existeSimbolo(nuevo) == False:
                    self.CodigoGenerado += '\t'+registro+ '='+str(valor)+';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.CodigoGenerado += '\t'+registro+ '='+str(valor)+';'+'\n'
                    ts.actualizar(nuevo)
                return
            elif temp.listaindices[0]!=0:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,{},registro)
                self.CodigoGenerado += '\t'+registro+'='+'array()'+';'+'\n'
                dim=1
                ind=[]
                for i in temp.listaindices:
                    ind.append(self.resolver_expresion_aritmetica(i,ts))
                    dim*=self.resolver_expresion_aritmetica(i,ts)
                valores=[]
                for j in instr.exp:
                    if isinstance(j,list):
                        for x in j:
                            valores.append(x)
                    else:
                        valores.append(j)
                if len(valores)==dim:
                    for k in range(dim):
                        val = self.resolver_expresion_aritmetica(valores[k],ts)
                        self.CodigoGenerado +='\t'+registro+"["+str(k)+"]="+str(val)+";"+"\n"
                nuevo.valor=ind
                ts.agregar(nuevo)
                return
            else:

                print('mas indices')
            return
        else:
            print(type(instr.id))
        return
#--------------------------------------------------------------------Definicion global
    def procesar_definicion_global(self,instr, ts) :
        tipoReg = instr.tipo
        
        for d in instr.listaid:
            if isinstance (d,DefinicionSinValor): self.procesar_definicion_sinValor_global(d,ts,tipoReg)
            elif isinstance(d,DefinicionConvalor): self.procesar_definicion_conValor_global(d,ts,tipoReg)
            
        return 

    def procesar_definicion_sinValor_global(self, instr, ts, tipo):
        temp = instr.id
        if isinstance (temp,ExpresionInicioSimple):
            registro =self.generarTemp()
            if tipo ==td.INT:
                nuevo = TS.Simbolo(temp.id,tipo,0,registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.Global += '\t' + registro + '= 0;'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.Global += '\t' + registro + '= 0;'+'\n'
                    ts.actualizar(nuevo)
            elif tipo == td.FLOAT:
                nuevo = TS.Simbolo(temp.id,tipo,0.0,registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.Global += '\t' + registro + '= 0.0;'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.Global += '\t' + registro + '= 0.0;'+'\n'
                    ts.actualizar(nuevo)
            elif tipo == td.CADENA:
                nuevo = TS.Simbolo(temp.id,tipo,"0",registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.Global += '\t' + registro + '= \' 0\';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.Global += '\t' + registro + '= \' 0\';'+'\n'
                    ts.actualizar(nuevo)
            else:
                print('Error, tipo '+str(tipo)+' no aplicable en la definicion')
        
        elif isinstance (temp,ExpresionListaIndices):
            
            if temp.listaindices[0]!=0:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,{},registro)
                self.Global += '\t'+registro+'='+'array()'+';'+'\n'
                dim=1
                ind=[]
                for i in temp.listaindices:
                    ind.append(self.resolver_expresion_aritmetica(i,ts))
                    dim *=self.resolver_expresion_aritmetica(i,ts)
                if tipo==td.INT:
                    for j in range(dim):
                        self.Global+='\t'+registro+"["+str(j)+"]"+"=0;"+"\n"
                elif tipo==td.FLOAT:
                    for j in range(dim):
                        self.Global+='\t'+registro+"["+str(j)+"]"+"=0.0;"+"\n"
                elif tipo==td.CADENA:
                    for j in range(dim):
                        self.Global+='\t'+registro+"["+str(j)+"]"+"=\'0\';"+"\n"
                nuevo.valor=ind
                ts.agregar(nuevo)
                return
            else:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,{},registro)
                if ts.existeSimbolo(nuevo) == False:
                    self.Global += '\t'+registro+ '='+"\' 0\'"+';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.Global += '\t'+registro+ '='+"\' 0\'"+';'+'\n'
                    ts.actualizar(nuevo)
                return
            return
        else:
            print(type(instr.id))
        return
    
    def procesar_definicion_conValor_global(self,instr,ts,tipo):
        temp = instr.id
        if isinstance(temp,ExpresionInicioSimple):
            registro = self.generarTemp()
            valor  = self.resolver_expresion_aritmetica(instr.exp,ts)
            nuevo = TS.Simbolo(temp.id,tipo,valor,registro)
            if ts.existeSimbolo(nuevo)==False:
                self.Global += '\t' + registro + '='+str(valor)+';'+'\n'
                ts.agregar(nuevo)
            elif ts.existeSimbolo(nuevo)==True:
                self.Global += '\t' + registro + '='+str(valor)+';'+'\n'
                ts.actualizar(nuevo)
            return
        elif isinstance(temp,ExpresionListaIndices):            
            if temp.listaindices[0]==0:
                valor = self.resolver_expresion_aritmetica(instr.exp,ts)
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,valor,registro)
                if ts.existeSimbolo(nuevo) == False:
                    self.Global += '\t'+registro+ '='+str(valor)+';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    self.Global += '\t'+registro+ '='+str(valor)+';'+'\n'
                    ts.actualizar(nuevo)
                return
            elif temp.listaindices[0]!=0:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,{},registro)
                self.Global += '\t'+registro+'='+'array()'+';'+'\n'
                dim=1
                ind=[]
                for i in temp.listaindices:
                    ind.append(self.resolver_expresion_aritmetica(i,ts))
                    dim*=self.resolver_expresion_aritmetica(i,ts)
                valores=[]
                for j in instr.exp:
                    if isinstance(j,list):
                        for x in j:
                            valores.append(x)
                    else:
                        valores.append(j)
                if len(valores)==dim:
                    for k in range(dim):
                        val = self.resolver_expresion_aritmetica(valores[k],ts)
                        self.Global +='\t'+registro+"["+str(k)+"]="+str(val)+";"+"\n"
                nuevo.valor=ind
                ts.agregar(nuevo)
                return
            else:

                print('mas indices')
            return
        else:
            print(type(instr.id))
        return

    def procesar_asignacion_global(self,instr, ts) :
        asi = instr.id
        if isinstance(asi,ExpresionInicioSimple):
            registro = ts.obtener(asi.id).reg
            valor  = self.resolver_expresion_aritmetica(instr.expNumerica,ts)
            try:
                if instr.tipo == "=":
                    self.Global += '\t'+registro+'='+str(valor)+';'+'\n'
                elif instr.tipo =="+=":
                    self.Global += '\t'+registro+'='+registro+'+'+str(valor)+';'+'\n'
                elif instr.tipo =="-=":
                    self.Global += '\t'+registro+'='+registro+'-'+str(valor)+';'+'\n'
                elif instr.tipo =="*=":
                    self.Global += '\t'+registro+'='+registro+'*'+str(valor)+';'+'\n' 
                elif instr.tipo =="/=":
                    self.Global += '\t'+registro+'='+registro+'/'+str(valor)+';'+'\n'
                elif instr.tipo =="%=":
                    self.Global += '\t'+registro+'='+registro+'%'+str(valor)+';'+'\n'
                elif instr.tipo =="<<=":
                    self.Global += '\t'+registro+'='+registro+'<<'+str(valor)+';'+'\n'
                elif instr.tipo ==">>=":
                    self.Global += '\t'+registro+'='+registro+'>>'+str(valor)+';'+'\n'
                elif instr.tipo =="&=":
                    self.Global += '\t'+registro+'='+registro+'&'+str(valor)+';'+'\n'
                elif instr.tipo =="|=":
                    self.Global += '\t'+registro+'='+registro+'|'+str(valor)+';'+'\n'
                elif instr.tipo =="^=":
                    self.Global += '\t'+registro+'='+registro+'^'+str(valor)+';'+'\n'
            except :
                print("Error, no se puede realizar la traduccion de esta asignacion")   
        elif isinstance(asi,ExpresionListaIndices):
            iden =ts.obtener(asi.id).reg
            valor  = self.resolver_expresion_aritmetica(instr.expNumerica,ts)
            for r in asi.listaindices:
                iden +="["+str(self.resolver_expresion_aritmetica(r,ts))+"]"
            try:
                if instr.tipo == "=":
                    self.Global += '\t'+iden+'='+str(valor)+';'+'\n'
                elif instr.tipo =="+=":
                    self.Global += '\t'+iden+'='+iden+'+'+str(valor)+';'+'\n'
                elif instr.tipo =="-=":
                    self.Global += '\t'+iden+'='+iden+'-'+str(valor)+';'+'\n'
                elif instr.tipo =="*=":
                    self.Global += '\t'+iden+'='+iden+'*'+str(valor)+';'+'\n' 
                elif instr.tipo =="/=":
                    self.Global += '\t'+iden+'='+iden+'/'+str(valor)+';'+'\n'
                elif instr.tipo =="%=":
                    self.Global += '\t'+iden+'='+iden+'%'+str(valor)+';'+'\n'
                elif instr.tipo =="<<=":
                    self.Global += '\t'+iden+'='+iden+'<<'+str(valor)+';'+'\n'
                elif instr.tipo ==">>=":
                    self.Global += '\t'+iden+'='+iden+'>>'+str(valor)+';'+'\n'
                elif instr.tipo =="&=":
                    self.Global += '\t'+iden+'='+iden+'&'+str(valor)+';'+'\n'
                elif instr.tipo =="|=":
                    self.Global += '\t'+iden+'='+iden+'|'+str(valor)+';'+'\n'
                elif instr.tipo =="^=":
                    self.Global += '\t'+iden+'='+iden+'^'+str(valor)+';'+'\n'
            except:           
                pass
            
        return
       
#---------------------------------------------------------------------------------- 
    def procesar_asignacion(self,instr, ts) :
        asi = instr.id
        if isinstance(asi,ExpresionInicioSimple):
            registro = ts.obtener(asi.id).reg
            valor  = self.resolver_expresion_aritmetica(instr.expNumerica,ts)
            try:
                if instr.tipo == "=":
                    self.CodigoGenerado += '\t'+registro+'='+str(valor)+';'+'\n'
                elif instr.tipo =="+=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'+'+str(valor)+';'+'\n'
                elif instr.tipo =="-=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'-'+str(valor)+';'+'\n'
                elif instr.tipo =="*=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'*'+str(valor)+';'+'\n' 
                elif instr.tipo =="/=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'/'+str(valor)+';'+'\n'
                elif instr.tipo =="%=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'%'+str(valor)+';'+'\n'
                elif instr.tipo =="<<=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'<<'+str(valor)+';'+'\n'
                elif instr.tipo ==">>=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'>>'+str(valor)+';'+'\n'
                elif instr.tipo =="&=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'&'+str(valor)+';'+'\n'
                elif instr.tipo =="|=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'|'+str(valor)+';'+'\n'
                elif instr.tipo =="^=":
                    self.CodigoGenerado += '\t'+registro+'='+registro+'^'+str(valor)+';'+'\n'
            except :
                print("Error, no se puede realizar la traduccion de esta asignacion")   
        elif isinstance(asi,ExpresionListaIndices):
            iden =ts.obtener(asi.id).reg
            valor  = self.resolver_expresion_aritmetica(instr.expNumerica,ts)
            for r in asi.listaindices:
                iden +="["+str(self.resolver_expresion_aritmetica(r,ts))+"]"
            try:
                if instr.tipo == "=":
                    self.CodigoGenerado += '\t'+iden+'='+str(valor)+';'+'\n'
                elif instr.tipo =="+=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'+'+str(valor)+';'+'\n'
                elif instr.tipo =="-=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'-'+str(valor)+';'+'\n'
                elif instr.tipo =="*=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'*'+str(valor)+';'+'\n' 
                elif instr.tipo =="/=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'/'+str(valor)+';'+'\n'
                elif instr.tipo =="%=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'%'+str(valor)+';'+'\n'
                elif instr.tipo =="<<=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'<<'+str(valor)+';'+'\n'
                elif instr.tipo ==">>=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'>>'+str(valor)+';'+'\n'
                elif instr.tipo =="&=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'&'+str(valor)+';'+'\n'
                elif instr.tipo =="|=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'|'+str(valor)+';'+'\n'
                elif instr.tipo =="^=":
                    self.CodigoGenerado += '\t'+iden+'='+iden+'^'+str(valor)+';'+'\n'
            except:           
                pass
            
        return
   
    def procesar_mientras(self,instr, ts) :
        while resolver_expresion_logica(instr.expLogica, ts) :
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            procesar_instrucciones(instr.instrucciones, ts_local)

    def procesar_if(self,instr, ts) :
        try:
            condicion = self.resolver_expresion_logica(instr.exp,ts)
        except :
            err = 'Error No se puede resolver la expresion a comparar en el if ',instr.exp ,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            self.errores.append(err)

        if condicion == 1: 
            self.Llamada_goto(instr.goto,ts,self.instrucciones)
            return 1
        else:
            return 0

    def procesar_ifSimple (self, instr, ts):
        try:
            condicion = self.resolver_expresion_aritmetica(instr.cond,ts)
        except:
            print("Error al encontrar la condicion del if")
        try:    
            etiVer = self.generaLabel()
            etiFal = self.generaLabel()
            etiSal = self.generaLabel()
            self.CodigoGenerado += '\t'+'if (!'+str(condicion)+') goto '+etiFal+';'+'\n'
            self.procesar_sentencias(instr.bloqueSentenciasIf,ts)
            #self.CodigoGenerado += '\t'+'goto '+etiFal+ ';'+'\n'

            #self.CodigoGenerado +=etiVer+":"+"\n"

            #self.CodigoGenerado +='\t'+"goto "+etiSal+";"+"\n"
            self.CodigoGenerado +=etiFal+":"+"\n"
            self.CodigoGenerado +='\t'+"goto "+etiSal+";"+"\n"
            return etiSal
        except :
            print('error en if',instr.linea, instr.columna)
            return 0

    def procesar_While (self, instr, ts):
        try:
            etiVer = self.generaLabel()
            etiFal = self.generaLabel()
            etiSal = self.generaLabel()

            self.CodigoGenerado +=etiSal+":"+"\n"
            condicion = self.resolver_expresion_aritmetica(instr.condicion,ts)
            self.CodigoGenerado += '\t'+'if ('+str(condicion)+') goto '+etiVer+';'+'\n'
            self.CodigoGenerado += '\t'+'goto '+etiFal+ ';'+'\n'

            self.CodigoGenerado +=etiVer+":"+"\n"
            self.procesar_sentencias(instr.instrucciones,ts)
            self.CodigoGenerado +='\t'+"goto "+etiSal+";"+"\n"
            self.CodigoGenerado +=etiFal+":"+"\n"
        except:
            print("error al traducir el while")  

    def procesar_for(self, instr,ts):
        try:
            etiVer = self.generaLabel()
            etiFal = self.generaLabel()
            etiRep = self.generaLabel()
            #ts_local = TS.TablaDeSimbolos(ts.simbolos)
            ts_local = copy.deepcopy(TS.TablaDeSimbolos(ts.simbolos))
            if isinstance(instr.definicion, Definicion): self.procesar_definicion(instr.definicion,ts_local)
            elif isinstance(instr.definicion,Asignacion): self.procesar_asignacion(instr.definicion,ts_local)
            self.CodigoGenerado += etiRep+":"+"\n"
            cond = self.resolver_expresion_logica(instr.condicion,ts_local)
            self.CodigoGenerado+='\t'+"if ("+cond+") goto "+etiVer+";"+"\n"
            self.CodigoGenerado+='\t'+"goto "+etiFal+";"+"\n"
            self.CodigoGenerado += etiVer+":"+"\n"
            self.procesar_sentencias(instr.sentencias,ts_local)
            self.procesar_incremento(instr.incremento,ts_local)
            self.CodigoGenerado+='\t'+"goto "+etiRep+";"+"\n"
            self.CodigoGenerado += etiFal+":"+"\n"
        except:
            print("error, no se puede traducir el ciclo for")
            return
            
    def procesar_sentencias(self,sentencias,ts):
        for sent in sentencias:
            if isinstance(sent,Imprimir): self.procesar_imprimir(sent,ts)
            elif isinstance(sent,Definicion): self.procesar_definicion(sent,ts)
            elif isinstance(sent,Asignacion): self.procesar_asignacion(sent,ts)
            elif isinstance(sent,inc) : self.procesar_incremento(sent,ts)
            elif isinstance(sent,While): self.procesar_While(sent,ts)
            elif isinstance(sent,IfSimple): 
                sal =self.procesar_ifSimple(sent,ts)
                self.CodigoGenerado += sal+":"+"\n"
                if sal==0:
                    print("error en traducir if")
                    return
            elif isinstance(sent,IfElse): 
                if self.procesar_ifElse(sent,ts) == 0:
                    print("error en traducir if else")
                    return
            elif isinstance(sent,Goto): self.Llamada_goto(sent,ts)
            elif isinstance(sent,Label): self.procesa_Label(sent,ts)
            elif isinstance(sent, DeclaracionStruct) : self.procesar_decla_struct(sent, ts)
            elif isinstance(sent, AsignacionStruct) : self.procesar_asignacion_struct(sent,ts)
            elif isinstance(sent, FuncionFor): self.procesar_for(sent,ts)
            elif isinstance(sent, ExpresionLlamada): self.procesar_llamada_funcion(sent,ts)
            elif isinstance(sent, DeclaracionStructArr) : self.procesar_decla_struct_arr(sent, ts)
            elif isinstance(sent, AsignacionStructArray): self.procesar_asignacion_struct_arr(sent,ts)
            elif isinstance(sent, Return): self.procesar_return(sent,ts)
            else:
                print(sent)
                print('error, sentencia no posible de realizar')
    
    def procesar_ifElse(self,instr, ts) :
        try:
            salida= self.procesar_ifSimple(instr.ifinst,ts) 
            self.procesar_sentencias(instr.elseinst,ts)
            self.CodigoGenerado += salida +":"+"\n"
            return 1
        except:
            print('error, no se puede traducir el if else')
            return 0

    def resolver_cadena(self,exp, ts) :
        if isinstance(exp, ExpresionConcatenar) :
            exp1 = resolver_cadena(exp.exp1, ts)
            exp2 = resolver_cadena(exp.exp2, ts)
            return exp1 + exp2
        elif isinstance(exp, ExpresionDobleComilla) :
            return exp.val
        elif isinstance(exp, ExpresionCadenaNumerico) :
            return str(resolver_expresion_aritmetica(exp.exp, ts))
        elif isinstance(exp,ExpresionIdentificador):
            return str(ts.obtener(exp.id).valor)
        else :
            print('Error: Expresión cadena no válida')

    def resolver_expresion_logica(self,expLog, ts) :

        exp1 = self.resolver_expresion_aritmetica(expLog.exp1, ts)
        exp2 = self.resolver_expresion_aritmetica(expLog.exp2, ts)
        if expLog.exp1.tipo == TS.TIPO_DATO.INT or expLog.exp1.tipo == TS.TIPO_DATO.FLOAT:
            if expLog.exp2.tipo == TS.TIPO_DATO.INT or expLog.exp2.tipo == TS.TIPO_DATO.FLOAT:
                expLog.tipo = TS.TIPO_DATO.INT
                if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' > '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.MENOR_QUE :
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' < '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.IGUAL : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' == '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.DIFERENTE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' != '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.MAYORQUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' >= '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.MENORQUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' <= '+str(exp2)+';'+'\n'
                    return temp
            else:
                print('Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo')
                err = 'Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo' ,' En la linea: ',expLog.linea,' En la columna: ',expLog.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)  
        elif expLog.exp1.tipo == TS.TIPO_DATO.CADENA:
            if expLog.exp2.tipo == TS.TIPO_DATO.CADENA:
                expLog.tipo = TS.TIPO_DATO.INT
                if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' > '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.MENOR_QUE :
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' < '+str(exp2)+';'+'\n'
                    return temp
                if expLog.operador == OPERACION_LOGICA.IGUAL : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' == '+str(exp2)+';'+'\n'
                    return temp 
                if expLog.operador == OPERACION_LOGICA.DIFERENTE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' != '+str(exp2)+';'+'\n'
                    return temp  
                if expLog.operador == OPERACION_LOGICA.MAYORQUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' >= '+str(exp2)+';'+'\n'
                    return temp  
                if expLog.operador == OPERACION_LOGICA.MENORQUE : 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' <= '+str(exp2)+';'+'\n'
                    return temp                                                                    
            else:
                print('error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, \n se espera que ambos tengan el mismo tipo')
                err = 'Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo' ,' En la linea: ',expLog.linea,' En la columna: ',expLog.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)  

    def resolver_expresion_aritmetica(self,expNum, ts) :
        if isinstance(expNum, ExpresionBinaria) :
            #VALIDAR TIPOS
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1, ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2, ts)

            if (expNum.exp1.tipo==td.INT):

                if(expNum.exp2.tipo==td.INT):


                    if expNum.operador == OPERACION_ARITMETICA.MAS : 
                        expNum.tipo = TS.TIPO_DATO.INT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'+'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                        expNum.tipo = TS.TIPO_DATO.INT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'-'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.POR : 
                        expNum.tipo = TS.TIPO_DATO.INT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'*'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                        expNum.tipo = TS.TIPO_DATO.INT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'/'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                        expNum.tipo = TS.TIPO_DATO.INT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'%'+str(exp2)+";"+"\n"
                        return temporal
                        
                elif (expNum.exp2.tipo==td.FLOAT):

                    if expNum.operador == OPERACION_ARITMETICA.MAS :                      
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'+'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'-'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.POR : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'*'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'/'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'%'+str(exp2)+";"+"\n"
                        return temporal
                    else:
                        print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
                        err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                        self.errores.append(err)  
                else:
                    print('Error de tipos: el operador ',expNum.exp2.val,' no es de tipo INT o FLOAT y no puede ser operado ')
                    err = 'Error de tipos: el operador ',expNum.exp2.val,' no es de tipo INT o FLOAT y no puede ser operado' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err)  

            elif (expNum.exp1.tipo==td.FLOAT):
        
                if(expNum.exp2.tipo==td.INT or expNum.exp2.tipo==td.FLOAT):
                    if expNum.operador == OPERACION_ARITMETICA.MAS : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'+'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'-'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.POR : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'*'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'/'+str(exp2)+";"+"\n"
                        return temporal
                    if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                        expNum.tipo = TS.TIPO_DATO.FLOAT
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'%'+str(exp2)+";"+"\n"
                        return temporal
                    else:
                        print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
                        err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                        self.errores.append(err)  
                else:
                    print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo INT o FLOAT y no puede ser operado ')   
                    err = 'Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo INT o FLOAT y no puede ser operado ' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err)  

            elif (expNum.exp1.tipo==td.CADENA):
                if(expNum.exp2.tipo==td.CADENA):
                    if expNum.operador == OPERACION_ARITMETICA.MAS : 
                        expNum.tipo = TS.TIPO_DATO.CADENA
                        temporal = self.generarTemp()
                        self.CodigoGenerado += '\t'+temporal+'='+str(exp1)+'+'+str(exp2)+";"+"\n"
                        return temporal
                    else:
                        print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
                        err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion ' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                        self.errores.append(err)  
                else:
                    print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo CADENA y no puede ser operado ')
                    err = 'Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo CADENA y no puede ser operado' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err)
        
        elif isinstance(expNum, ExpresionNegativo) :
            exp = self.resolver_expresion_aritmetica(expNum.exp, ts)
            expNum.tipo = expNum.exp.tipo
            temporal = self.generarTemp()
            self.CodigoGenerado += '\t'+temporal+'='+"-"+str(exp)+";"+"\n"
            return temporal

        elif isinstance(expNum, ExpresionNumero) :
            expNum.tipo = expNum.tipo
            return expNum.val

        elif isinstance(expNum, ExpresionIdentificador) :
            
            return ts.obtener(expNum.id).valor

        elif isinstance (expNum, ExpresionPuntero):
            temp = str(expNum.id).lstrip('&')           
            try:
                reg = ts.obtener(temp).reg
                r = self.generarTemp()
                self.CodigoGenerado += '\t'+r+'='+'&'+reg+';'+'\n'
                expNum.tipo = td.INT
                return r
            except :
                print('error, no existe el registro asociado al puntero')
                return expNum.val

        elif isinstance (expNum,ExpresionValorAbsoluto):
            temp=self.resolver_expresion_aritmetica(expNum.exp,ts)
            if expNum.exp.tipo== TS.TIPO_DATO.INT or expNum.exp.tipo == TS.TIPO_DATO.FLOAT:
                print(temp)
                expNum.val = abs(temp)
                expNum.tipo = expNum.exp.tipo
            else:
                expNum.val=temp
                expNum.tipo = expNum.exp.tipo
                print('No es posible obtener el valor absoluto de: ',expNum.val)
                err = 'Error, no es posible obtener el valor absoluto de: ',expNum.val ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)
            return expNum.val

        elif isinstance (expNum,ExpresionConversion):
            reg = self.resolver_expresion_aritmetica(expNum.exp,ts) 
            conv = expNum.tipo
            if conv=="int":
                expNum.Tipo = td.INT
            elif conv == "float":
                expNum.Tipo = td.FLOAT
            elif conv == "char":
                expNum.Tipo = td.CADENA
            r = self.generarTemp()
            self.CodigoGenerado+='\t'+r+"=("+conv+")"+reg+";"+"\n"
            
            return r
            
        elif isinstance (expNum, ExpresionLogicaNot):
            temp = self.resolver_expresion_aritmetica(expNum.exp,ts)
            expNum.tipo=TS.TIPO_DATO.INT
            temporal = self.generarTemp()
            self.CodigoGenerado += '\t'+temporal+'= !'+str(temp)+";"+'\n'
            return temporal
    
        elif isinstance (expNum, ExpresionLogicaXOR):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
                expNum.tipo = TS.TIPO_DATO.INT
                temp = self.generarTemp()
                self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' xor '+str(exp2)+';'+'\n'
                return temp
            else:
                print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un XOR, ambos deben ser INT')
                err = 'Error de tipos ',exp2,'y ',exp2,' no pueden operarse en un XOR, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)  
        
        elif isinstance (expNum, ExpresionLogicaOR):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
                expNum.tipo = TS.TIPO_DATO.INT
                temp = self.generarTemp()
                self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' || '+str(exp2)+';'+'\n'
                return temp
            else:
                print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un OR, ambos deben ser INT')
                err = 'Error de tipos ',exp1,'y ',exp2,' no pueden operarse en un OR, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum, ExpresionLogicaAND):   
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
                expNum.tipo = TS.TIPO_DATO.INT
                temp = self.generarTemp()
                self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' && '+str(exp2)+';'+'\n'
                return temp     
            else:
                print('error de tipos ',exp1,' y "=',exp2,' no pueden operarse en un AND, ambos deben ser INT')
                err = 'Error de tipos ',exp1,' y "=',exp2,' no pueden operarse en un AND, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)   
        
        elif isinstance (expNum, ExpresionBitNot):
            temp = self.resolver_expresion_aritmetica(expNum.exp,ts)
            if expNum.exp.tipo == TS.TIPO_DATO.INT or expNum.exp.tipo == TS.TIPO_DATO.FLOAT:       
                expNum.tipo = TS.TIPO_DATO.INT
                temporal = self.generarTemp()
                self.CodigoGenerado += '\t'+temporal+'= ~'+str(temp)+';'+'\n'
                return temporal   
            else:
                print('El valor ',temp,'no pude ser operado en binario por un NOT, se esperaba un tipo INT o FLOAT')
                err = 'Error el valor ',temp,'no pude ser operado en binario por un NOT, se esperaba un tipo INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err)   
    
        elif isinstance (expNum, ExpresionBitAnd):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT:     
                if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                    expNum.tipo = TS.TIPO_DATO.INT
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' & '+str(exp2)+';'+'\n'
                    return temp
                else:
                    print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')
                    err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum, ExpresionBitOr):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT:    
                if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' | '+str(exp2)+';'+'\n'
                    return temp
                else:
                    print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT')
                    err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT')
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum, ExpresionBitXor):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT:  
                if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                    expNum.tipo = TS.TIPO_DATO.INT
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' ^ '+str(exp2)+';'+'\n'
                    return temp
                else:
                    print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT')
                    err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT')
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum, ExpresionBitIzq):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT:    
                if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                    expNum.tipo = TS.TIPO_DATO.INT
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' << '+str(exp2)+';'+'\n'
                    return temp
                else:
                    print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT')
                    err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT')
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum, ExpresionBitDer):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1,ts)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2,ts)
            if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT:   
                if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                    expNum.tipo = TS.TIPO_DATO.INT
                    temp = self.generarTemp()
                    self.CodigoGenerado += '\t'+temp+'='+str(exp1)+' >> '+str(exp2)+';'+'\n'
                    return temp
                else:
                    print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT')
                    err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT')
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                self.errores.append(err) 
        
        elif isinstance (expNum,ExpresionLogica):
            return self.resolver_expresion_logica(expNum,ts)
        
        elif isinstance (expNum, InicioArray):
            expNum.tipo = TS.TIPO_DATO.ARRAY
            expNum.val = {}
            return expNum.val
        
        elif isinstance(expNum,ExpresionPila):
            expNum.val = ts.obtener(expNum.id).valor
            expNum.tipo = ts.obtener(expNum.id).tipo
            return expNum.val
    
        elif isinstance (expNum,ExpresionPunteroPila):
            expNum.val = ts.obtener(expNum.id).valor
            expNum.tipo = td.INT
            return expNum.val

        elif isinstance(expNum,Expresion_Pop_pila):
            pila = ts.obtener(expNum.idPila).valor
            puntero = ts.obtener(expNum.puntero).valor
            
            expNum.val = pila[puntero]

            if isinstance(expNum.val,int): expNum.tipo = td.INT
            elif isinstance (expNum.val,str): expNum.tipo = td.CADENA
            elif isinstance(expNum.val,float): expNum.tipo = td.FLOAT
            return expNum.val

        elif isinstance(expNum,Expresion_param):
            expNum.val = ts.obtener(expNum.id).valor
            expNum.tipo = ts.obtener(expNum.id).tipo
            return expNum.val
        
        elif isinstance(expNum,AccesoValorArray):

            temporal = ts.obtener(expNum.id).valor

            for j in range(len(expNum.lista)):
                ind = self.resolver_expresion_aritmetica(expNum.lista[j],ts)
                if (j==(len(expNum.lista)-1)):

                    temporal = temporal.get(ind)
                    if temporal == None:
                        print('Error, no existe un valor en el indice: ',ind)
                        err = 'Error, no existe un valor en el indice: ',ind,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                        self.errores.append(err) 
                else:
                    temporal_aux = temporal.get(ind)
                    if temporal_aux == None:
                        print('Error, no existe un valor en el indice: ',ind)
                        err = 'Error, no existe un valor en el indice: ',ind,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                        self.errores.append(err) 
                    else:
                        temporal = temporal.get(ind)

            if isinstance (temporal,str): expNum.tipo = td.CADENA
            elif isinstance(temporal,int): expNum.tipo = td.INT
            elif isinstance(temporal,float): expNum.tipo = td.FLOAT
            elif isinstance (temporal,dict): expNum.tipo = td.ARRAY
            return temporal            
        
        elif isinstance(expNum,Read):
            val = "SAD"
            res = val.getInteger()
            val.cerrar()
            patronFloat = re.compile('([0-9]+(\.)[0-9]+){1}')
            patronNum = re.compile('[0-9]+')
            if patronFloat.match(res):
                expNum.val = float(res)
                expNum.tipo = td.FLOAT
            elif patronNum.match(res):
                expNum.val = int(res)
                expNum.tipo = td.INT
            else:
                expNum.val = str(res)
                expNum.tipo = td.CADENA
            return expNum.val
        
        elif isinstance(expNum,ExpresionId):
            try:
                registro = ts.obtener(expNum.id)
                expNum.tipo = registro.tipo
                return registro.reg
            except:
                print('Error, la variable solicitada no existe o no tiene un registro asociado')
                return
        elif isinstance(expNum,ExpresionInicioSimple):
            try:
                registro = ts.obtener(expNum.id)
                expNum.tipo = registro.tipo
                return registro.reg
            except:
                print('Error, la variable solicitada no existe o no tiene un registro asociado')
                return
        elif isinstance(expNum,ExpresionAccesoStruct):
            padre = ts.obtener(expNum.idPadre)
            hijo = expNum.idHijo
            expNum.tipo = padre.tipo
            temporal = self.generarTemp()
            self.CodigoGenerado += '\t'+temporal+'='+padre.reg+'[\''+str(hijo)+'\']'+';'+'\n'
            return temporal
        elif isinstance(expNum,ExpresionAccesoStructArr):
            padre = ts.obtener(expNum.idPadre)
            pos = self.resolver_expresion_aritmetica(expNum.pos,ts)
            hijo = expNum.idHijo
            expNum.tipo = padre.tipo
            temporal = self.generarTemp()
            self.CodigoGenerado += '\t'+temporal+'='+padre.reg+"["+str(pos)+"]"+'[\''+str(hijo)+'\']'+';'+'\n'
            return temporal
        elif isinstance(expNum, ExpresionListaIndices):
            array = ts.obtener(expNum.id)
            if len(expNum.listaindices)>=2:
                #calculo de la primera posicion
                t1  = self.generarTemp()
                pos1= self.resolver_expresion_aritmetica(expNum.listaindices[0],ts)
                self.CodigoGenerado+= '\t'+t1+"="+str(pos1)+";"+"\n"
                
                #calculo de la segunda posicion
                t2 = self.generarTemp()
                n2 = array.valor[1]
                self.CodigoGenerado+= '\t'+t2+"="+t1+"*"+str(n2)+";"+"\n"
                t3 = self.generarTemp()
                pos2 =self.resolver_expresion_aritmetica(expNum.listaindices[1],ts)
                self.CodigoGenerado+= '\t'+t3+"="+t2+"+"+str(pos2)+";"+"\n"
                t4 = self.generarTemp()
                self.CodigoGenerado+= '\t'+t4+"="+array.reg+"["+t3+"];"+"\n"
                expNum.tipo = array.tipo
                return t4
            elif len(expNum.listaindices)==1:
                t1  = self.generarTemp()
                pos1= self.resolver_expresion_aritmetica(expNum.listaindices[0],ts)
                self.CodigoGenerado+= '\t'+t1+"="+array.reg+"["+str(pos1)+"];"+"\n"
                expNum.tipo = array.tipo
                return t1
        elif isinstance(expNum, ExpresionScan):

            read = "read()"
            return read
        else:
            print(expNum)
            err = 'Error, no existe un valor en el indice: ',expNum,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            self.errores.append(err) 

    def procesar_unset(self,exp, ts):
        
        if isinstance(exp.exp,ExpresionTemporal):
            temp = exp.exp.id
            ts.eliminar(temp)
        else:
            print('El valor ',exp.exp.id,'no puede ser ejecutado por unset(), se esperaba un registro')
            err = 'Error el valor ',exp.exp.id,'no puede ser ejecutado por unset(), se esperaba un registro',' En la linea: ',exp.linea,' En la columna: ',exp.columna, 'Tipo: SEMANTICO'
            self.errores.append(err) 

    def procesar_incremento(self, instr, ts):
        try:
            reg = ts.obtener(instr.exp) 
        except:
            print('la variable no esta definida')
        try:
            if reg.tipo == td.INT:
                if instr.tipo == '++':
                    self.CodigoGenerado += '\t'+reg.reg+'='+reg.reg+'+1;'+'\n'
                elif instr.tipo == '--':
                    self.CodigoGenerado += '\t'+reg.reg+'='+reg.reg+'-1;'+'\n'
        except :
            print('error de tipos')

        return

    def procesar_main(self, instr, ts):
        self.CodigoGenerado += "main:"+"\n"
        try:
            self.procesar_sentencias(instr.sentencias,ts)
            #self.CodigoGenerado+='\t'+"exit;"+"\n"
        except :
            print('error, no se pueden ejecutar las sentencias dentro de main')

    def procesar_asignacion_extra (self,instr,ts):
        try:
            val = self.resolver_expresion_aritmetica(instr.exp, ts)
            simbolo = TS.Simbolo(instr.id, instr.exp.tipo, val,self.Etiqueta)
            if ts.existeSimbolo(simbolo) :
                ts.actualizar(simbolo)
            else:
                ts.agregar(simbolo)
        except :
            print('No se puede realizar la asignacion de',instr.id)
            err = 'Error No se puede realizar la asignacion de',instr.id,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            self.errores.append(err) 
            pass

    def procesar_asignacion_arreglo (self,instr,ts):
        diccionario = ts.obtener(instr.id).valor
        lista = instr.lista
        niveles = len(lista)
        valor_a_asignar = self.resolver_expresion_aritmetica(instr.exp,ts)

        for i in range(len(lista)):
            indice = self.resolver_expresion_aritmetica(lista[i],ts)
            if i== niveles-1:
                diccionario[indice]=valor_a_asignar
            else:
                diccionario_aux = diccionario.get(indice)
                if diccionario_aux == None:
                    diccionario[indice]={}
                    diccionario=diccionario.get(indice)
                else:
                    diccionario=diccionario.get(indice)

    def procesa_Label(self,instr,ts):
        try:
            self.CodigoGenerado+=str(instr.id)+":"+"\n"
        except :
            print("error, no se puede traducir el label")

    def Llamada_goto(self,instr,ts):  
        try:
            self.CodigoGenerado += "\t"+"goto "+instr.id + ";" + "\n"
            return
        except :
            print("error en traduccion de goto")
            return

    def procesar_funcion (self, instr,ts):
        try:
            self.CodigoGenerado += instr.id+":"+"\n"
            if instr.parametros[0].exp!=0:
                salida = self.generaLabel()
                parametros =[]
                for par in instr.parametros:
                    if par.tipo == td.INT :
                        para = self.generaPar()
                        nuevo = TS.Simbolo(par.exp,par.tipo,0,para,instr.id)
                        parametros.append(para)
                    elif par.tipo == td.CADENA:
                        para = self.generaPar()
                        nuevo = TS.Simbolo(par.exp,par.tipo," ",para,instr.id)
                        parametros.append(para)
                    elif par.tipo == td.FLOAT:
                        para = self.generaPar()
                        nuevo = TS.Simbolo(par.exp,par.tipo,0.0,para,instr.id)
                        parametros.append(para)
                    if ts.existeSimbolo(nuevo)==False:
                        ts.agregar(nuevo)
                    else:
                        ts.actualizar(nuevo)
                fun = TS.Simbolo(instr.id,td.FUNCION,parametros,salida)
                ts.agregar(fun)
            else:
                salida = self.generaLabel()
                fun = TS.Simbolo(instr.id,td.FUNCION,{},salida)
                ts.agregar(fun)
            self.procesar_sentencias(instr.sentencias,ts)
            self.CodigoGenerado += '\t'+"goto "+salida+";"+"\n"
        except :
            print('Error al traducir la funcion')

    def procesar_llamada_funcion(self, instr, ts):
        parametrosGuardados = ts.obtener(instr.id)

        if len(parametrosGuardados.valor)==len(instr.parametros):
            for i in range(len(parametrosGuardados.valor)):
                self.CodigoGenerado += "\t"+parametrosGuardados.valor[i]+"="+str(self.resolver_expresion_aritmetica(instr.parametros[i],ts))+";"+"\n"

        self.CodigoGenerado +="\t"+"goto "+instr.id+";"+"\n"    
        self.CodigoGenerado +=parametrosGuardados.reg+":"+"\n"
    
    def procesar_def_struct(self, instr, ts):

        try:
            elementos =[]
            for i in instr.elementos:
                t=i.tipo
                for e in i.ide:
                    iden =e.id.id
                    elementos.append([t,iden])
            nuevo = TS.Simbolo(instr.ide,td.STRUCT,elementos,'struct')
            if ts.existeSimbolo(nuevo)==False:
                ts.agregar(nuevo)
        except :
            print("Error, Struct ya definido")
            pass

    def procesar_decla_struct(self,instr,ts):
        try:
            struct = ts.obtener(instr.TipoStruct)
        except :
            print('error, el struct no esta definidio previamente')

        try:
            registro = self.generarTemp()
            nuevo = TS.Simbolo(instr.ide,td.STRUCT,{},registro)

            if ts.existeSimbolo(nuevo)==False:
                ts.agregar(nuevo)
                self.Global += '\t'+registro+'=array();'+'\n'

                for i in struct.valor:
                    if i[0] == td.INT:
                        self.Global +='\t'+registro+'[\''+i[1]+'\']=0;'+'\n'
                    elif i[0]== td.FLOAT:
                        self.Global +='\t'+registro+'[\''+i[1]+'\']=0.0;'+'\n'
                    elif i[0] == td.CADENA:
                        self.Global +='\t'+registro+'[\''+i[1]+'\']=\"0\";'+'\n'
                                 
        except:
            print('error, nose puede traducir la declaracion de struct')
    
    def procesar_decla_struct_arr(self,instr, ts):
        try:
            struct = ts.obtener(instr.TipoStruct)
        except :
            print('error, el struct no esta definidio previamente')
        try:    
            registro = self.generarTemp()
            nuevo = TS.Simbolo(instr.ide,td.STRUCT,{},registro)
            if ts.existeSimbolo(nuevo)==False:
                ts.agregar(nuevo)
                self.Global += '\t'+registro+'=array();'+'\n'
                for ind in instr.indices:
                    indice = self.resolver_expresion_aritmetica(ind,ts)
                
                for i in range(indice):
                    for e in struct.valor:
                        if e[0]==td.INT:
                            self.Global +='\t'+registro+"["+str(i)+"][\'"+e[1]+"\']=0;"+"\n"
                        elif e[0]==td.FLOAT:
                            self.Global +='\t'+registro+"["+str(i)+"][\'"+e[1]+"\']=0.0;"+"\n"
                        elif e[0]==td.CADENA:
                            self.Global +='\t'+registro+"["+str(i)+"][\'"+e[1]+"\']=\'0\';"+"\n"     
        
        except:
            print('error, nose puede traducir la declaracion de struct')

    def procesar_asignacion_struct(self,instr,ts):
        struct = ts.obtener(instr.TipoStruct)
        valor =self.resolver_expresion_aritmetica(instr.valor,ts)
        self.Global += '\t'+struct.reg+'[\''+instr.ide+'\']='+str(valor)+";"+"\n"

    def procesar_asignacion_struct_arr(self,instr,ts):
        struct = ts.obtener(instr.Struct)
        valor =self.resolver_expresion_aritmetica(instr.valor,ts)
        ind = self.resolver_expresion_aritmetica(instr.indice,ts)
        self.Global += '\t'+struct.reg+"["+str(ind)+"]"+'[\''+instr.ide+'\']='+str(valor)+";"+"\n"

    def ejecutar_expresiones_label(self,listainstrucciones,ts,listaglobal):
            for instr in listainstrucciones :
                if isinstance(instr, Imprimir) : self.procesar_imprimir(instr, ts)
                elif isinstance(instr, Definicion) : self.procesar_definicion(instr, ts)
                elif isinstance(instr, Asignacion) : self.procesar_asignacion(instr, ts)
                elif isinstance(instr, Mientras) : self.procesar_mientras(instr, ts)
                elif isinstance(instr, If) : self.procesar_if(instr, ts)
                elif isinstance(instr, IfElse) : 
                    if self.procesar_if_else(instr, ts) == 1 : return
                elif isinstance(instr, Unset) : self.procesar_unset(instr,ts)
                elif isinstance(instr,AsignaPunteroPila): self.procesar_asignacion_punteropila(instr,ts)
                elif isinstance(instr,AsignaValorPila): self.procesar_asignacion_pila(instr,ts)
                elif isinstance(instr, AsignacionExtra): self.procesar_asignacion_extra(instr,ts)
                elif isinstance(instr, Main): self.Etiqueta = 'Main'
                elif isinstance(instr,Asigna_arreglo): self.procesar_asignacion_arreglo(instr,ts)
                elif isinstance(instr,Label): self.procesa_Label(instr,ts)
                elif isinstance(instr,Exit): return
                elif isinstance(instr,Goto):
                    self.Llamada_goto(instr,ts, listaglobal)
                    return
                else : 
                    print('Error: instrucción no válida', instr)
                    err = 'Error: instrucción no válida', instr,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 

    def procesar_return(self,instr,ts):
        r = self.resolver_expresion_aritmetica(instr.exp,ts)
        ret = self.generaRetorno()
        self.CodigoGenerado+='\t'+ret+"="+str(r)+";"+"\n"
        return
        
    def procesar_instrucciones(self,instrucciones, ts) :
        ## lista de instrucciones recolectadas.

        for instr in instrucciones :
            if isinstance(instr, Main) : 
                self.procesar_main(instr,ts)
                self.CodigoGenerado +="exit;"+"\n"
            elif isinstance(instr, Definicion) : self.procesar_definicion_global(instr, ts)
            elif isinstance(instr, Asignacion) : self.procesar_asignacion_global(instr, ts)
            elif isinstance(instr, inc) : self.procesar_incremento(instr, ts)
            elif isinstance(instr, DefinicionFuncion) : self.procesar_funcion(instr, ts)
            elif isinstance(instr, DefStruct) : self.procesar_def_struct(instr,ts)
            elif isinstance(instr, DeclaracionStruct) : self.procesar_decla_struct(instr, ts)
            elif isinstance(instr, AsignacionStruct) : self.procesar_asignacion_struct(instr,ts)
            elif isinstance(instr, DeclaracionStructArr) : self.procesar_decla_struct_arr(instr, ts)
            elif isinstance(instr, AsignacionStructArray): self.procesar_asignacion_struct_arr(instr,ts)
            elif isinstance(instr, Return): self.procesar_return(instr,ts)
            #elif isinstance(instr,AsignaValorPila): self.procesar_asignacion_pila(instr,ts)
            #elif isinstance(instr, AsignacionExtra): self.procesar_asignacion_extra(instr,ts)
            #elif isinstance(instr, Main): self.Etiqueta = 'Main'
            #elif isinstance(instr,Asigna_arreglo): self.procesar_asignacion_arreglo(instr,ts)
            #elif isinstance(instr,Label): self.procesa_Label(instr,ts)
            #elif isinstance(instr,Exit): return
            #elif isinstance(instr,Goto): 
                #self.Llamada_goto(instr,ts, instrucciones)
                #return
                
            else : 
                err = 'Error: instrucción no válida', instr,' En la linea: ',instr,' En la columna: ',instr, 'Tipo: SEMANTICO'
                self.errores.append(err) 

    def procesar_instrucciones_debugger(self,instrucciones, ts, i) :
        ## lista de instrucciones recolectadas
        if isinstance(instrucciones[0],Main):
            if i <= len(instrucciones):
                if isinstance(instrucciones[i], Imprimir) : self.procesar_imprimir(instrucciones[i], ts)
                elif isinstance(instrucciones[i], Definicion) : self.procesar_definicion(instrucciones[i], ts)
                elif isinstance(instrucciones[i], Asignacion) : self.procesar_asignacion(instrucciones[i], ts)
                elif isinstance(instrucciones[i], Mientras) : self.procesar_mientras(instrucciones[i], ts)
                elif isinstance(instrucciones[i], If) :
                    if self.procesar_if(instrucciones[i], ts)==1 : 
                        return
                elif isinstance(instrucciones[i], IfElse) : self.procesar_if_else(instrucciones[i], ts)
                elif isinstance(instrucciones[i], Unset) : self.procesar_unset(instrucciones[i],ts)
                elif isinstance(instrucciones[i],AsignaPunteroPila): self.procesar_asignacion_punteropila(instrucciones[i],ts)
                elif isinstance(instrucciones[i],AsignaValorPila): self.procesar_asignacion_pila(instrucciones[i],ts)
                elif isinstance(instrucciones[i], AsignacionExtra): self.procesar_asignacion_extra(instrucciones[i],ts)
                elif isinstance(instrucciones[i], Main): self.Etiqueta = 'Main'
                elif isinstance(instrucciones[i],Asigna_arreglo): self.procesar_asignacion_arreglo(instrucciones[i],ts)
                elif isinstance(instrucciones[i],Label): self.procesa_Label(instrucciones[i],ts)
                elif isinstance(instrucciones[i],Exit): return
                elif isinstance(instrucciones[i],Goto): 
                    self.Llamada_goto(instrucciones[i],ts, instrucciones)
                    return
                
                else : 
                    err = 'Error: instrucción no válida', instrucciones[i],' En la linea: ',instrucciones[i].linea,' En la columna: ',instrucciones[i].columna, 'Tipo: SEMANTICO'
                    self.errores.append(err) 
            else:
                print('sad')
                return
        else:
            print('Error la etiqueta main no esta al inicio del programa o no existe')
            err = 'Error la etiqueta main no esta al inicio del programa o no existe',' En la linea: ',instrucciones[i].linea,' En la columna: ',instrucciones[i].columna, 'Tipo: SEMANTICO'
            self.errores.append(err) 

    def generarTemp(self):
        temp = '$t'+str(self.cont)
        self.cont+=1
        return temp

    def generaLabel(self):
        eti = 'Label'+str(self.contLabel)
        self.contLabel+=1
        return eti

    def generaPar(self):
        eti = '$a'+str(self.contPar)
        self.contPar+=1
        return eti

    def generaRetorno(self):
        eti = '$v'+str(self.contRet)
        self.contRet+=1
        return eti

a = Ejecucion_MinorC()

f = open("./entrada.txt", "r")
input = f.read()
a.ejecutar_asc(input)
a.GenerarAST()
print(a.salidaTotal)
