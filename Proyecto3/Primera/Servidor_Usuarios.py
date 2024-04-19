import json
from flask import Flask, jsonify, render_template, request

app =Flask(__name__)

# Archivo donde se almacenarán los datos
archivo_datos = "clientes.json"

@app.route('/getClientes')
def mostrar_clientes():
    with open('clientes.json', 'r') as file:
        clientes = json.load(file)
    return render_template('clientes.html', clientes=clientes)

# Función para cargar los datos desde el archivo
def cargar_datos():
    try:
        with open(archivo_datos, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Función para guardar los datos en el archivo
def guardar_datos(datos):
    with open(archivo_datos, "w") as file:
        json.dump(datos, file)

@app.route('/', methods=['GET'])
def funcion1():
    return jsonify({"mensaje": "Sí está funcionando"})

# Ruta para obtener la lista de clientes
@app.route('/getClientes', methods=['GET'])
def obtener_clientes():
    clientes = cargar_datos()
    return jsonify(clientes)

@app.route('/obtenerDatosUsuarios/', methods=['POST'])
def ObtenerDatos():
    datos= request.get_json()

    #obteniendo los datos
    nombre = datos.get('nombre_json')
    apellido = datos.get('apellido_json')
    NIT = datos.get('edad_json')

    print("Nombre recibido: ", nombre)
    print("Apellido recibido: ", apellido)
    print("Edad recibida: ", NIT)

    return jsonify({"status": 200})

@app.route('/enviar-formulario', methods=['POST'])
def RecibirFormulario():
    nombre = request.form['nombre']
    correo = request.form['correo']
    NIT = request.form['NIT']

    print("Nombre recibido: ", nombre)
    print("correo recibido: ", correo)
    print("NIT recibido: ", NIT)

    # Cargar los datos existentes
    clientes = cargar_datos()

    # Verificar si el cliente ya existe por su NIT
    for cliente in clientes:
        if cliente['NIT'] == NIT:
            return jsonify({"error": "El cliente ya existe"})

    # Si el cliente no existe, agregarlo a la lista
    nuevo_cliente = {
        'nombre': nombre,
        'correo': correo,
        'NIT': NIT
    }
    clientes.append(nuevo_cliente)

    # Guardar los datos actualizados
    guardar_datos(clientes)

    return jsonify({"status": "Cliente agregado correctamente"})

#Método para cargar el archivo de configuración
@app.route('/upload/config', methods=['POST'])
def upload_config():
    file = request.files['archivo_configuracion']
    if file:
        # Procesar el archivo
        return {"status": "Archivo procesado correctamente"}, 200
    else:
        return {"error": "Error al procesar el archivo"}, 400
    
if __name__ == "__main__":
    app.run(port=4700, debug=True)