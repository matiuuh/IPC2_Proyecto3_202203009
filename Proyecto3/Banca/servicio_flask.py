# servicio_flask.py
import json
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
from io import BytesIO
from xml.etree.ElementTree import ElementTree, fromstring
from datetime import datetime
import os
from flask import Flask, jsonify, request, send_file
from reportlab.pdfgen import canvas
import re
from datetime import datetime
from xml.etree.ElementTree import ElementTree, fromstring

app = Flask(__name__)

# Estructuras en memoria
clientes = {}
bancos = {}
transacciones = []
pagos = []

def crear_pdf_configuracion(xml_data, filename="configuracion.pdf"):
    pdf_path = "C:/Users/estua/OneDrive/Documentos/IPC/IPC2_PROYECTO3/Proyecto3" + filename
    p = canvas.Canvas(pdf_path)
    p.drawString(100, 800, "Archivo de Configuración")
    y_position = 780
    lines = xml_data.decode('utf-8').split('\n')
    for line in lines:
        p.drawString(100, y_position, line)
        y_position -= 12
    p.save()
    return pdf_path

def crear_pdf_transaccion(xml_data, filename="transaccion.pdf"):
    pdf_path = "C:/Users/estua/OneDrive/Documentos/IPC/IPC2_PROYECTO3/Proyecto3" + filename
    p = canvas.Canvas(pdf_path)
    p.drawString(100, 800, "Archivo de transacción")
    y_position = 780
    lines = xml_data.decode('utf-8').split('\n')
    for line in lines:
        p.drawString(100, y_position, line)
        y_position -= 12
    p.save()
    return pdf_path

@app.route('/cargar-configuracion', methods=['POST'])
def cargar_configuracion():
    xml_data = None
    try:
        # Intenta obtener el archivo de la carga de archivos
        if 'archivo_configuracion' in request.files:
            archivo = request.files['archivo_configuracion']
            if archivo.filename == '':
                return jsonify({'error': 'No se seleccionó archivo.'}), 400
            xml_data = archivo.read()
        elif request.data:
            # Si no hay archivos, intenta leer los datos directamente del cuerpo de la petición
            xml_data = request.data

        if not xml_data:
            return jsonify({'error': 'No se proporcionaron datos XML válidos.'}), 400

        # Procesa los datos XML
        resultado = procesar_config_xml(xml_data)
        ruta_archivo = generar_y_guardar_respuesta_config_xml(resultado)
        pdf_file_path = crear_pdf_configuracion(xml_data)
        return jsonify({'archivo_guardado': ruta_archivo, 'pdf_creado': pdf_file_path}), 200

    except Exception as e:
        app.logger.error(f'Error al cargar configuración: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/cargar-transacciones', methods=['POST'])
def cargar_transacciones():
    xml_data = None
    try:
        # Intenta obtener el archivo de la carga de archivos
        if 'archivo_transacciones' in request.files:
            archivo = request.files['archivo_transacciones']
            if archivo.filename == '':
                return jsonify({'error': 'No se seleccionó archivo.'}), 400
            xml_data = archivo.read()
        elif request.data:
            # Si no hay archivos, intenta leer los datos directamente del cuerpo de la petición
            xml_data = request.data

        if not xml_data:
            return jsonify({'error': 'No se proporcionaron datos XML válidos.'}), 400

        # Procesa los datos XML
        resultado = procesar_transac_xml(xml_data)
        ruta_archivo = generar_y_guardar_respuesta_transac_xml(resultado)
        pdf_file_path = crear_pdf_transaccion(xml_data)
        return jsonify({'archivo_guardado': ruta_archivo, 'pdf_creado': pdf_file_path}), 200

    except Exception as e:
        app.logger.error(f'Error al cargar transacciones: {str(e)}')
        return jsonify({'error': str(e)}), 500


