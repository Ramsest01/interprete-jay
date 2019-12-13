# -*- coding: utf-8 -*-
"""
	Estudiate:
        Estéfano Ramos
        V-26778542

    Especificacion EBNF

	    <InputElement>::= <Espacio en blanco> | <Comentario> | <Token>
        <Espacio en blanco>::= ' ' | '\t' | '\r' | '\n' | '\f'
        <Comentario>::='//' <cadena>  ('\r' | '\n')
        <Token>::= <Identificador> | <Reservada> | <Literal> | <Separador> | <Operardor>
        <Identificador>::=<Letra> { <Letra> | <Digito>}*
        <Letra>::= 'a' | 'b '| … | 'z' | 'A' | 'B' | …. | 'Z'
        <Digito>::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        <Reservada>::='boolean' | 'else' | 'if' | 'int' | 'main' | 'void' | 'while'
        <Literal>::= <Boleano> | <Entero>
        <Boleano>::= 'true' | 'false'
        <Entero>::= <Digito> {<Digito>}*
        <Separador>::= '(' | ')' | '{' | '}' | ';' | ','
        <Operador>::= '=' | '+' | '-' | '*' | '/' | '<' | '<=' | '>' | '>=' | '==' | '!=' | '&&' | '||' | '!'
        
        <Programa>::= 'void' 'main' '(' ')' '{' <Declaraciones><Statements> '}'
        <Declaraciones>::= { <Declaracion> }*
        <Declaricon>::= <Tipo> <Identificadores>';'
        <Tipo>::= 'int' | 'boolean'
        <Identificadores>::= <Identificador> { ',' <Identificador> }*
        <Statements>::= { <Statement> }*
        <Statement>::= <Bloque> | <Asignacion> |<IfStatement> | <WhileStatementk>
        <Bloque>::= '{'<Statements>'}' 
        <Asignacion>::= <identificador>'='<Exprecion>';'
        <IfStatement>::= 'if' '(' <Exprecion>')' <Statement> [ 'else' <Statement>]
        <WhileStatementk>::= 'while' '(' <Expression> ')' <Statement>
        <Exprecion>::= <Conjuncion> { '||' <Conjunction> }*
        <Conjuncion>::= <Relacion> { '&&' <Relacion>}*
        <Relacion>::= <Adicion> { ('<' |'<='|'=='|'>='|'>'|'!=') <Adicion>}*
        <Adicion>::=<Termino> { ('+'|'-') <Termino>}*
        <Termino>::=<Negacion> { ('*'|'/') <Negacion>}*
        <Negacion>::=['!'] <Factor>
        <Factor>::= <Identificador>| <Literal>| '('<Exprecion>')'

Nota: Los nombres de los simbolos terminales y no terminales fueron remplazados por funciones equivalentes en el programa.
        
"""	

#Conseguir la direccion del archivo "FUENTE.PSE"

import os
ruta=os.path.dirname(os.path.abspath(__file__))
ruta=ruta+'\FUENTE.PSE'

print "Interprete del lenguaje de programacion Jay:"
print
print"A continuacion se procedera a leer el archivo 'FUENTE.PSE', precione Enter para comenzar"

raw_input()

#Tratar de abrir de abrir el archivo en la ruta obtenida.

try:
    archivo = open(ruta)
    print"Archivo 'FUENTE.PSE' encontrado exitosamente, precione Enter para continuar"
    raw_input()
except Exception as error:
    print"Error al abrrir el archivo:",error

#Variables a usar en el programa.

#Lista de almacenamiento temporal de los tokens.
ltokens=[]
#Lista de almacenamiento de las variables declaradas y sus valores a lo largo de la ejecucion.
variables=[]
#Variable global que almacena el posicionamiento actual.
pos=0
puntero=-1

#Lista con los tipos de tokens para el analisis lexico.
ws=["\n","\t","\r","\f"," "]
separadores=["(",")","{","}",";",","]
operadores= ["+","-","*","/","=",">","<","!","<=",">=","==", ("!"+"="), ("&"+"&") , ("|"+"|")]
reservadas=["boolean", "else", "if", "int", "main", "void", "while"]
booleano=["true", "false"]

