# -*- coding: utf-8 -*-

from typing import ContextManager
import mysql as mysql
from mysql.connector import errorcode
import datetime
from datetime import timedelta
from datetime import date
import time

# Consultar todo de Entrada

def entrada(cnx):
    '''
    Función para consultar los datos de todas las entradas.
    '''
    try:
        cursor = cnx.cursor()
        query = ("SELECT id_entrada, dia, precio, num_butaca, num_fila, id_sala, disponibilidad FROM entrada")

        cursor.execute(query)
        for (id_entrada, dia, precio, num_butaca, num_fila, id_sala, disponibilidad) in cursor:
            print("\nEntrada: {}, Día: {:%d %b %Y} , Precio: {}, Butaca: {}, Fila: {}, Sala: {}, Disp: {} \n-------------------------------------------------------------------------------------".format(id_entrada, dia, precio, num_butaca, num_fila, id_sala, disponibilidad))
    
    except Exception:
        return print("Algo ha salido mal...")

# Vender entrada

def vender_entrada(cnx):
    '''
    Función para vender una entrada y marcarla como no disponible.
    '''
    try:
        cursor = cnx.cursor()
        update_entrada = ("UPDATE entrada SET disponibilidad=False WHERE id_entrada= %(id_vendida)s")
        # Excepción id_vendida
        new = int(input("Introduce id de la entrada vendida: "))
        new_data = {'id_vendida':new}
        cursor.execute(update_entrada, new_data)
        print("¡Entrada",new,"vendida!")
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Algo ha salido mal...")

# Consultar una Proyección

def proyeccion(cnx):
    '''
    Función para consultar los datos de todas las proyecciones.
    '''
    try:
        cursor = cnx.cursor()
        query = ("SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala from pelicula inner join proyeccion on pelicula.codigo = proyeccion.codigo")

        cursor.execute(query)
        for (titulo, duracion_minutos, hora_entrada, hora_salida, id_sala) in cursor:
            print("\nTítulo: {}, Duración: {}, Entrada: {}, Salida: {}, Sala: {} \n-------------------------------------------------------------------------------------".format(titulo, duracion_minutos, hora_entrada, hora_salida, id_sala))
    except Exception:
        return print("Algo ha salido mal...")

# Consulta las películas por día

def peli_pordia(cnx):
    '''
    Función para consultar todas las pelis que se emiten en un día determinado.
    '''
    try: 
        cursor = cnx.cursor()
        query = ("SELECT distinct B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.dia = %(dia)s")

        while True:
            try:
                fecha = input("Introducir fecha aaaa-mm-dd: ")
                fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
                break
        
            except:
                print ("Fecha incorrecta\n")

        new_data = {'dia':fecha}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        for (titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala) in myresult:
            print("\nTítulo: {}, Día: {:%Y %b %d} Duración: {}, Entrada: {}, Salida: {}, Sala: {} \n-----------------------------------------------------------------------------------------------".format(titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala))

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Algo ha salido mal...")

# Consulta películas por disponibilidad

def peli_disponibilidad(cnx):
    '''
    Función para consultar todas las películas disponibles.
    '''
    try:
        cursor = cnx.cursor()
        query = ("SELECT entrada.id_entrada, B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.disponibilidad = True")

        cursor.execute(query)
        myresult = cursor.fetchall()

        for (id_entrada, titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala) in myresult:
            print("\nId entrada: {}, Título: {}, Día: {:%Y %b %d} Duración: {}, Entrada: {}, Salida: {}, Sala: {} \n--------------------------------------------------------------------------------------------------------------".format(id_entrada, titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala))

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Algo ha salido mal...")

# Consulta películas por nombre