def generar_y_guardar_respuesta_transac_xml(resultado, filename="respuesta_transacciones.xml"):
    # Crear el elemento raíz XML
    respuesta = ET.Element('transacciones')

    # Agregar subelementos para facturas
    facturas = ET.SubElement(respuesta, 'facturas')
    ET.SubElement(facturas, 'nuevasFacturas').text = str(resultado['nuevas_facturas'])
    ET.SubElement(facturas, 'facturasDuplicadas').text = str(resultado['facturas_duplicadas'])
    ET.SubElement(facturas, 'facturasConError').text = str(resultado['facturas_con_error'])
    
    # Agregar subelementos para pagos
    pagos = ET.SubElement(respuesta, 'pagos')
    ET.SubElement(pagos, 'nuevosPagos').text = str(resultado['nuevos_pagos'])
    ET.SubElement(pagos, 'pagosDuplicados').text = str(resultado['pagos_duplicados'])
    ET.SubElement(pagos, 'pagosConError').text = str(resultado['pagos_con_error'])

    # Convertir el árbol XML a una cadena
    xml_str = ET.tostring(respuesta, encoding='utf8', method='xml').decode('utf8')

    # Definir la ruta donde se guardará el archivo
    directorio_respuestas = "C:/Users/estua/OneDrive/Documentos/IPC/IPC2_PROYECTO3/Proyecto3"
    if not os.path.exists(directorio_respuestas):
        os.makedirs(directorio_respuestas)
    
    ruta_completa = os.path.join(directorio_respuestas, filename)

    # Escribir el XML en un archivo
    with open(ruta_completa, 'w', encoding='utf-8') as archivo_xml:
        archivo_xml.write(xml_str)

    # Opcionalmente, retornar la ruta del archivo para uso posterior
    return ruta_completa

    return ET.tostring(respuesta, encoding='utf8', method='xml').decode('utf8')

#método para generar el archivo respuesta de config
def generar_y_guardar_respuesta_config_xml(resultado, filename="respuesta_configuracion.xml"):
    # Crear el elemento raíz XML
    respuesta = ET.Element('respuesta')

    # Agregar subelementos para clientes
    clientes = ET.SubElement(respuesta, 'clientes')
    ET.SubElement(clientes, 'creados').text = str(resultado['clientes_creados'])
    ET.SubElement(clientes, 'actualizados').text = str(resultado['clientes_actualizados'])
    
    # Agregar subelementos para bancos
    bancos = ET.SubElement(respuesta, 'bancos')
    ET.SubElement(bancos, 'creados').text = str(resultado['bancos_creados'])
    ET.SubElement(bancos, 'actualizados').text = str(resultado['bancos_actualizados'])

    # Convertir el árbol XML a una cadena
    xml_str = ET.tostring(respuesta, encoding='utf8', method='xml').decode('utf8')

    # Definir la ruta donde se guardará el archivo
    directorio_respuestas = "C:/Users/estua/OneDrive/Documentos/IPC/IPC2_PROYECTO3/Proyecto3"
    if not os.path.exists(directorio_respuestas):
        os.makedirs(directorio_respuestas)
    
    ruta_completa = os.path.join(directorio_respuestas, filename)

    # Escribir el XML en un archivo
    with open(ruta_completa, 'w', encoding='utf-8') as archivo_xml:
        archivo_xml.write(xml_str)

    # Opcionalmente, retornar la ruta del archivo para uso posterior
    return ruta_completa

def validar_nit(nit):
    # El patrón verifica que el NIT tenga exactamente 7 dígitos, un guión, y un dígito verificador
    patron_nit = r'^\d{7}-\d$'
    return re.match(patron_nit, nit) is not None

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
        
        if validar_nit(nit):
            if nit in clientes:
                # Si el cliente ya existe, verifica si la información ha cambiado
                if clientes[nit]['nombre'] != nombre:
                    clientes[nit]['nombre'] = nombre
                    clientes_actualizados += 1
            else:
                # Si no existe, crea un nuevo cliente
                clientes[nit] = {'nombre': nombre}
                clientes_creados += 1
        else:
            print(f"Invalid NIT format: {nit}")

    # Procesar bancos
    for elemento_banco in root.findall('bancos/banco'):
        codigo = elemento_banco.find('codigo').text.strip()
        nombre = elemento_banco.find('nombre').text.strip()
        
        if codigo in bancos:
            # Si el banco ya existe, verifica si la información ha cambiado
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
def extraer_fechas(texto):
    patron_fecha = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
    return re.findall(patron_fecha, texto)

def validar_nit(nit):
    patron_nit = r'^\d{7}-\d$'
    return re.match(patron_nit, nit) is not None

