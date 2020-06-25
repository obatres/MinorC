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
#--------------------------------------METODOS/FUNCIONES DE EJECUCION EN INTERFAZ
    def ejecutar_asc(self, input):
        import gramaticaM as g
        #self.gram = g.verGramatica()
        self.instrucciones = g.parse(input) 
        #print(self.instrucciones)
        self.procesar_instrucciones(self.instrucciones, self.ts_global)   
        
    def errores_asc(self):
        import gramaticaM as g
        self.errores = g.retornalista()
        return self.errores 

    def RecibirSalida(self):
        nuevo = copy.copy(self.resultado)
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
        self.dot.node(nodo,'Etiqueta')
        self.dot.edge(root, nodo)

        cont=cont+1
        nodo1 = 'nodo'+ str(cont)
        self.dot.node(nodo1,'Main')
        self.dot.edge(nodo, nodo1)

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
        self.dot.node(nodo1,instr.id)
        self.dot.edge(nodo,nodo1)
        cont = self.dibujar_expresion(instr.expNumerica,nodo,cont)
        return cont

    def dibujar_print(self,instr,root,cont):
        cont=cont+1
        nodo = 'nodo'+ str(cont)
        self.dot.node(nodo,'Print')
        self.dot.edge(root, nodo)

        cont = self.dibujar_expresion(instr.exp,nodo,cont)

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

        self.dot.edge(nodo,nodo1)

        return cont

    def DibujarAST(self,instrucciones):
        cont = 1
        root = 'nodo'+ str(cont)
        self.dot.node(root, 'AUGUS')
        for instr in instrucciones:
            if isinstance(instr,Asignacion) : cont = self.dibujar_asignacion(instr,root,cont)
            elif isinstance(instr,Imprimir) : cont = self.dibujar_print(instr,root,cont)
            elif isinstance(instr,If): cont = self.dibujar_if(instr,root,cont)
            elif isinstance(instr,Unset): cont = self.dibujar_unset(instr,root,cont)
            elif isinstance(instr,AsignaValorPila): cont = self.dibujar_AsignaValorPila(instr,root,cont)
            elif isinstance(instr,AsignacionExtra): cont = self.dibujar_AsignaRegistro(instr,root,cont)
            elif isinstance(instr,Main): cont = self.dibujar_main(instr,root,cont)
            elif isinstance(instr,Asigna_arreglo): cont=self.dibujar_Asigna_arreglo(instr,root,cont)
            elif isinstance(instr,Label): cont=self.dibujar_Label(instr,root,cont)
            elif isinstance(instr,Goto): cont=self.dibujar_Goto(instr,root,cont)
            elif isinstance(instr,Exit): cont=self.dibujar_exit(instr,root,cont)
            else : 
                print('')
        #print(dot.source)

