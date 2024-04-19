from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido al Backend!"

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/reset', methods=['POST'])
def reset_data():
    # Lógica para resetear la base de datos
    return {"status": "Correcto"}, 200

from flask import request

#Método para cargar el archivo de configuración
@app.route('/upload/config', methods=['POST'])
def upload_config():
    file = request.files['archivo_configuracion']
    if file:
        # Procesar el archivo
        return {"status": "Archivo procesado correctamente"}, 200
    else:
        return {"error": "Error al procesar el archivo"}, 400

#Método para cargar el archivo de transacciones
@app.route('/upload/transac', methods=['POST'])
def upload_transac():
    file = request.files['archivo_transacciones']
    if file:
        # Procesar el archivo
        return {"status": "File processed successfully"}, 200
    else:
        return {"error": "No file provided"}, 400

#Método para consultar el estado de cuenta    
@app.route('/account_status', methods=['GET'])
def account_status():
    nit = request.args.get('nit_cliente')
    # Lógica para buscar y devolver el estado de cuenta
    return {"client": nit, "status": "account details here"}, 200

#Método para consultar ingresos
@app.route('/income', methods=['GET'])
def income():
    month = request.args.get('mes')
    # Lógica para calcular y devolver los ingresos del mes
    return {"month": month, "income": "income details here"}, 200
