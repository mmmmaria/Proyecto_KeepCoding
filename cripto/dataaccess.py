import sqlite3
from config import PATH_TO_DATABASE

class DBManager():
        
    def __toDict__(self, cur):
        # Obtenemos los datos de la consulta
        claves = cur.description
        filas = cur.fetchall()

        # Procesar los datos para devolver una lista de diccionarios. Un diccionario por fila
        resultado = []
        for fila in filas:
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]] = valor
            resultado.append(d)

        return resultado

    def consultaSQL(self, query, parametros=[]):
        # Abrimos la conexion
        conexion = sqlite3.connect(PATH_TO_DATABASE)
        cur = conexion.cursor()

        # Ejecutamos la consulta
        cur.execute(query, parametros)
        resultado = self.__toDict__(cur)
        conexion.close()
        return resultado

    def modificaTablaSQL(self,query,parametros=[]):
        conexion=sqlite3.connect(PATH_TO_DATABASE)
        cur=conexion.cursor()
        cur.execute(query,parametros)

        conexion.commit()
        conexion.close()
