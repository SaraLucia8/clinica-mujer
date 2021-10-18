from flask import Flask
from flask import render_template as render

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render('login.html')

@app.route('/registro', methods=['GET','POST'])
def registro():
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
    app.run(debug=True, port=8000)