#clase donde seran almacenado los tokens, su valor y tipo.
class Token:
    def __init__(self, tipo, valor):
        self.valor = valor
        self.tipo = tipo

#clase donde se almacenan las variables, su tipo, el nombre del identificador, el valor que pueden tener y la linea que aparecieron o se hizo un cambio.
class Variable:
     def __init__(self, tipo="", nombre="", valor="", linea=""):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.nombre = nombre

#Metodo que comprueba si una cadena es un identificador valido.
def esId(cad):
    resultado = True
    if cad[0].isalpha(): 
        if len(cad)>1:
            if not cad[1:].isalnum():            
                resultado = False  
    else:
        resultado = False
    return resultado

#Analizador lexico recive una cadena y verifica caracter por caracte ignora los espacios en blanco si existen tokens validos y los retorna en una lista.
def lexico(cadena):

    lista = []
    aux=""
    i=0

    #Funcion local para validar si una cadena es una reservada, un identificador o un literal, en caso contrario detiene el programa por un error lexico.
    def validar(cadena):
        if cadena:                          
            if cadena not in reservadas:
                if cadena not in booleano:
                    if not esId(cadena):
                        if not cadena.isdigit():
                            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
                        else:
                            salida=Token("numero",cadena)
                            lista.append(salida)
                    else:
                        salida=Token("identificador",cadena)
                        lista.append(salida) 
                else:
                    salida=Token("booleano",cadena)
                    lista.append(salida)  
            else:
                salida=Token("reservada",cadena)
                lista.append(salida) 
        return ""               

    #Al no ser un espacio en blanco se almacena los caracteres hasta encontrar un separador, un operador o un espacio en blanco para proceder a validar la cadena almacenada.
    if cadena:
        while i < len(cadena):
            if cadena[i] not in ws:
                if cadena[i]=="/" and cadena[i+1]=="/":
                    while( cadena[i]!="\n" and cadena[i]!="\r"):
                        i+=1
                else:
                    if cadena[i] in separadores: 
                        aux=validar(aux)
                        aux+=cadena[i]
                        salida=Token("separador",aux)
                        lista.append(salida) 
                        aux=""
                        i+=1
                    elif cadena[i] in operadores or cadena[i]+cadena[i+1] in operadores:
                        if cadena[i]+cadena[i+1] not in operadores:
                            aux=validar(aux)
                            aux+=cadena[i]
                            salida=Token("operador",aux)
                            lista.append(salida) 
                            aux=""
                            i+=1
                        else:
                            aux=validar(aux)
                            aux+=cadena[i]+cadena[i+1]
                            salida=Token("operador",aux)
                            lista.append(salida) 
                            aux=""
                            i+=2
                    else:
                        aux+=cadena[i]
                        i+=1
            else:
                aux=validar(aux)
                i+=1
    
    #La lista local se le asigna a la lista global donde se alamacena los tokens obtenidos.
    ltokens.extend( lista)

#Funcion que retorna el token siguiente en la lista y si la lista esta vacia se procede con en el analisis lexico en la siguiente linea del programa.
def nex_t():
    global pos
    global puntero
    aux=None
    
    if (len(ltokens)-1 > puntero):
        puntero+=1          
        aux = ltokens[puntero]
    else:       
        if pos>0:
            mostrar()
        pos+=1
        linea = archivo.readline()
        if linea:
            lexico(linea)
            aux = nex_t()
    return aux

#Funcion principal program verifica los tokens iniciales (void main () {) para iniciar la validacion y ejecucion de las declaraciones y los Statements y finalizar la ejecucion con '}'
#Si aun hay tokens en la lista es porque hubo en error sintactico en la ejecucion.
def program():
    
    for exp in ["void","main","(",")","{"]:
        t = nex_t()
        if t.valor!=exp:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
   
    t = nex_t()
                        
    t=declaraciones(t)
                        
    t=statamens(t)
                        
    if(t.valor=="}"):
        if nex_t() != None:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        print
        print("Fin de la ejecucion.")
    else:
        raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
    
