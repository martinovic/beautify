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
    Ultima modificacion: 7-dic-2012
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
            if len(fmtString.strip()) > 0:
                if fmtString.lstrip().startswith('def'):
                    fhOut.write('\r\n')

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

        if len(line) > 79 and line.lstrip().startswith('#'):
            line = self.spaces(line) + "# Comentario removido\r\n"

        if len(line) > 79 and line.lstrip().startswith('##'):
            line = self.spaces(line) + "# Comentario removido\r\n"

        a = line

        a = a.replace(' _value = ', '\r\n' + self.spaces(line) + '_value=')
        a = a.replace(' _style = ', '\r\n' + self.spaces(line) + '_style=')
        a = a.replace(' _id = ', '\r\n' + self.spaces(line) + '_id=')
        a = a.replace(', wx.', ',\r\n' + self.spaces(line) + 'wx.')
        a = a.replace('(wx.', '(\r\n' + self.spaces(line) + 'wx.')
        a = a.replace('| wx.', '|\r\n' + self.spaces(line) + 'wx.')
        if not a.lstrip().startswith('def'):
            a = a.replace('(self', '(\r\n' + self.spaces(line) + 'self')
        a = a.replace(', dict(', ',\r\n' + self.spaces(line) + 'dict(')
        a = a.replace(':', ': ')
        a = a.replace(':  ', ': ')

        if len(a) > 79:
            if '\r\n' not in a:
                # evita la situacion de un split(',')
                if "split(',')" not in a:
                    a = a.replace(',', ',\r\n' + self.spaces(line))

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

        try:
            veces = a.count('{')
            for vez in range(veces):
                numSpc = 0
                pos1 = a.index('{') + 1
                for x in range(pos1, len(a)):
                    if a[x] == ' ':
                        numSpc += 1
                    else:
                        break
                buscado = '{' + ' ' * (numSpc)
                a = a.replace(buscado, '{')
        except:
            pass

        # Para los casos de if, else, def y class
        if a.lstrip().startswith('for'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('if'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('else'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('class'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('try'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('except'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('def'):
            a = a.replace(': ', ':')
            a = a.replace(' = ', '=')

        if a.count('=') > 1:
            b = a[::-1]
            a = b.replace(' = ', '=', ((b.count('=')) - 1))[::-1]

        try:
            pos1 = a.index("'")
            pos2 = a[pos1 + 1:].index("'")
            subStr1 = a[pos1 + 1: pos1 + pos2 + 1]
            # si se deben hacer cambios especiales en el substring
            # se aplicaria aqui
            #print(subStr1)
        except:
            if not a.lstrip().startswith('if'):
                a = a.replace('-', ' - ')
                a = a.replace('  -  ', ' - ')

                a = a.replace('+', ' + ')
                a = a.replace('  +  ', ' + ')

                a = a.replace('/', ' / ')
                a = a.replace('  /  ', ' / ')

                #a = a.replace(',', ', ')
                a = a.replace(',  ', ', ')

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
