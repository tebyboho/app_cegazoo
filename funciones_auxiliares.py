'''
    Funciones auxiliares
'''
import os 
import pandas as pd
import re

# Extrae datos del excel 

def extraccion_datos(ruta):
    df = pd.read_excel(ruta, engine='openpyxl')
    
    # Logica para saber que tipo de estructura va a extraer, con columna_transferencia o sin_columna_transferencia
        # Determinar si la columna "Transferencias" existe en la fila 2
    tiene_transferencias = (
        df.shape[1] > 12 and  # Asegura que haya al menos 13 columnas
        isinstance(df.iloc[2, 12], str) and 
        df.iloc[2, 12].strip().lower() == 'transferencias'
    )
    if tiene_transferencias:
        return {
            "fecha": df.iloc[0, 0],
            "turno": df.iloc[0, 2],
            "vendedor": df.iloc[0, 6],
            "total_accesorios": df.iloc[1, 0],
            "total_balanceados": df.iloc[1, 2],
            "total_medicamentos": df.iloc[1, 4],
            "total_animales": df.iloc[1, 6],
            "total_acuario": df.iloc[1, 8],
            "pagos": df.iloc[1, 13],
            'pagos_caja': df.iloc[1, 14],
            "venta_efectivo": df.iloc[18, 14],
            "total_credito": df.iloc[19, 14],
            "total_debito": df.iloc[20, 14],
            "total_transferencias": df.iloc[21, 14],
            "total_sobres": df.iloc[22, 14],
            "total_venta": df.iloc[26, 14],
            "file": os.path.basename(ruta)
        }
    else:
        return {
            "fecha": df.iloc[0, 0],
            "turno": df.iloc[0, 2],
            "vendedor": df.iloc[0, 6],
            "total_accesorios": df.iloc[1, 0],
            "total_balanceados": df.iloc[1, 2],
            "total_medicamentos": df.iloc[1, 4],
            "total_animales": df.iloc[1, 6],
            "total_acuario": df.iloc[1, 8],
            "pagos": df.iloc[1, 12],
            'pagos_caja': df.iloc[1, 13],
            "venta_efectivo": df.iloc[18, 13],
            "total_credito": df.iloc[19, 13],
            "total_debito": df.iloc[20, 13],
            "total_sobres": df.iloc[21, 13],
            "total_venta": df.iloc[25, 13],
            "file": os.path.basename(ruta)
        }
    
    
def recorrer_procesar(ruta_raiz):
    '''Recorre recursivamente buscanso todos los .xlsx'''
    datos_lista = []
    
    for root, _, files in os.walk(ruta_raiz):
        for file in files:
            if file.endswith(".xlsx") and not file.startswith("~$"):
                file_path = os.path.join(root, file)
                
                try:
                    datos = extraccion_datos(file_path)
                    datos_lista.append(datos)
                except Exception as e:
                    print(f'Error procesadno {file}: {e}')
    return datos_lista


def obtener_vendedora(vendedora):
    
    patrones_vendedoras = {
    'Sofia': r'(?i)so+f*i*a*',
    'Magali': r'(?i)ma*g*[au]*i*l*a*',
    'Daira': r'(?i)dai+r*a*',
    'Gabriela': r'(?i)g+a*b*r*i*e*l*a*',
    'Agustin': r'(?i)a+g*u*s*t*i*n*',
    'Teby': r'(?i)t+e+b+y*',
    'Paola': r'(?i)p+a*o+l*a*'
    }
    for nombre, patron in patrones_vendedoras.items():
        if re.search(patron, vendedora):
            return nombre