#declaraciones recive el token actual y comprueba si es una palabra reservada que coincida con un tipo de dato y si tiene un identificador o identificador mas ',' identificador
#para agregarlos a la tabla de variables con su tipo de dato. Retorna el siguiente token a evaluar.
def declaraciones(tok):
    t=tok
    while t.valor=="int" or t.valor=="boolean":
        var = Variable(t.valor)
        tipo= t.valor
        t= nex_t()
        if t.tipo == "identificador":
            var.nombre=t.valor
            var.linea=pos
            variables.append(var)
            t= nex_t()
            while t.valor==",":
                t= nex_t()
                if t.tipo == "identificador":
                    var = Variable(tipo,t.valor,linea=pos)
                    variables.append(var)
                    t= nex_t()                    
                else:
                    raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
            if t.valor!=";":
                raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        else:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        t = nex_t()
    return t

#Revisa y se puede fomar un statement comparando si podria ser un bloque, una asignacion, una setencia if o while. retorna el token que aun no se ha usado.
def statamens(tok,enc=True):
    t=tok
    while t.valor=="{" or t.tipo == "identificador" or t.valor=="if" or t.valor=="while":
       t=statament(t,enc)          
    return t

#Al confimar que tiene forma de statement se divide en el caso a evaluar un bloque, una asignacion, una setencia if o while.
def statament(tok,enc=True):
    t=tok
    #bloque valido '{' Statement '}'
    if t.valor=="{":
        t= nex_t()
        t=statamens(t,enc)
        if t.valor=="}":
            t= nex_t()
        else:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
    #Al ver que es un identificador se procede a evaluar la asigncaion para obtener el valor de la exprecion y asignarselo al identificador en la tabla de variables
    elif t.tipo == "identificador":
        id=t.valor
        t, salida=asignacion(t)
        if enc:
            asignar(id, salida)
        t= nex_t()
    #Una exprecion if evalua '(' exprecion ')' si el resultado de esta es "true" deja activo el statement para que pueda ejecutarse y si el estatement da como resultado un token 'else'
    # se evalua sintacticamente y dependiendo del resultado de la exprecion se ejecuta, siempre es uno o el otro nunca los dos.        
    elif t.valor=="if":
        t= nex_t()
        if t.valor =="(":
            t= nex_t()
            t, salida=exprecion(t)
            if t.valor ==")":
                t= nex_t()
                act=False
                if enc and salida=="true":
                    act=True
                t=statament(t,act)
                if t.valor=="else":
                    t= nex_t()
                    t=statament(t,not act)
            else:
                raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        else:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos)) 
    #Se comprueba que sea una exprecion while valida y la ejecuta   
    elif t.valor=="while":
        global puntero
        t= nex_t()
        if t.valor =="(":
            x=0
            if enc:
               x=puntero
            t= nex_t()
            t, salida=exprecion(t)
            if t.valor ==")":
                act=False
                if enc and salida=="true":
                    act=True           
                t= nex_t()                                                       
                t=statament(t,act)
                if act:                              
                    i=1
                    while salida=="true":
                        puntero=x
                        t= nex_t()
                        t, salida=exprecion(t)
                        if t.valor ==")":
                            act=False
                            if enc and salida=="true":
                                act=True           
                            t= nex_t()                                                       
                            t=statament(t,act)
                            if enc and salida=="true":
                                mostrar(i)                      
                        i+=1
                    
            else:
                raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        else:
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
    return t  

#verifica si una asignacion es valida, Asignacion valida identificador '=' (exprecion)';'
def asignacion(tok):
    t=tok
    t=nex_t()
    if t.valor=="=":
        t= nex_t()
        t, salida= exprecion(t)
    else:
        raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
    return t, salida

#verifica que la exprecion tenga la forma conjucion o varios conjucion || conjuncion y ejecuta la operaciones logicas.
def exprecion(tok):
    t=tok
    t,salida=conjuncion(t)
    while t.valor=="|"+"|":
        t= nex_t()
        t,r=conjuncion(t)
        if salida !="false" or r!="false":
            salida="true"
        else:
            salida="false"
    return t,salida

#verifica que la conjucion tenga la forma relacion o varios relacion && relacion y ejecuta las operaciones logicas.
def conjuncion(tok):
    t=tok
    t,salida=relacion(t)
    while t.valor=="&"+"&":
        t= nex_t()
        t,r=relacion(t)
        if salida!="false" and r!="false":
            salida="true"
        else:
            salida="false"
    return t, salida

