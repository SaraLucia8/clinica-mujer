from flask import Flask
from flask import render_template as render, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import *
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key="1234"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class base(db.Model):
    __abstract__ = True
    cedula = db.Column(db.Integer, primary_key=True)

class users(base):
    __tablename__ = 'users'
    nombre=db.Column(db.String)
    apellido=db.Column(db.String)
    nacimiento=db.Column(db.String)
    eps=db.Column(db.String)
    email=db.Column(db.String, unique=True)
    telefono=db.Column(db.Integer)
    dir=db.Column(db.String)
    ciudad=db.Column(db.String)
    password=db.Column(db.String)
    rol =db.Column(db.String)

    def __repr__(self):
        return "usuario registrado" + str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
         return check_password_hash(self.password, password)

@app.route('/', methods=['GET'])
def index():
    return render('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuarioUno =request.form['cedula']
        password = request.form['contrasena']        
        
        usuario= users.query.filter_by(cedula=usuarioUno).first()
        admin = users.query.filter_by(rol='admin')
        medico= users.query.filter_by(rol='medico')
        paciente= users.query.filter_by(rol='paciente')
        if usuario:                      
            if usuario.check_password(password):
                return redirect('dashboard') 



    return render('login.html')

@app.route('/registro', methods=['GET','POST'])
def registro(): 
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nacimiento = request.form['nacimiento']
        eps = request.form['eps']
        email = request.form['email']
        tel = request.form['tel']
        direccion = request.form['dir']
        ciudad = request.form['ciudad']
        password = request.form['contrasena']

        usuario = users(cedula= cedula, nombre=nombre, apellido= apellido, nacimiento = nacimiento, eps=eps, email=email, telefono=tel, dir=direccion, ciudad=ciudad, password=password)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        
        if usuario:
            return render('login.html')

    return render('registro.html')
    
@app.route('/politica-privacidad', methods=['GET'])
def politica_privacidad():
    return render('politica_privacidad.html')

@app.route('/nosotros', methods=['GET'])
def nosotros():
    return render('nosotros.html')

@app.route('/contacto', methods=['GET'])
def contacto():
    return render('contacto.html')

# ************ADMIN************
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render('dashboard.html')

#Medico
@app.route('/medico', methods=['GET'])
def medicouser():
    return render('medicos.html')

@app.route('/medico/user', methods=['GET'])
def medico():
    return render('usermedico.html')

@app.route('/medico/new', methods=['GET', 'POST'])
def new_medico():
    return render('new_medico.html')

@app.route('/medico/user/editar', methods=['GET', 'POST'])
def edit_medico():
    return render('editmedico.html')

@app.route('/medico/user/eliminar', methods=['GET', 'POST'])
def delete_medico():
    return render('deletemedico.html')

#Historia clinica
@app.route('/historia-clinica', methods=['GET'])
def historia():
    return render('historia-clinica.html')

@app.route('/historia-clinica/paciente/editar', methods=['GET', 'POST'])
def edit_historia():
    return render('edithistoria.html')

@app.route('/historia-clinica/paciente/eliminar', methods=['GET', 'POST'])
def delete_historia():
    return render('deletehistoria.html')

#Citas
@app.route('/listado-citas', methods=['GET'])
def listado_citas():    
    return render('listado-citas.html')

@app.route('/listado-citas/cita', methods=['GET'])
def detalle_citas():    
    return render('detalle-cita.html')

@app.route('/listado-citas/cita/editar', methods=['GET', 'POST'])
def editar_citas():    
    return render('editcita.html')

@app.route('/listado-citas/cita/eliminar', methods=['GET', 'POST'])
def delete_citas():    
    return render('deletecita.html')

@app.route('/form', methods=['GET', 'POST'])
@app.route('/form-cita', methods=['GET', 'POST'])
def formcita():
    return render('form-cita.html')

#Pacientes
@app.route('/paciente', methods=['GET'])
def paciente():
    return render('pacientes.html')

# @app.route('/paciente/<user>', methods=['GET'])
# def userPaciente(user):
#     return render('layout-paciente.html', user = user, nacimiento = '1/10/1800', eps = 'SURA', correo='example@uninorte.com.co', cel= 3160000000, dir= 'cali' , ciudad='Cali, Valle')

@app.route('/paciente/user', methods=['GET'])
def view_paciente():
    return render('userpaciente.html')

@app.route('/paciente/user/editar', methods=['GET', 'POST'])
def edit_paciente():
    return render('editpaciente.html')

@app.route('/paciente/user/eliminar', methods=['GET', 'POST'])
def delete_paciente():
    return render('deletepaciente.html')

#Roles y permisos 
@app.route('/roles', methods=['GET'])
def roles():
    return render('roles.html')

@app.route('/roles/new', methods=['GET', 'POST'])
def new_rol():
    return render('new_rol.html')

# ************MEDICO************
@app.route('/dashboard-medico', methods=['GET'])
def dashboard_medico():
    return render('dashboardmedico.html')

@app.route('/agenda', methods=['GET'])
def agenda_medico():
    return render('agendamedico.html')

@app.route('/medico/historia-clinica', methods=['GET'])
def historia_medico():
    return render('med-historiaclinica.html')

@app.route('/medico/historia-clinica/user', methods=['GET'])
def ver_medico():
    return render('med-vercita.html')

@app.route('/medico/historia-clinica/user/newcoment', methods=['GET', 'POST'])
def comentar_medico():
    return render('med-comentarcita.html')

# ************PACIENTE************
@app.route('/dashboard-paciente', methods=['GET'])
def dashboard_paciente():
    return render('dashboardpaciente.html')

@app.route('/mis-citas', methods=['GET'])
def citas_paciente():
    return render('pac-citas.html')

@app.route('/mis-citas/agendar', methods=['GET', 'POST'])
def newcitas_paciente():
    return render('pac-newcitas.html')

@app.route('/mis-citas/calificar', methods=['GET', 'POST'])
def calificar_cita_paciente():
    return render('pac-calficarcitas.html')

@app.route('/mis-citas/editar', methods=['GET', 'POST'])
def editar_cita_paciente():
    return render('pac-editarcitas.html')

@app.route('/mis-citas/eliminar', methods=['GET', 'POST'])
def eliminar_cita_paciente():
    return render('pac-eliminarcitas.html')

@app.route('/mi-historia-clinica', methods=['GET'])
def historia_paciente():
    return render('pac-historia.html')

if __name__ == '__main__': 
    db.create_all()
    app.run(debug=True, port=8000)