#--------------------------------------------------------------------PROCESAR INSTRUCCIONES
    def procesar_imprimir(self,instr, ts) :

        try:          
            #salida = resolver_registro(instr.exp,ts)
            salida = self.resolver_expresion_aritmetica(instr.exp,ts)
            #print('>', salida)
            self.CodigoGenerado += '\t'+'print('+str(salida)+');'+"\n"    
            #self.resultado += '>'+str(salida)+'\n'
            return  str(salida) + '\n'
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
                    print('Error, la variable '+str(temp.id)+' ya ha sido declarada anteriormente')
            elif tipo == td.FLOAT:
                nuevo = TS.Simbolo(temp.id,tipo,0.0,registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.CodigoGenerado += '\t' + registro + '= 0.0;'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    print('Error, la variable '+str(temp.id)+' ya ha sido declarada anteriormente')
            elif tipo == td.CADENA:
                nuevo = TS.Simbolo(temp.id,tipo," ",registro)
                if ts.existeSimbolo(nuevo)==False:
                    self.CodigoGenerado += '\t' + registro + '= \' \';'+'\n'
                    ts.agregar(nuevo)
                elif ts.existeSimbolo(nuevo)==True:
                    print('Error, la variable '+str(temp.id)+' ya ha sido declarada anteriormente')
            else:
                print('Error, tipo '+str(tipo)+' no aplicable en la definicion')
        
        elif isinstance (temp,ExpresionListaIndices):
            print('Lista indices')
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
                print('Error, la variable '+str(temp.id)+' ya ha sido declarada anteriormente')
            return
        elif isinstance(temp,ExpresionListaIndices):
            valor = self.resolver_expresion_aritmetica(instr.exp,ts)
            if len(temp.listaindices)<=1:
                registro = self.generarTemp()
                nuevo = TS.Simbolo(temp.id,tipo,valor,registro)
                if ts.existeSimbolo(nuevo) == False:
                    self.CodigoGenerado += '\t'+registro+ '='+str(valor)+';'+'\n'
                    ts.agregar(nuevo)
                return
            else:
                print('mas indices')
            return
        else:
            print(type(instr.id))
        return
   
    def procesar_asignacion(self,instr, ts) :
        try:
            val = self.resolver_expresion_aritmetica(instr.expNumerica, ts)
            simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,self.Etiqueta)
            if ts.existeSimbolo(simbolo) :
                ts.actualizar(simbolo)
            else:
                ts.agregar(simbolo)
        except :
            print('No se puede realizar la asignacionde',instr.id, instr.linea, instr.columna)
            err = 'Error No se puede realizar la asignacionde ',instr.id ,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            self.errores.append(err)
            pass

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

    def procesar_if_else(self,instr, ts) :
        val = resolver_expresion_logica(instr.expLogica, ts)
        if val :
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            procesar_instrucciones(instr.instrIfVerdadero, ts_local)
        else :
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            procesar_instrucciones(instr.instrIfFalso, ts_local)

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
            expNum.val = ts.obtenerPuntero(temp)
            expNum.tipo = TS.TIPO_DATO.INT
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
            temp = self.resolver_expresion_aritmetica(expNum.exp,ts) 
            conv = expNum.tipo
            if conv=='int':
                if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                    expNum.val = ord(temp[0])
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val 
                elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                    expNum.val = int(Decimal(temp))
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val 
                elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                    expNum.val = temp
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                else:
                    print('la conversion a (int) de ',temp,'no se puede realizar por error de tipo')
                    err = 'Error la conversion a (int) de ',temp,'no se puede realizar por error de tipo',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    self.errores.append(err)
            
            elif conv=='float':
                if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                    temp1 = ord(temp[0])
                    expNum.val = str(temp1) + '.0'
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return float(expNum.val)
                elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                    expNum.val = temp
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val 
                elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                    expNum.val = str(temp) + '.0'
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return float(expNum.val) 
                else:
                    print('la conversion a (float) de ',temp,'no se puede realizar por error de tipo')
            
            elif conv=='char':
                if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                    expNum.val = temp[0]
                    expNum.tipo = TS.TIPO_DATO.CADENA
                    return expNum.val
                elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                    temp2 = int(Decimal(temp))
                    if temp2>=0 and temp2<255: expNum.val = chr(temp2)                    
                    elif temp2>=256:          expNum.val = chr(temp2%256)

                    expNum.tipo = TS.TIPO_DATO.CADENA
                    return expNum.val
                elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                    
                    if temp>=0 and temp<255: expNum.val = chr(temp)                    
                    elif temp>=256:          expNum.val = chr(temp%256)

                    expNum.tipo = TS.TIPO_DATO.CADENA
                    return expNum.val
                else:
                    print('la conversion a (char) de ',temp,'no se puede realizar por error de tipo')
            
            else:
                print('La conversion de tipo',expNum.tipo,'No es posible ejecutarla')
            
        elif isinstance (expNum, ExpresionLogicaNot):
            temp = self.resolver_expresion_aritmetica(expNum.exp,ts)
            expNum.tipo=TS.TIPO_DATO.INT
            temporal = self.generarTemp()
            self.CodigoGenerado += '\t'+temp+'= !'+str(temp)+'\n'
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

    def procesar_inicioPila(self,instr,ts):
        pila = TS.Simbolo(instr.id,td.PILA,[],self.Etiqueta)
        if ts.existeSimbolo(pila):
            print('La pila ya existe')
            err = 'Error el valor ',instr.id,'La pila ya existe',' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            self.errores.append(err) 
        else:
            ts.agregar(pila)

    def procesar_main(self, instr, ts):
        self.CodigoGenerado += "main:"+"\n"

        for sent in instr.sentencias:
            if isinstance(sent,Imprimir): self.procesar_imprimir(sent,ts)
            else:
                print('error, sentencia no posible de realizar')

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
        
        self.Etiqueta=str(instr.id)

    def Llamada_goto(self,instr,ts,listasiguientes):  
        siguientes = []
        i = 0
        for ins in listasiguientes:
            if isinstance(ins,Label):
                self.Etiqueta = str(instr.id)
                if ins.id == instr.id:
                    siguientes = listasiguientes[i+1:]
                    self.ejecutar_expresiones_label(siguientes,ts,listasiguientes)
                    return
            i = i+1
        return

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

    def procesar_instrucciones(self,instrucciones, ts) :
        ## lista de instrucciones recolectadas
            for instr in instrucciones :
                if isinstance(instr, Main) : self.procesar_main(instr,ts)
                elif isinstance(instr, Definicion) : self.procesar_definicion(instr, ts)
                #elif isinstance(instr, Asignacion) : self.procesar_asignacion(instr, ts)
                #elif isinstance(instr, Mientras) : self.procesar_mientras(instr, ts)
                #elif isinstance(instr, If) : 
                #elif isinstance(instr, IfElse) : self.procesar_if_else(instr, ts)
                #elif isinstance(instr, Unset) : self.procesar_unset(instr,ts)
                #elif isinstance(instr,AsignaPunteroPila): self.procesar_asignacion_punteropila(instr,ts)
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
        eti = 'Label'+str(self.contLabel)+":"
        self.contLabel+=1
        return eti

a = Ejecucion_MinorC()

f = open("./entrada.txt", "r")
input = f.read()
a.ejecutar_asc(input)
print(a.CodigoGenerado)
