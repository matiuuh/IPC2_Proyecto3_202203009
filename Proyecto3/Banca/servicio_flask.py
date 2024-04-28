# servicio_flask.py
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
from io import BytesIO
from xml.etree.ElementTree import ElementTree, fromstring
from datetime import datetime

app = Flask(__name__)

# Estructuras en memoria
clientes = {}
bancos = {}
transacciones = []
pagos = []

@app.route('/cargar-configuracion', methods=['POST'])
def cargar_configuracion():
    xml_data = request.data
    resultado = procesar_config_xml(xml_data)
    respuesta_xml = generar_respuesta_config_xml(resultado)
    return respuesta_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/cargar-transacciones', methods=['POST'])
def cargar_transacciones():
    xml_data = request.data
    resultado = procesar_transac_xml(xml_data)
    print(transacciones)  # Ver los datos de transacciones después de procesar
    respuesta_xml = generar_respuesta_transac_xml(resultado)
    return respuesta_xml, 200, {'Content-Type': 'application/xml'}

def generar_respuesta_config_xml(resultado):
    respuesta = ET.Element('respuesta')
    clientes = ET.SubElement(respuesta, 'clientes')
    ET.SubElement(clientes, 'creados').text = str(resultado['clientes_creados'])
    ET.SubElement(clientes, 'actualizados').text = str(resultado['clientes_actualizados'])
    
    bancos = ET.SubElement(respuesta, 'bancos')
    ET.SubElement(bancos, 'creados').text = str(resultado['bancos_creados'])
    ET.SubElement(bancos, 'actualizados').text = str(resultado['bancos_actualizados'])

    return ET.tostring(respuesta, encoding='utf8', method='xml').decode('utf8')

def generar_respuesta_transac_xml(resultado):
    respuesta = ET.Element('transacciones')
    facturas = ET.SubElement(respuesta, 'facturas')
    ET.SubElement(facturas, 'nuevasFacturas').text = str(resultado['nuevas_facturas'])
    ET.SubElement(facturas, 'facturasDuplicadas').text = str(resultado['facturas_duplicadas'])
    ET.SubElement(facturas, 'facturasConError').text = str(resultado['facturas_con_error'])
    
    pagos = ET.SubElement(respuesta, 'pagos')
    ET.SubElement(pagos, 'nuevosPagos').text = str(resultado['nuevos_pagos'])
    ET.SubElement(pagos, 'pagosDuplicados').text = str(resultado['pagos_duplicados'])
    ET.SubElement(pagos, 'pagosConError').text = str(resultado['pagos_con_error'])

    return ET.tostring(respuesta, encoding='utf8', method='xml').decode('utf8')


#Método para procesar el archivo de configuración
def procesar_config_xml(xml_data):
    tree = ElementTree(fromstring(xml_data))
    root = tree.getroot()

    global clientes, bancos

    clientes_creados = 0
    clientes_actualizados = 0
    bancos_creados = 0
    bancos_actualizados = 0

    # Procesar clientes
    for elemento_cliente in root.findall('clientes/cliente'):
        nit = elemento_cliente.find('NIT').text.strip()
        nombre = elemento_cliente.find('nombre').text.strip()
        
        if nit in clientes:
            # Si el cliente ya existe, actualiza la información
            if clientes[nit]['nombre'] != nombre:
                clientes[nit]['nombre'] = nombre
                clientes_actualizados += 1
        else:
            # Si no existe, crea un nuevo cliente
            clientes[nit] = {'nombre': nombre}
            clientes_creados += 1

    # Procesar bancos
    for elemento_banco in root.findall('bancos/banco'):
        codigo = elemento_banco.find('codigo').text.strip()
        nombre = elemento_banco.find('nombre').text.strip()
        
        if codigo in bancos:
            # Si el banco ya existe, actualiza la información
            if bancos[codigo]['nombre'] != nombre:
                bancos[codigo]['nombre'] = nombre
                bancos_actualizados += 1
        else:
            # Si no existe, crea un nuevo banco
            bancos[codigo] = {'nombre': nombre}
            bancos_creados += 1

    return {
        'clientes_creados': clientes_creados,
        'clientes_actualizados': clientes_actualizados,
        'bancos_creados': bancos_creados,
        'bancos_actualizados': bancos_actualizados,
    }

    
#Método para serializar los datos
def serializar_a_xml(datos, etiqueta_raiz):
    raiz = ET.Element(etiqueta_raiz)
    for dato in datos:
        elemento = ET.SubElement(raiz, dato['tipo'])
        for clave, valor in dato.items():
            if clave != 'tipo':
                subelemento = ET.SubElement(elemento, clave)
                subelemento.text = str(valor)
    arbol = ET.ElementTree(raiz)
    xml_io = BytesIO()
    arbol.write(xml_io, encoding='utf-8', xml_declaration=True)
    return xml_io.getvalue()

#método para resetear
@app.route('/reset', methods=['POST'])
def reset_data():
    global clientes, bancos, transacciones, pagos
    clientes.clear()
    bancos.clear()
    transacciones.clear()
    pagos.clear()
    return jsonify({'message': 'Datos restablecidos a estado inicial'}), 200

