from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pqr'
mysql = MySQL(app)

app.secret_key = "mysecretkey"


@app.route('/getAll', methods=['GET'])
def getAll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
        content = {'ID': result[0], 'NOMBRE': result[1], 'APELLIDO': result[2],
                   'ID_TIPO_USUARIO': result[3], 'NUMERO_IDENTIFICACION': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/getAllById/<id>', methods=['GET'])
def getAllById(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id))
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
        content = {'ID': result[0], 'NOMBRE': result[1], 'APELLIDO': result[2],
                   'ID_TIPO_USUARIO': result[3], 'NUMERO_IDENTIFICACION': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/add_registro', methods=['POST'])
def add_registro():
    if request.method == 'POST':
        NOMBRE = request.json['NOMBRE']
        APELLIDO = request.json['APELLIDO']
        ID_TIPO_USUARIO = request.json['ID_TIPO_USUARIO']
        NUMERO_IDENTIFICACION = request.json['NUMERO_IDENTIFICACION']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (NOMBRE,APELLIDO,ID_TIPO_USUARIO,NUMERO_IDENTIFICACION) VALUES (%s,%s,%s,%s) ",
                    (NOMBRE, APELLIDO, ID_TIPO_USUARIO, NUMERO_IDENTIFICACION))
        mysql.connection.commit()
        return jsonify({"INFORMACION": "REGISTRO EXITOSO"})


@app.route('/update/<id>', methods=['PUT'])
def update(id):
    NOMBRE = request.json['NOMBRE']
    APELLIDO = request.json['APELLIDO']
    ID_TIPO_USUARIO = request.json['ID_TIPO_USUARIO']
    NUMERO_IDENTIFICACION = request.json['NUMERO_IDENTIFICACION']
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE usuarios  SET NOMBRE= %s ,APELLIDO=%s,ID_TIPO_USUARIO=%s  WHERE usuarios.ID = %s", (NOMBRE,APELLIDO,ID_TIPO_USUARIO,NUMERO_IDENTIFICACION))
    mysql.connection.commit()
    return jsonify({"INFORMACION": "REGISTRO ACTUALIZADO"})


@app.route('/delete/<id>', methods = ['DELETE'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = %s', (id))
    mysql.connection.commit()
    return jsonify({"INFORMACION": "REGISTRO ELIMINADO"})
app.run(port=5000)