#verifica que la relacion tenga la forma adicion o varios adicion (operadores logicosde mayor menor igual diferente) adicion y ejecuta la operaciones logicas.
def relacion(tok):
    t=tok
    t, salida=adicion(t)
    while t.valor in ["<","<=","==",">=",">","!="]:
        op=t.valor
        t= nex_t()
        t,r=adicion(t)
        if op=="<":
            if(int(salida) < int(r)):
                salida="true"
            else:
                salida="false"
        elif op=="<=":
            if(int(salida) <= int(r)):
                salida="true"
            else:
                salida="false"
        elif op=="==":
            if(salida == r):
                salida="true"
            else:
                salida="false"
        elif op== ">":
            if(int(salida) > int(r)):
                salida="true"
            else:
                salida="false"
        elif op== ">=":
            if(int(salida) >= int(r)):
                salida="true"
            else:
                salida="false"
        elif op== "!=":
            if(salida != r):
                salida="true"
            else:
                salida="false"
       
    return t, salida

#verifica que la adicion tenga la forma termino o varios termino + o - termino y ejecuta las operaciones.
def adicion(tok):
    t=tok
    t, salida=termino(t)
    while t.valor in ["+","-"]:
        op=t.valor
        t= nex_t()
        if op=="+":
            t,r=termino(t)
            ext=int(salida)+int(r)
        else:
            t,r=termino(t)
            ext=int(salida)-int(r)
        salida=str(ext)
    return t,salida

#verifica que el termino tenga la forma negacion o varios negacion * o / negacion y ejecuta las operaciones.
def termino(tok):
    t=tok
    t, salida=negacion(t)
    while t.valor in ["*","/"]:
        op=t.valor
        t= nex_t()
        if op=="*":
            t,r=negacion(t)
            ext=int(salida)*int(r)
        else:
            t,r=negacion(t)
            ext=int(salida)/int(r)
        salida=str(ext)
    return t, salida

#verifica que la negacion tenga la forma '!' factor y ejecutar la operacion logica o factor.
def negacion(tok):
    t=tok
    if t.valor=="!":
        t=nex_t()
        t,salida=factor(t)
        if salida=="false":
            salida="true"
        else:
            salida="false"
    else:
        t, salida=factor(t)
    return t, salida

#verifica que el factor sea un identificador o '(' exprecion ')' o un literal.
def factor(tok):
    t=tok
    salida=0
    if t.tipo=="identificador":
        salida=consultar(t.valor)
        t=nex_t()
    elif t.valor=="(":
        t=nex_t()
        t, salida=exprecion(t)
        if t.valor!=")":
            raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
        t=nex_t()
    elif t.tipo in ["booleano","numero"]:
        salida= t.valor
        t=nex_t()
    else:
        raise Exception("LINEA {}: Error lexico/sintaxis".format(pos))
    return t, salida

#Procedimiento que actualiza los valores de las variables en la lista.    
def asignar(id, valor):
    for v in variables:
        if v.nombre==id:
            v.valor=valor
            v.linea=pos

#Funcion que retorna el valor de una varible en la lista.
def consultar(id):
    for v in variables:
        if v.nombre==id:
             return v.valor

#Procedimiento que muestra los valores en la lista de variables
def mostrar(i=0):
    if i>0:
        print
        print "Tabla de variables en la iteracion:", i
    else:
        print
        print "Tabla de variables en la linea:",pos
    print
    print "{:^10}{:^10}{:^15}{:^10}".format("linea:", "tipo:","identificador:","valor:")
    for var in variables:
        print "{:^10}{:^10}{:^15}{:^10}".format(var.linea, var.tipo, var.nombre, var.valor)
    print
    print "Presione la tecla Enter para continuar...",
    raw_input()

#Aqui iniciamos el analisis sintactico para poder iniciar el analisis lexico, y asi poder ejecutar el codigo.    
try:
    program()
#Al encontrar un error Lexico / sintactico mostrarlo al usuario 
except Exception as error:
    print(error)
    raw_input()
finally:
    archivo.close()


