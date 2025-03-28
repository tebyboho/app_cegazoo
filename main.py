'''
    Programa para recorrer las cajas y extraer la informacion que necesito
    fecha, turno, empleado
    total_accesorios, total_balanceados, total_medicamentos, total_acuario
    total_efectivo, total credito, total_debito, total_transferencias, venta_total
    pagos, pagos caja
'''


import os
import pandas as pd
import re
from funciones_auxiliares import recorrer_procesar, obtener_vendedora
from db_connection import connect_bd
import time



inicio = time.time()

# Globales
dir_name = 'CAJAS'
ruta_raiz = os.path.join(os.getcwd(), dir_name)

patrones_vendedoras = {
    'Sofia': r'(?i)\bsofi+i*[a]*\b',
    'Magui': r'(?i)\bmagui+i*[s]*\b',
    'Daira': r'(?i)\bdai+i*[ra]*\b'
}


datos_procesados = recorrer_procesar(ruta_raiz)

cantidad_archivos = len(datos_procesados)

conexion, cursor = connect_bd()

if conexion and cursor:
    for i in range(len(datos_procesados)):
        # Extraer los datos del diccionario para hacer el insert
        fecha = datos_procesados[i]['fecha']
        #turno = datos_procesados[i]['turno']
        vendedor = datos_procesados[i]['vendedor']
        total_accesorios = datos_procesados[i]['total_accesorios']
        total_balanceados = datos_procesados[i]['total_balanceados']
        total_medicamentos = datos_procesados[i]['total_medicamentos']
        total_animales = datos_procesados[i]['total_animales']
        total_acuario = datos_procesados[i]['total_acuario']
        pagos = datos_procesados[i]['pagos']
        pagos_caja = datos_procesados[i]['pagos_caja']
        total_efectivo = datos_procesados[i]['venta_efectivo']
        total_credito = datos_procesados[i]['total_credito']
        total_debito = datos_procesados[i]['total_debito']
        total_transferencias = datos_procesados[i].get('total_transferencias', 0)  # Usamos .get para manejar valores faltantes
        total_sobres = datos_procesados[i]['total_sobres']
        total_ventas = datos_procesados[i]['total_venta']
        file = datos_procesados[i]['file']
        
        nombre_vendedora = obtener_vendedora(datos_procesados[i]['vendedor'])
        if nombre_vendedora:
            cursor.execute("SELECT id FROM empleados WHERE nombre LIKE %s;", (f"%{nombre_vendedora}%",))
            empleado_id = cursor.fetchone()[0]
        else:
            empleado_id = None
            
        #  'turno' viene en formato de cadena como 'mañana' o 'tarde'
        turno = datos_procesados[i]['turno']

        # Convertir el turno a un valor entero que coincide con el valor de la base de datos
        turno_int = 1 if turno.lower() == 'mañana' else 2 if turno.lower() == 'tarde' else None

        # Verificamos si el turno es válido antes de continuar
        if turno_int is not None:
            cursor.execute("SELECT turno_id FROM turnos WHERE turno_id = %s;", (turno_int,))
            turno_id = cursor.fetchone()[0]
        else:
            # Manejar el caso en que el turno no es válido
            turno_id = None
            
            
        # Construir el query INSERT
        query_insert = """
        INSERT INTO ventas (
            fecha, turno_id, empleado_id, total_accesorios, total_balanceados, total_medicamentos, 
            total_animales, total_acuario, total_pagos, total_pagos_caja, total_efectivo, total_credito, 
            total_debito, total_transferencias, total_sobres, total_ventas
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
            # Ejecutar el insert
        cursor.execute(query_insert, (
            fecha, turno_id, empleado_id, total_accesorios, total_balanceados, total_medicamentos, 
            total_animales, total_acuario, pagos, pagos_caja, total_efectivo, total_credito, 
            total_debito, total_transferencias, total_sobres, total_ventas
        ))
    

        # Confirmar cambios en la base de datos
        conexion.commit()

# Cerrar cursor y conexión
cursor.close()
conexion.close()
                        
fin = time.time()

print(f'Tiempo de ejecución: {fin - inicio}')
print(f'{cantidad_archivos} archivos procesados')