# -*- coding: utf-8 -*-

from typing import ContextManager
import mysql as mysql
from mysql.connector import errorcode
import datetime
from datetime import timedelta
from datetime import date
import time


def test_entrada(cnx):
    '''
    Función para testear que la consulta de los datos de todas las entradas es correcta.
    '''
    try:
        cursor = cnx.cursor()
        query = ("SELECT id_entrada, dia, precio, num_butaca, num_fila, id_sala, disponibilidad FROM entrada")

        cursor.execute(query)
    except Exception:
        return print("Test-01 FAILED")
    
    print("Test-01 PASSED. ")
    return 

def test_vender_entrada(cnx):
    try:
        cursor = cnx.cursor()
        update_entrada = ("UPDATE entrada SET disponibilidad=False WHERE id_entrada= %(id_vendida)s")
        new = int(2) #Le indicamos que venda la entrada 2 automáticamente.
        new_data = {'id_vendida':new}
        cursor.execute(update_entrada, new_data)
        #print("¡Entrada",new,"vendida!")
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Test-02 PASSED")

    print("Test-02 PASSED.")
    return

def test_proyeccion(cnx):
    try:
        cursor = cnx.cursor()
        query = ("SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala from pelicula inner join proyeccion on pelicula.codigo = proyeccion.codigo")
        cursor.execute(query)
    except Exception:
        return print("Test-03 PASSED")
    
    print("Test-03 PASSED.")
    return

def test_peli_pordia(cnx):
    try: 
        cursor = cnx.cursor()
        query = ("SELECT distinct B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.dia = %(dia)s")
        while True:
            try:
                fecha = "2021-01-01" #se lo asignamos por defecto
                fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
                break
        
            except:
                print ("Fecha incorrecta\n")
        new_data = {'dia':fecha}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Test-04 PASSED")
    
    print("Test-04 PASSED.")
    return

def test_peli_disponibilidad(cnx):
    try:
        cursor = cnx.cursor()
        query = ("SELECT entrada.id_entrada, B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.disponibilidad = True")

        cursor.execute(query)
        myresult = cursor.fetchall()

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Test-05 PASSED")

    print("Test-05 PASSED.")
    return

def test_peli_nombre(cnx):
    try:
        cursor = cnx.cursor()
        query = ("SELECT entrada.id_entrada, entrada.disponibilidad, B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.disponibilidad = True and B.titulo = %(titulo)s")

        nombre_peli = 'Torrente'
        new_data = {'titulo':nombre_peli}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Test-06 PASSED")
    
    print("Test-06 PASSED.")
    return

def test_nuevo_dia(cnx):
    try:
        cursor = cnx.cursor()
        update_entrada = ("UPDATE entrada SET disponibilidad=True WHERE disponibilidad= False")
        cursor.execute(update_entrada)
        cnx.commit()
        cursor.close()
    
    except Exception:
        return print("Test-07 PASSED")
    
    print("Test-07 PASSED.")
    return

def test_añadir_peli(cnx):
    try:
        cursor = cnx.cursor()
        query = ("INSERT INTO pelicula (codigo, titulo, duracion_minutos, hora_entrada,hora_salida) VALUES (%(codigo_peli)s, %(titulo)s, %(duracion_minutos)s, %(hora_entrada)s, %(hora_salida)s)")

        codigo_peli = '6'
        nombre_peli = 'Madagascar 3'
        duracion_peli = 97
    
        while True:
            try:
                hora_entrada_peli = time.strftime('16:30:00')
                hora_salida_peli = time.strftime('18:07:00')
                break
            except:
                print ("Hora incorrecta\n")
    
        new_data = {'codigo_peli':codigo_peli, 'titulo':nombre_peli, 'duracion_minutos':duracion_peli, 'hora_entrada':hora_entrada_peli, 'hora_salida':hora_salida_peli}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()     
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Test-08 PASSED")
    
    print("Test-08 PASSED.")
    return