def procesar_transac_xml(xml_data):
    tree = ElementTree(fromstring(xml_data))
    root = tree.getroot()

    facturas_nuevas = 0
    pagos_nuevos = 0
    facturas_duplicadas = 0
    facturas_con_error = 0
    pagos_duplicados = 0
    pagos_con_error = 0

    # Process invoices
    for factura in root.findall('facturas/factura'):
        try:
            numero_factura = factura.find('numeroFactura').text.strip()
            nit_cliente = factura.find('NITcliente').text.strip()
            fecha = factura.find('fecha').text.strip()
            valor = float(factura.find('valor').text.strip())

            if validar_nit(nit_cliente) and extraer_fechas(fecha):
                # Check if the invoice already exists
                factura_existente = next((item for item in transacciones if item['numeroFactura'] == numero_factura), None)
                if factura_existente:
                    facturas_duplicadas += 1
                else:
                    transacciones.append({
                        'numeroFactura': numero_factura,
                        'NITcliente': nit_cliente,
                        'fecha': extraer_fechas(fecha)[0],
                        'valor': valor
                    })
                    facturas_nuevas += 1
            else:
                facturas_con_error += 1
        except Exception as e:
            facturas_con_error += 1

    # Process payments
    for pago in root.findall('pagos/pago'):
        try:
            codigo_banco = pago.find('codigoBanco').text.strip()
            fecha_pago = pago.find('fecha').text.strip()
            nit_cliente_pago = pago.find('NITcliente').text.strip()
            valor_pago = float(pago.find('valor').text.strip())

            if validar_nit(nit_cliente_pago) and extraer_fechas(fecha_pago):
                # Check if the payment already exists
                pago_existente = next((item for item in pagos if item['codigoBanco'] == codigo_banco and item['NITcliente'] == nit_cliente_pago and item['fecha'] == extraer_fechas(fecha_pago)[0]), None)
                if pago_existente:
                    pagos_duplicados += 1
                else:
                    pagos.append({
                        'codigoBanco': codigo_banco,
                        'NITcliente': nit_cliente_pago,
                        'fecha': extraer_fechas(fecha_pago)[0],
                        'valor': valor_pago
                    })
                    pagos_nuevos += 1
            else:
                pagos_con_error += 1
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

    if not mes or not año:
        return jsonify({'error': 'Ambos mes y año son necesarios para la consulta.'}), 400

    total_ingresos = 0
    for pago in pagos:
        try:
            fecha = datetime.strptime(pago['fecha'].split()[0], '%d/%m/%Y')
            if fecha.month == int(mes) and fecha.year == int(año):
                total_ingresos += pago['valor']
        except ValueError:
            continue  # Ignora este pago si hay un problema con la fecha

    ingresos = {'Mes': mes, 'Año': año, 'TotalIngresos': total_ingresos}
    return jsonify(ingresos)


#Método para consultar estado de cuenta
@app.route('/estado-cuenta/<nit_cliente>', methods=['GET'])
def obtener_estado_cuenta(nit_cliente):
    # Filtrando datos relevantes
    transacciones_cliente = [t for t in transacciones if t['NITcliente'] == nit_cliente]
    pagos_cliente = [p for p in pagos if p['NITcliente'] == nit_cliente]

    # Calculando el saldo
    saldo = sum(p['valor'] for p in pagos_cliente) - sum(t['valor'] for t in transacciones_cliente)

    # Preparando datos para devolver
    estado_cuenta = {
        'NIT': nit_cliente,
        'Saldo': saldo,
        'Transacciones': transacciones_cliente,
        'Pagos': pagos_cliente
    }

    # Creación del PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Estado de Cuenta para NIT: {nit_cliente}")
    p.drawString(100, 780, f"Saldo: ${saldo}")

    y_position = 760
    p.drawString(100, y_position, "Transacciones:")
    y_position -= 20
    for trans in transacciones_cliente:
        p.drawString(100, y_position, f"Factura: {trans['numeroFactura']} - Valor: ${trans['valor']}")
        y_position -= 20

    y_position -= 10
    p.drawString(100, y_position, "Pagos:")
    y_position -= 20
    for pago in pagos_cliente:
        p.drawString(100, y_position, f"Pago: {pago['valor']} - Fecha: {pago['fecha']}")
        y_position -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    # Guardar el PDF en el servidor
    pdf_filename = f"{nit_cliente}_estado_cuenta.pdf"
    with open(pdf_filename, 'wb') as f:
        f.write(buffer.getvalue())

    # Opcional: devolver el PDF como descarga directa o devolver JSON con enlace al PDF
    if 'pdf' in request.args:
        return send_file(buffer, attachment_filename=pdf_filename, as_attachment=True)
    else:
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
        'Carné': '202203009',
        'Documentación': 'https://github.com/Matius-Noriega/IPC2_Proyecto3_202203009.git'
    }
    return jsonify(info_estudiante)

def guardar_datos():
    data = {
        'clientes': clientes,
        'bancos': bancos,
        'transacciones': transacciones,
        'pagos': pagos
    }
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_datos():
    global clientes, bancos, transacciones, pagos
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            clientes = data['clientes']
            bancos = data['bancos']
            transacciones = data['transacciones']
            pagos = data['pagos']
    except (IOError, ValueError):
        clientes = {}
        bancos = {}
        transacciones = []
        pagos = []

cargar_datos()  # Cargar datos al iniciar la aplicación

# Rutas adicionales aquí...
if __name__ == '__main__':
    app.run(threaded=True, port=8000, debug=True)
