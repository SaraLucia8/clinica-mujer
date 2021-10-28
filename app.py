from flask import Flask, render_template as render, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import *
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key="1234"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)    

class users(db.Model):
    __tablename__ = 'users'
    cedula = db.Column(db.Integer, primary_key=True)
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
    especialidad = db.Column(db.String)
    estado = db.Column(db.Boolean)
    
    def __repr__(self):
        return self.cedula

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
         return check_password_hash(self.password, password)

class citas(db.Model):
    __tablename__ = 'citas'
    cita_id=db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, nullable=False)
    paciente_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String)
    motivo = db.Column(db.String(500))
    estado = db.Column(db.Boolean)
    hora_atencion = db.Column(db.String)
    sintomas = db.Column(db.String)
    diagnostico = db.Column(db.String)
    anotaciones = db.Column(db.String)
    calificacion = db.Column(db.Integer)
    calificacion_obs = db.Column(db.String)

class cli_rol(db.Model):
    __tablename__   = 'Cli_rol'
    id_rol  = db.Column(db.String,  primary_key=True)
    nom_rol = db.Column(db.String)
    #users = db.relationship('users', backref=db.backref('usuarios_per', lazy=True))

class permisos_rol(db.Model):
    __tablename__   = 'permisos'
    rol        = db.Column(db.String, primary_key=True )
    med_cre    = db.Column(db.String)
    med_con    = db.Column(db.String)
    med_edi    = db.Column(db.String)
    med_eli    = db.Column(db.String)
    pac_cre    = db.Column(db.String)
    pac_con    = db.Column(db.String)
    pac_edi    = db.Column(db.String)
    pac_eli    = db.Column(db.String)
    cita_cre   = db.Column(db.String)
    cita_con   = db.Column(db.String)
    cita_edi   = db.Column(db.String)
    cita_eli   = db.Column(db.String)
    cal_cre    = db.Column(db.String)
    cal_con    = db.Column(db.String)
    cal_edi    = db.Column(db.String)
    cal_eli    = db.Column(db.String)
    com_cre    = db.Column(db.String)
    com_con    = db.Column(db.String)
    com_edi    = db.Column(db.String)
    com_eli    = db.Column(db.String)