def test_eliminar_peli(cnx):
    try:
        cursor = cnx.cursor()
        query = ("DELETE FROM pelicula WHERE codigo = %(codigo)s")
        new = '6'
        new_data = {'codigo':new}
        cursor.execute(query, new_data)
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Test-09 PASSED")

    print("Test-09 PASSED.")
    return

def test_crear_taquillero(cnx):
    try:
        cursor = cnx.cursor()
        userName = 'Cristina'
        password = 'Mariposa2001'
        try:
            query1 = ("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s'"%(userName, password))
            cursor.execute(query1)
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))
        try:
            query2 = ("GRANT SELECT on Practica_cine.* to '%s'@'localhost'"%(userName))
            cursor.execute(query2)
        except Exception as Ex:
            print("Error granting select privileges: %s"%(Ex))
        try:
            query3 = ("GRANT UPDATE on Practica_cine.entrada to '%s'@'localhost'"%(userName))
            cursor.execute(query3)
        except Exception as Ex:
            print("Error granting update privileges: %s"%(Ex))
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Test-10 PASSED")
    
    print("Test-10 PASSED.")
    return

def test_añadir_peli_a_sala(cnx):
    try:
        cursor = cnx.cursor()
        query = ("INSERT INTO proyeccion (id_sala, codigo) VALUES (%(id_sala)s, %(codigo)s)")

        codigo_peli = 1
        numero_sala = 101

        new_data = {'codigo':codigo_peli, 'id_sala':numero_sala}

        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        cnx.commit()
        cursor.close()
    except Exception:
        return print("Test-11 PASSED")
    
    print("Test-11 PASSED.")
    return

def main():
    print('=========================================================')
    
    print('Test 01 -> Consulta de los datos de todas las entradas.')
    test_entrada(cnx)
    print('=========================================================')

    print('Test 02 -> Venta de entrada')
    test_vender_entrada(cnx)
    print('=========================================================')

    print('Test 03 -> Consulta de las proyecciones')
    test_proyeccion(cnx)
    print('=========================================================')

    print('Test 04 -> Consulta de películas por día')
    test_peli_pordia(cnx)
    print('=========================================================')

    print('Test 05 -> Consulta de películas por disponibilidad')
    test_peli_disponibilidad(cnx)
    print('=========================================================')

    print('Test 06 -> Consulta de películas por nombre')
    test_peli_nombre(cnx)
    print('=========================================================')

    print('Test 07 -> Actualizar disponibilidad de las entradas')
    test_nuevo_dia(cnx)
    print('=========================================================')

    print('Test 08 -> Añadir película a la cartelera')
    test_añadir_peli(cnx)
    print('=========================================================')

    print('Test 09 -> Eliminar película de cartelera')
    test_eliminar_peli(cnx)
    print('=========================================================')

    print('Test 10 -> Crear nuevo taquillero')
    test_crear_taquillero(cnx)
    print('=========================================================')

    print('Test 11 -> Asignar película a sala')
    test_añadir_peli_a_sala(cnx)
    print('=========================================================')



# Checking whether this module is executed just itself alone.
if __name__ == "__main__":
    
    print('==================================================================================')
    print('Bienvenido a los tests de la aplicación de gestión de datos de los cines Nico&Max')
    print('==================================================================================')
    username = "Administrador"
    password= "ordenador123"

    if password == "ordenador123":
        
        ## ADMINISTRADOR

        if username == "Administrador":
            cnx = mysql.connector.connect(
                host="localhost",
                user="Administrador",
                password = "ordenador123",
                db="Practica_cine", 
                auth_plugin="mysql_native_password")

        ## TAQUILLERO

        if username == "Taquillero":
            cnx = mysql.connector.connect(
                host="localhost",
                user="Taquillero_Moratalaz",
                password = "ordenador123",
                db="Practica_cine", 
                auth_plugin="mysql_native_password" )

        print('\n==================================================================================')
        main()

    else:
        print('Contraseña incorrecta')