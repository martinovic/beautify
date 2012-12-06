#!/usr/bin/env python
# -*- coding: utf-8 -*-

__prj__ = 'beautify'
__version__ = '0.1'
__license__ = 'GNU General Public License v3'
__author__ = 'marcelo'
__email__ = 'marcelo@marcelo-Inspiron-N4030'
__url__ = ''
__date__ = '2012/12/06'

import sys


class Beauty:
    '''
    Esta clase permite limpiar y ordenar las clases cuando estan en un
    archivo sabana.
    Por ahora es valido solo para mis archivos de WxPython, pero se podria
    adaptar para otros con mucha facilidad.
    Aun le falta mucho a este codigo.
    '''
    def __init__(self, fileToClean):
        '''
            Descripcion de la clase o metodo
            @param fileToClean:
            @type string:
            @return: void
        '''

        with open(fileToClean, 'r') as fh:
            contenido = fh.readlines()

        self.headList = []
        listaClases = []

        # Armado del head de los archivos a generar
        for line in contenido:
            # si la linea inicia con class podemos
            # decir que ya termina el area de imports
            if line.startswith("class"):
                break
            self.headList.append(line)
        headSize = len(self.headList)
        contenido[0: headSize - 1] = []
        className = ""
        pos = 0
        # Armado de una lista que indica donde inicia y termina una clase
        # asi como el nombre de la misma
        for line in contenido:
            # Ahora si la linea inicia con class guardamos cual esel indice
            # en la lista y le agregamos el nombre de la clase a una nueva
            # lista
            if line.startswith("class"):
                className = line[len('class '):line.index('(')]
                indice = contenido.index(line)
                listaClases.append([className, indice])

        lastLine = 0

        # Armado de la llamada para hacer que escriba de una linea de inicio
        # a una final
        for v in listaClases:
            pos = listaClases.index(v)
            prox = pos + 1
            # aqui se calcula la linea-1 que es donde terminaria
            # la clase, si el indice da error deberia poder decir que es la
            # ultima clase y tomamos como ultima linea la cantidad
            # de elementos de la lista
            try:
                lastLine = listaClases[prox][1] - 1
            except:
                lastLine = len(contenido)

            # para escribir la clase
            self.writeFiles(listaClases[pos][0],
                listaClases[pos][1],
                lastLine,
                contenido)

    def writeFiles(self, className, fromLine, toLine, listData):
        '''
            Escribe el archivo de la clase
            @param className: nombre de la clase
            @type string:
            @param fromLine: inicio de la clase
            @type int:
            @param toLine: fin de la clase -1
            @type int:
            @param listData: lista de elementos
            @type list:
            @return: void
        '''
        fileOut = className + ".py"
        fhOut = open(fileOut, 'w')

        for line in self.headList:
            fhOut.write(line)
        fhOut.write("\r\n\r\n")

        for line in listData[fromLine: toLine]:
            fmtString = self.formateadorPEP8(line)
            fhOut.write(fmtString)
            # agrega documentacion
            if fmtString.lstrip().startswith('class'):
                doc = "    \'\'\'\r\n"
                doc += "    Clase " + className + "\r\n"
                doc += "    \'\'\'\r\n"
                fhOut.write(doc)

            if fmtString.lstrip().startswith('def'):
                doc = "        \'\'\'\r\n"
                doc += "            Descripcion de la clase o metodo\r\n"
                doc += "            @param __VARIABLE__:\r\n"
                doc += "            @type __TIPO__:\r\n"
                doc += "            @param __VARIABLE__:\r\n"
                doc += "            @type __TIPO__:\r\n"
                doc += "            @return: void\r\n"
                doc += "        \'\'\'\r\n"
                fhOut.write(doc)
        fhOut.close()

    def formateadorPEP8(self, line):
        '''
            formatea lo mejor posible a PEP8
            @param line:
            @type string:
            @return: string
        '''
        # Remplaza y arregla para que cumpla PEP8
        a = line.replace(',', ', ')
        a = a.replace(',  ', ', ')

        a = a.replace('-', ' - ')
        a = a.replace('  -  ', ' - ')

        a = a.replace('+', ' + ')
        a = a.replace('  +  ', ' + ')

        a = a.replace('/', ' / ')
        a = a.replace('  /  ', ' / ')

        a = a.replace(' _value = ', '\r\n' + self.spaces(line) + '_value=')
        a = a.replace(' _style = ', '\r\n' + self.spaces(line) + '_style=')
        a = a.replace(' _id = ', '\r\n' + self.spaces(line) + '_id=')
        a = a.replace('(cols = ', '(cols=')
        a = a.replace('hgap = ', 'hgap=')
        a = a.replace('vgap = ', 'vgap=')
        a = a.replace('0, wx.', '0,\r\n' + self.spaces(line) + 'wx.')
        a = a.replace('| wx.', '|\r\n' + self.spaces(line) + 'wx.')
        if not a.lstrip().startswith('def'):
            a = a.replace('(self', '(\r\n' + self.spaces(line) + 'self')
        a = a.replace(', dict(', ',\r\n' + self.spaces(line) + 'dict(')
        a = a.replace(':', ': ')
        a = a.replace(':  ', ': ')


        if a.lstrip().startswith('if'):
            if '== True' in a:
                a = a.replace('== True', '')
            if '== False' in a:
                a = a.replace('== False', '')
                a = a.replace('if ', 'if not ')

            a = a.replace('==', ' == ')
            a = a.replace('  ==  ', ' == ')

            a = a.replace('>=', ' >= ')
            a = a.replace('  >=  ', ' >= ')

            a = a.replace('<=', ' <= ')
            a = a.replace('  <=  ', ' <= ')

            a = a.replace('!=', ' != ')
            a = a.replace('  !=  ', ' != ')

        a = a.replace('+=', ' += ')
        a = a.replace('  +=  ', ' += ')

        a = a.replace('( ', '(')
        a = a.replace(' )', ')')

        a = a.replace('{ ', '{')
        a = a.replace(' }', '}')

        # Para los casos de if, else, def y class
        if a.lstrip().startswith('if'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('else'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('class'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('def'):
            a = a.replace(': ', ':')
            a = a.replace(' = ', '=')

        return a

    def spaces(self, line):
        '''
            Calcula la cantidad de espacios y le suma 4 mas
            Para que el identado quede prolijo
            @param line:
            @type string:
            @return: string
        '''
        cantidad = len(line) - len(line.lstrip())
        return (" " * cantidad) + "    "

if __name__ == '__main__':
    Beauty(sys.argv[1])

