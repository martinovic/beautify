#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

class Beauty:
    '''
    '''
    def __init__(self):
        '''
            Descripcion de la clase o metodo
            @param __VARIABLE__:
            @type __TIPO__:
            @param __VARIABLE__:
            @type __TIPO__:
            @return: void
        '''

        with open('LDP.py', 'r') as fh:
            contenido = fh.readlines()

        self.headList = []
        listaClases = []

        # Armado del head de los archivos a generar
        for line in contenido:
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
            try:
                lastLine = listaClases[prox][1] - 1
            except:
                lastLine = len(contenido)

            self.writeFiles(listaClases[pos][0],
                listaClases[pos][1],
                lastLine,
                contenido)

    def writeFiles(self, className, fromLine, toLine, listData):
        '''
            Escribe el archivo de la clase
            @param __VARIABLE__:
            @type __TIPO__:
            @param __VARIABLE__:
            @type __TIPO__:
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
        a = line.replace(' _value = ', '\r\n            _value=')
        a = a.replace(' _style = ', '\r\n            _style=')
        a = a.replace(' _id = ', '\r\n            _id=')
        a = a.replace('(cols = ', '(cols=')
        a = a.replace('hgap = ', 'hgap=')
        a = a.replace('vgap = ', 'vgap=')
        a = a.replace('0, wx.', '0,\r\n            wx.')
        a = a.replace('| wx.', '|\r\n            wx.')
        if not a.lstrip().startswith('def'):
            a = a.replace('(self', '(\r\n            self')
        a = a.replace(', dict(', ',\r\n                dict(')
        a = a.replace(':', ': ')
        a = a.replace(':  ', ': ')

        # Para los casos de if, else, def y class
        if a.lstrip().startswith('if'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('else'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('class'):
            a = a.replace(': ', ':')

        if a.lstrip().startswith('def'):
            a = a.replace(': ', ':')

        return a

if __name__ == '__main__':
    Beauty()