def peli_nombre(cnx):
    '''
    Función para consultar las entradas disponibles de una película en concreto.
    '''
    try:
        cursor = cnx.cursor()
        query = ("SELECT entrada.id_entrada, entrada.disponibilidad, B.titulo, entrada.dia, B.duracion_minutos, B.hora_entrada, B.hora_salida, B.id_sala FROM entrada INNER JOIN (SELECT titulo, duracion_minutos, hora_entrada, hora_salida, id_sala FROM pelicula INNER JOIN proyeccion ON pelicula.codigo = proyeccion.codigo) B ON B.id_sala = entrada.id_sala WHERE entrada.disponibilidad = True and B.titulo = %(titulo)s")

        nombre_peli = input("Introduce el nombre de la película ej: Torrente: ")
        new_data = {'titulo':nombre_peli}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        for (id_entrada, disponibilidad, titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala) in myresult:
            print("\nId entrada: {}, Disponibilidad: {}, Título: {}, Día: {:%Y %b %d} Duración: {}, Entrada: {}, Salida: {}, Sala: {} \n--------------------------------------------------------------------------------------------------------------".format(id_entrada, disponibilidad, titulo, dia, duracion_minutos, hora_entrada, hora_salida, id_sala))

        cnx.commit()
        cursor.close()

    except Exception:
        return print("Algo ha salido mal...")


# Al final del dia poner disponibilidad = True

def nuevo_dia(cnx):
    '''
    Función para que al terminar el día, todas las entradas vuelvan a estar disponibles.
    '''
    try:
        cursor = cnx.cursor()
        update_entrada = ("UPDATE entrada SET disponibilidad=True WHERE disponibilidad= False") #Estaría guay cambiar tambien la fecha
        cursor.execute(update_entrada)
        print("¡Preparados para un nuevo día!")
        cnx.commit()
        cursor.close()
    
    except Exception:
        return print("Algo ha salido mal...")

#Añadir película

def añadir_peli(cnx):
    '''
    Función para añadir una nueva película a la carterla.
    '''
    try:
        cursor = cnx.cursor()
        query = ("INSERT INTO pelicula (codigo, titulo, duracion_minutos, hora_entrada,hora_salida) VALUES (%(codigo_peli)s, %(titulo)s, %(duracion_minutos)s, %(hora_entrada)s, %(hora_salida)s)")

        codigo_peli = input("Introduce el codigo de la película: ")
        nombre_peli = input("Introduce el nombre de la película ej: Torrente: ")
        duracion_peli = int(input("Introduce la duración de la película (minutos): "))
    
        while True:
            try:
                hora_entrada_peli = time.strftime(input("Introducir hora entrada H:M:S: "))
                hora_salida_peli = time.strftime(input("Introducir hora salida H:M:S: "))
                break
            except:
                print ("Hora incorrecta\n")
    
        new_data = {'codigo_peli':codigo_peli, 'titulo':nombre_peli, 'duracion_minutos':duracion_peli, 'hora_entrada':hora_entrada_peli, 'hora_salida':hora_salida_peli}
        cursor.execute(query, new_data)
        myresult = cursor.fetchall()
        for (codigo, titulo, duracion_minutos, hora_entrada, hora_salida) in myresult:
                print("\nCódigo: {}, Título: {}, Duración: {}, Entrada: {}, Salida: {}\n--------------------------------------------------------------------------------------------------------------".format(codigo, titulo, duracion_minutos, hora_entrada, hora_salida))
        print("Película añadida")      
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Algo ha salido mal...")

def eliminar_peli(cnx):
    '''
    Función para eliminar una película de la carterla.
    '''
    try:
        cursor = cnx.cursor()
        query = ("DELETE FROM pelicula WHERE codigo = %(codigo)s")
        new = input("Introduce el codigo de la pelicula a eliminar: ")
        new_data = {'codigo':new}
        cursor.execute(query, new_data)
        print("Película eliminada")
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Algo ha salido mal...")

def crear_taquillero(cnx):
    '''
    Función para crear un nuevo perfil de taquillero cuando se contrate a uno.
    '''
    try:
        cursor = cnx.cursor()
        userName = input("Introduce el nombre del nuevo taquillero: ")
        password = input("Introduce una contraseña para el nuevo taquillero: ")
        try:
            query1 = ("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s'"%(userName, password))
            cursor.execute(query1)
            print("Usuario creado")
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))
        try:
            query2 = ("GRANT SELECT on Practica_cine.* to '%s'@'localhost'"%(userName))
            cursor.execute(query2)
            print("Select privileges correctly granted")
        except Exception as Ex:
            print("Error granting select privileges: %s"%(Ex))
        try:
            query3 = ("GRANT UPDATE on Practica_cine.entrada to '%s'@'localhost'"%(userName))
            cursor.execute(query3)
            print("Update privileges correctly granted")
        except Exception as Ex:
            print("Error granting update privileges: %s"%(Ex))
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Algo ha salido mal...")