@app.route('/', methods=['GET'])
def index():
    return render('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuarioUno =request.form['cedula']
        password = request.form['contrasena']        
        usuario= users.query.filter_by(cedula=usuarioUno).first()
        session['usuarioIngresado']=usuarioUno 
        if usuario:
            if usuario.rol == 'admin':                      
                if usuario.check_password(password):
                    return redirect(url_for('dashboard'))
            elif usuario.rol == 'medico':
                if usuario.check_password(password):
                    return redirect('dashboard-medico')
            else:
                if usuario.check_password(password):
                    return redirect('dashboard-paciente')
        else:            
            return render('login.html')
    return render('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

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
        rol = 'paciente'
        estado= True

        usuario = users(cedula= cedula, nombre=nombre, apellido= apellido, nacimiento = nacimiento, eps=eps, email=email, telefono=tel, dir=direccion, ciudad=ciudad, password=password, rol = rol, estado=estado)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
         
        if usuario:
            return redirect('login')

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

@app.route('/acceso-denegado')
def denegado():
    return render('acceso-denegado.html')

# ************ADMIN************
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('dashboard.html', row=usuario)
    else:
        return render('acceso-denegado.html')

@app.route('/search', methods=['GET', 'POST'])
def buscar():
    if 'usuarioIngresado' in session:
        if request.method =='POST':
            busqueda = str(request.form.get("search"))
            usuarios = users.query.filter(users.cedula.like(busqueda))
            listusu = usuarios.all()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('resultsearch.html', row=usuario, search=listusu)
    else:
        return render('acceso-denegado.html')

#Medico
@app.route('/medico', methods=['GET'])
def medicouser():
    if 'usuarioIngresado' in session:
        medicos = users.query.filter_by(rol='medico')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('medicos.html', listamedicos = medicos, row=usuario)
    else:
        return render('acceso-denegado.html')

@app.route('/medico/<user>', methods=['GET'])
def medico(user):
    if 'usuarioIngresado' in session:
        medicos = users.query.filter_by(cedula=user).first()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        pacientes = users.query.filter_by(rol='paciente')
        citass = citas.query.filter_by(medico_id=int(user)).all()
        return render('usermedico.html', medico=medicos, row=usuario, cita=citass, listapacientes = pacientes)
    else:
        return render('acceso-denegado.html')
    
@app.route('/medico/new', methods=['GET', 'POST'])
def new_medico():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            cedula = request.form['cedula']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            nacimiento = request.form['nacimiento']
            especialidad = request.form['especialidad']
            email = request.form['email']
            tel = request.form['tel']
            direccion = request.form['dir']
            ciudad = request.form['ciudad']
            password = request.form['contrasena']
            rol = 'medico'
            estado = True

            usuario = users(cedula= cedula, nombre=nombre, apellido= apellido, nacimiento = nacimiento, email=email, telefono=tel, dir=direccion, ciudad=ciudad, password=password, rol = rol, especialidad = especialidad, estado = estado)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
        return render('new_medico.html')
    else:
        return render('acceso-denegado.html')

@app.route('/medico/<user>/editar', methods=['GET', 'POST'])
def edit_medico(user):
    if 'usuarioIngresado' in session:
        medico = users.query.filter_by(cedula=user).first()
        if request.method == 'POST':
            medico.nombre = request.form['nombre']
            medico.apellido = request.form['apellido']
            medico.nacimiento = request.form['nacimiento']
            medico.especialidad = request.form['especialidad']
            medico.email = request.form['email']
            medico.telefono = request.form['telefono']
            medico.dir = request.form['dir']
            medico.ciudad = request.form['ciudad']
            medico.password = request.form['password']

            db.session.commit()

        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('editmedico.html', data=medico,row=usuario)
    else:
        return render('acceso-denegado.html') 

@app.route('/medico/<user>/eliminar', methods=['GET', 'POST'])
def delete_medico(user):
    if 'usuarioIngresado' in session:
        medico = users.query.filter_by(cedula=user).first()
        medico.estado = 0

        db.session.commit()
        return render('deletemedico.html')
    else:
        return render('acceso-denegado.html')
        
#Historia clinica
@app.route('/historia-clinica/<cita>/editar', methods=['GET', 'POST'])
def edit_historia(cita):
    if 'usuarioIngresado' in session:
        citass = citas.query.filter_by(cita_id=cita).first()
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        if request.method == 'POST':
            citass.motivo=request.form['motivo']
            citass.hora_atencion=request.form['hora_atencion']
            citass.sintomas=request.form['sintomas']
            citass.diagnostico=request.form['diagnostico']
            citass.anotaciones=request.form['anotaciones']

            db.session.commit()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('edithistoria.html', row=usuario, data=citass, listamedicos=medicos, listapacientes=pacientes)
    else:
        return render('acceso-denegado.html')
    
@app.route('/historia-clinica/<cita>/eliminar', methods=['GET', 'POST'])
def delete_historia(cita):
    if 'usuarioIngresado' in session:
        citass = citas.query.filter_by(cita_id=cita).first()
        citass.estado = 0

        db.session.commit()
        return render('deletehistoria.html')
    else:
        return render('acceso-denegado.html')
    
#Citas
@app.route('/listado-citas', methods=['GET','POST'])
def listado():
    if 'usuarioIngresado' in session:
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('listado-citas.html', listamedicos=medicos, listapacientes=pacientes, row=usuario)
    else:
        return render('acceso-denegado.html')

@app.route('/listado-citas/new', methods=['GET','POST'])
# @app.route('/form-cita', methods=['GET', 'POST'])
def newcita():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            medico_id = request.form['citamedico']
            paciente_id = request.form['citapaciente']
            fecha = request.form['citafecha']
            motivo = request.form['citamotivo']
            estado = 1
            
            cita = citas(medico_id=medico_id, paciente_id=paciente_id, fecha=fecha, motivo=motivo, estado=estado)
            db.session.add(cita)
            db.session.commit()
            return redirect(request.referrer)
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('newcita.html', listamedicos=medicos, row=usuario, listapacientes=pacientes)
    else:
        return render('acceso-denegado.html')

@app.route('/listado-citas/<cedulam>', methods=['GET','POST'])
def listado_citas(cedulam):
    if 'usuarioIngresado' in session:
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        citass= citas.query.filter_by(medico_id=cedulam).all()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('listado-citas.html', listamedicos=medicos, listacitas=citass, listapacientes=pacientes, row=usuario)
    else:
        return render('acceso-denegado.html')
    
@app.route('/listado-citas/<cita>/ver', methods=['GET'])
def detalle_citas(cita):
    if 'usuarioIngresado' in session:
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        cita = citas.query.filter_by(cita_id=cita).first()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('cita.html', row=usuario, data=cita, listamedicos=medicos, listapacientes=pacientes)
    else:
        return render('acceso-denegado.html')
    
@app.route('/listado-citas/<cita>/editar', methods=['GET', 'POST'])
def editar_citas(cita):
    if 'usuarioIngresado' in session:
        cita = citas.query.filter_by(cita_id=cita).first()
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        if request.method == 'POST':
            cita.medico_id = int(request.form['citamedico'])
            cita.paciente_id = int(request.form['citapaciente'])
            cita.fecha = request.form['citafecha']
            cita.motivo = request.form['citamotivo']
            db.session.commit()
        
        return render('editcita.html', data=cita, row=usuario, listamedicos=medicos, listapacientes=pacientes, cedulam = cita.medico_id)
    else:
        return render('acceso-denegado.html')
    
@app.route('/listado-citas/<cita>/eliminar', methods=['GET', 'POST'])
def delete_citas(cita):
    if 'usuarioIngresado' in session:
        cita = citas.query.filter_by(cita_id=cita).first()
        cita.estado = 0

        db.session.commit()
        return render('deletecita.html')
    else:
        return render('acceso-denegado.html')
    
#Pacientes
@app.route('/paciente', methods=['GET'])
def paciente():
    if 'usuarioIngresado' in session:
        pacientes = users.query.filter_by(rol='paciente')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        print(session['usuarioIngresado'])
        return render('pacientes.html', listapacientes = pacientes, row = usuario)
    else:
        return render('acceso-denegado.html')  

@app.route('/paciente/<user>', methods=['GET'])
def view_paciente(user):
    if 'usuarioIngresado' in session:
        paciente = users.query.filter_by(cedula=user).first()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        medicos = users.query.filter_by(rol='medico')
        citass = citas.query.filter_by(paciente_id=user).all()
        return render('userpaciente.html', data=paciente, row=usuario, listamedicos=medicos,  cita=citass)
    else:
        return render('acceso-denegado.html')   
    
@app.route('/paciente/<user>/editar', methods=['GET', 'POST'])
def edit_paciente(user):
    if 'usuarioIngresado' in session:
        paciente = users.query.filter_by(cedula=user).first()
        if request.method == 'POST':
            paciente.nombre = request.form['nombre']
            paciente.apellido = request.form['apellido']
            paciente.nacimiento = request.form['nacimiento']
            paciente.eps = request.form['eps']
            paciente.email = request.form['email']
            paciente.telefono = request.form['telefono']
            paciente.dir = request.form['dir']
            paciente.ciudad = request.form['ciudad']
            paciente.password = request.form['password']

            db.session.commit()

        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('editpaciente.html', data=paciente,row=usuario)
    else:
        return render('acceso-denegado.html') 
    
@app.route('/paciente/<user>/eliminar', methods=['GET', 'POST'])
def delete_paciente(user):
    if 'usuarioIngresado' in session:
        paciente = users.query.filter_by(cedula=user).first()
        paciente.estado = 0

        db.session.commit()

        return render('deletepaciente.html')
    else:
        return render('acceso-denegado.html') 
    
#Roles y permisos 
@app.route('/roles', methods=['GET','POST'])
def listadorol():
    if 'usuarioIngresado' in session:
        roles = cli_rol.query.filter_by()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('roles.html', listaroles=roles, row=usuario)
    else:
        return render('acceso-denegado.html')

@app.route('/roles/<rol_seleccionado>', methods=['GET','POST'])
def listado_roles(rol_seleccionado):
    if 'usuarioIngresado' in session:
        roles    = cli_rol.query.filter_by()
        permisos = permisos_rol.query.filter_by(rol=rol_seleccionado)
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('roles.html', listaroles=roles, listapermisos=permisos,row=usuario)
    else:
        return render('acceso-denegado.html')
    
# ************MEDICO************
@app.route('/dashboard-medico', methods=['GET'])
def dashboard_medico():
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('dashboardmedico.html', row=usuario)
    else:
        return render('acceso-denegado.html')

@app.route('/agenda/<cedulam>', methods=['GET'])
def agenda_medicov(cedulam):
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        lcita = citas.query.filter_by(medico_id=cedulam)
        pacientes = users.query.filter_by(rol='paciente')
        return render('agendamedico.html',row=usuario, listacitas=lcita, listapacientes=pacientes)
    else:
        return render('acceso-denegado.html')

@app.route('/medico/historia-clinica/<cedulam>', methods=['GET'])
def historia_medico(cedulam):
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        pacientes = users.query.filter_by(rol='paciente')
        citass= citas.query.filter_by(medico_id=cedulam).all()
        cedulap=[]
        for c in citass:
            cedulap.append(c.paciente_id)        
        cedulaa = list(set(cedulap))
        print(cedulaa)
        return render('med-historiaclinica.html', row=usuario, listapacientes=pacientes, cedulaa=cedulaa)
    else:
        return render('acceso-denegado.html')

@app.route('/medico/historia-clinica/<cedulam>/<cedulap>', methods=['GET', 'POST'])
def ver_historia_medico(cedulam, cedulap):
    if 'usuarioIngresado' in session:
        paciente = users.query.filter_by(cedula=cedulap).first()
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        medicos = users.query.filter_by(rol='medico')
        pacientes = users.query.filter_by(rol='paciente')
        citass = citas.query.filter_by(paciente_id=cedulap).all()
        return render('med-ver-historia.html', data=paciente, row=usuario, listamedicos=medicos,  cita=citass, cedulap=cedulap, listapacientes=pacientes)
    else:
        return render('acceso-denegado.html')
    
@app.route('/medico/historia-clinica/<cedulam>/newcoment/<cedulap>', methods=['GET', 'POST'])
def comentar_citas_medico(cedulap, cedulam):
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        lcita = citas.query.filter_by(paciente_id=cedulap).all()
        pacientes = users.query.filter_by(rol='paciente')
        return render('med-citas-paciente.html',row=usuario, listapacientes=pacientes, listacitas=lcita, cedulam=cedulam)
    else:
        return render('acceso-denegado.html')

@app.route('/medico/historia-clinica/<cedulam>/newcoment/<cedulap>/<cita>', methods=['GET', 'POST'])
def comentar_medico(cedulap, cedulam, cita):
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        citap= citas.query.filter_by(cita_id=cita).first()

        if request.method == 'POST':
            citap.sintomas = request.form['sintomas']
            citap.diagnostico =  request.form['diagnostico']
            citap.anotaciones = request.form['anotaciones']
            citap.estado = 1

            db.session.commit()
        return render('med-comentarcita.html', usuario=usuario, cita = citap)
    else:
        return render('acceso-denegado.html')
        
@app.route('/medico/historia-clinica/user/<cedulap>', methods=['GET'])
def ver_medico(cedulap):
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        pax = users.query.filter_by(cedula= cedulap).first()
        citap= citas.query.filter_by(paciente_id=cedulap).first()
        return render('med-vercita.html', usuario =usuario, cita= citap, paciente= pax)
    else:
        return render('acceso-denegado.html')

# ************PACIENTE************
@app.route('/dashboard-paciente', methods=['GET'])
def dashboard_paciente():
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('dashboardpaciente.html', row=usuario)
    else:
        return render('acceso-denegado.html')
    
@app.route('/mis-citas', methods=['GET'])
def citas_paciente():
    if 'usuarioIngresado' in session:
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        return render('pac-citas.html', row=usuario)
    else:
        return render('acceso-denegado.html')
    
@app.route('/mis-citas/agendar', methods=['GET', 'POST'])
def newcitas_paciente():
    if 'usuarioIngresado' in session:
    
        medicos = users.query.filter_by(rol='medico')
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
    
        if request.method == 'POST':
            medico_id = request.form['medicos']
            paciente_id = int(session['usuarioIngresado'])
            fecha = request.form['fecha-cita']
            hora_atencion = request.form['hora-cita']
            motivo = request.form['motivo']
            estado = 0

            cita = citas(medico_id=medico_id, paciente_id=paciente_id, fecha= fecha, hora_atencion= hora_atencion, motivo=motivo, estado=estado)
            db.session.add(cita)
            db.session.commit()

        return render('pac-newcitas.html', medicos = medicos, usuario = usuario)
    else:
        return render('acceso-denegado.html')
    
@app.route('/mis-citas/calificar', methods=['GET', 'POST'])
def calificar_cita_paciente():
    if 'usuarioIngresado' in session:
        return render('pac-calficarcitas.html')
    else:
        return render('acceso-denegado.html')
    
@app.route('/mis-citas/editar', methods=['GET', 'POST'])
def editar_cita_paciente():
    if 'usuarioIngresado' in session:
        return render('pac-editarcitas.html')
    else:
        return render('acceso-denegado.html')
    
@app.route('/mis-citas/eliminar', methods=['GET', 'POST'])
def eliminar_cita_paciente():
    if 'usuarioIngresado' in session:
        return render('pac-eliminarcitas.html')
    else:
        return render('acceso-denegado.html')
    
@app.route('/mi-historia-clinica', methods=['GET'])
def historia_paciente():
    if 'usuarioIngresado' in session:
        paciente = users.query.filter_by(cedula=int(session['usuarioIngresado']))
        usuario = users.query.filter_by(cedula=int(session['usuarioIngresado'])).first()
        medicos = users.query.filter_by(rol='medico')
        citass = citas.query.filter_by(paciente_id=int(session['usuarioIngresado'])).all()
        return render('pac-historia.html', data=paciente, row=usuario, listamedicos=medicos,  cita=citass)
    else:
        return render('acceso-denegado.html')
    

if __name__ == '__main__': 
    db.create_all()
    extend_existing=True
    app.run(debug=True, port=8000)