#Método para procesar transacción
def procesar_transac_xml(xml_data):
    tree = ElementTree(fromstring(xml_data))
    root = tree.getroot()

    facturas_nuevas = 0
    pagos_nuevos = 0
    facturas_duplicadas = 0
    facturas_con_error = 0
    pagos_duplicados = 0
    pagos_con_error = 0

    # Procesar facturas
    for elemento_factura in root.findall('facturas/factura'):
        try:
            numero_factura = elemento_factura.find('numeroFactura').text.strip()
            nit_cliente = elemento_factura.find('NITcliente').text.strip()
            fecha = elemento_factura.find('fecha').text.strip()
            valor = float(elemento_factura.find('valor').text.strip())

            # Verificar si la factura ya existe
            factura_existente = next((item for item in transacciones if item['numeroFactura'] == numero_factura), None)
            if factura_existente:
                facturas_duplicadas += 1
            else:
                transacciones.append({
                    'numeroFactura': numero_factura,
                    'NITcliente': nit_cliente,
                    'fecha': fecha,
                    'valor': valor
                })
                facturas_nuevas += 1
        except Exception as e:
            facturas_con_error += 1

    # Procesar pagos
    for elemento_pago in root.findall('pagos/pago'):
        try:
            codigo_banco = elemento_pago.find('codigoBanco').text.strip()
            fecha = elemento_pago.find('fecha').text.strip()
            nit_cliente = elemento_pago.find('NITcliente').text.strip()
            valor = float(elemento_pago.find('valor').text.strip())

            # Verificar si el pago ya existe
            pago_existente = next((item for item in pagos if item['codigoBanco'] == codigo_banco and item['NITcliente'] == nit_cliente and item['fecha'] == fecha), None)
            if pago_existente:
                pagos_duplicados += 1
            else:
                pagos.append({
                    'codigoBanco': codigo_banco,
                    'fecha': fecha,
                    'NITcliente': nit_cliente,
                    'valor': valor
                })
                pagos_nuevos += 1
        except Exception as e:
            pagos_con_error += 1

    return {
        'nuevas_facturas': facturas_nuevas,
        'facturas_duplicadas': facturas_duplicadas,
        'facturas_con_error': facturas_con_error,
        'nuevos_pagos': pagos_nuevos,
        'pagos_duplicados': pagos_duplicados,
        'pagos_con_error': pagos_con_error,
    }

#Método para consultar ingresos
@app.route('/ingresos', methods=['GET'])
def obtener_ingresos():
    mes = request.args.get('mes')
    año = request.args.get('año')

    # Filtrar pagos por mes y año, asumiendo que 'fecha' contiene texto adicional
    total_ingresos = 0
    for pago in pagos:
        # Extraer la fecha y convertirla a un objeto datetime
        fecha_str = pago['fecha']
        try:
            # Intenta extraer la fecha considerando que puede haber texto adicional
            fecha_str = fecha_str.split()[0]  # Esto asume que la fecha siempre está al principio
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
            if fecha.month == int(mes) and fecha.year == int(año):
                total_ingresos += pago['valor']
        except ValueError as e:
            # Aquí puedes manejar fechas mal formadas o loggear errores si es necesario
            pass
    
    ingresos = {
        'Mes': mes,
        'Año': año,
        'TotalIngresos': total_ingresos
    }

    return jsonify(ingresos)


#Método para consultar estado de cuenta
@app.route('/estado-cuenta/<nit_cliente>', methods=['GET'])
def obtener_estado_cuenta(nit_cliente):
    # Asumimos que 'transacciones' y 'pagos' son listas de diccionarios que contienen la información de cada uno.
    # Asumimos también que hay una clave 'NITcliente' en las facturas y los pagos que corresponde al NIT del cliente.
    transacciones_cliente = [t for t in transacciones if t['NITcliente'] == nit_cliente]
    pagos_cliente = [p for p in pagos if p['NITcliente'] == nit_cliente]

    saldo = sum(p['valor'] for p in pagos_cliente) - sum(t['valor'] for t in transacciones_cliente)

    estado_cuenta = {
        'NIT': nit_cliente,
        'Saldo': saldo,
        'Transacciones': transacciones_cliente,
        'Pagos': pagos_cliente
    }

    return jsonify(estado_cuenta)



#métodos para testear el programa
@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    # Suponiendo que `clientes` es un diccionario global
    return jsonify(clientes)

@app.route('/bancos', methods=['GET'])
def obtener_bancos():
    # Suponiendo que `bancos` es un diccionario global
    return jsonify(bancos)

@app.route('/transacciones', methods=['GET'])
def obtener_transacciones():
    # Suponiendo que `transacciones` es una lista global
    return jsonify(transacciones)

@app.route('/pagos', methods=['GET'])
def obtener_pagos():
    # Suponiendo que `pagos` es una lista global
    return jsonify(pagos)

@app.route('/info', methods=['GET'])
def obtener_info_estudiante():
    info_estudiante = {
        'Nombre': 'Mateo Estuardo Diego Noriega',
        'Carné': '202203009'
    }
    return jsonify(info_estudiante)


# Rutas adicionales aquí...
if __name__ == '__main__':
    app.run(threaded=True, port=8000, debug=True)