def añadir_peli_a_sala(cnx):
    '''
    Función para asignar una película a una sala.
    '''
    try:
        cursor = cnx.cursor()
        query = ("INSERT INTO proyeccion (id_sala, codigo) VALUES (%(id_sala)s, %(codigo)s)")

        codigo_peli = int(input("Introduce el codigo de la película: "))
        numero_sala = int(input("Introduce el numero de la sala: "))

        new_data = {'codigo':codigo_peli, 'id_sala':numero_sala}

        cursor.execute(query, new_data)
        myresult = cursor.fetchall()

        for (codigo, id_sala) in myresult:
                print("\nCódigo: {}, id_sala: {}\n--------------------------------------------------------------------------------------------------------------".format(codigo, id_sala))
        
        print("Se ha añadido correctamente")
        cnx.commit()
        cursor.close()
    except Exception:
        return print("Algo ha salido mal...")

def menu():
    try:
        if username=="Taquillero" or username=="Administrador":
            print('==================================================================================')
            print("¡Genial! Estas son sus opciones disponibles:")
            print("0. Cerrar la aplicación.")
            print("1. Imprimir opciones de nuevo.")
            print("2. Vender una entrada.")
            print("3. Consultar la información de las entradas.")
            print("4. Consultar una proyección.")
            print("5. Consultar las películas por día.")
            print("6. Consultar películas por disponibilidad.")
            print("7. Consultar películas por nombre.")
            print("8. Volver a poner en venta las entradas.")  

        if username=="Administrador":
            print("9. Añadir película a la cartelera")
            print("10. Eliminar película de la cartelera")
            print("11. Contratar un taquillero")
            print("12. Asignar película a sala")
        
        print('==================================================================================')
    
    except Exception:
        return print("Algo ha salido mal...")

def main():
    menu()
    while True:
        try:
            operacion = input('Introduce el código de operación a realizar: ')
            if int(operacion)==0:
                return
            elif int(operacion)==1:
                print('\n----------------Opcion 1----------------')
                menu()
            elif int(operacion)==2:
                print('\n----------------Opcion 2----------------')
                entrada(cnx)
                vender_entrada(cnx)
            elif int(operacion)==3:
                print('\n----------------Opcion 3----------------')
                entrada(cnx)
            elif int(operacion)==4:
                print('\n----------------Opcion 4----------------')
                proyeccion(cnx)
            elif int(operacion)==5:
                print('\n----------------Opcion 5----------------')
                peli_pordia(cnx)
            elif int(operacion)==6:
                print('\n----------------Opcion 6----------------')
                peli_disponibilidad(cnx)
            elif int(operacion)==7:
                print('\n----------------Opcion 7----------------')
                peli_nombre(cnx)
            elif int(operacion)==8:
                print('\n----------------Opcion 8----------------')
                nuevo_dia(cnx)
            elif int(operacion)==9 and username == "Administrador":
                print('\n----------------Opcion 9----------------')
                añadir_peli(cnx)
            elif int(operacion)==10 and username == "Administrador":
                print('\n----------------Opcion 10----------------')
                eliminar_peli(cnx)
            elif int(operacion)==11 and username == "Administrador":
                print('\n----------------Opcion 11----------------')
                crear_taquillero(cnx)
            elif int(operacion)==12 and username == "Administrador":
                print('\n----------------Opcion 12----------------')
                añadir_peli_a_sala(cnx)
            else:
                print('Debes introducir un código disponible para tu usuario! ')
        except Exception:
            print('Ha ocurrido un error inesperado. Por favor intentelo de nuevo')
            


if __name__=="__main__":

    print('==================================================================================')
    print('Bienvenido a la aplicación de gestión de datos de los cines Nico&Max')
    print('==================================================================================')
    username = input('\nIntroduzca si es "Taquillero" o "Administrador": ')
    password= input('Introduzca su constraseña: ')

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
        print('---------------------------------Cines Nico&Max---------------------------------')
        main()

    else:
        print('Contraseña incorrecta')