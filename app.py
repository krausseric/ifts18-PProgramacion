#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, ConsultaPais, ConsultaEdad, ConsultaFecha, AgregarCliente, AgregarProducto
from wtforms import SelectField
from app import app

if __name__="__name__":
    app.run()

app = Flask(__name__)
bootstrap = Bootstrap(app)
server = app.server

app.config['SECRET_KEY'] = 'un string que funcione como llave'


#----------------------------------------------------------------------Módulos----------------------------------------------------------#

#Este modulo arbre el archivo ingresado, y permita agregar a travez del append (a+) una "nueva linea" al archivo.
#Por el atributo "listado", se pasan los datos del fomulario para que sean cargados en la "nueva linea".
#

def archivoAgregar(archivoabrir, listado): #Atributos
    with open(archivoabrir,'a+', encoding='utf-8') as archivo: 
        archivo_csv = csv.writer(archivo)
        registro = listado #Se cargan los datos del formulario 
        archivo_csv.writerow(registro) #Se escribe la nueva linea
    return archivo_csv


#--------------------------------------------------------------------------------------------------------------------------------------#


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm() #Llama al Formulario
    if formulario.validate_on_submit():  # Acá se valida el "Enviar" del formulario
        print(formulario.usuario.name)                                               #Devuelve el valor de usuario a
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data)) #la funcio saludar_persona.
    return render_template('saludar.html', form=formulario)#Si no valida el Enviar del formulario, nos regresa a saludar.html.


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)

#-------------------------------------------------------------Manejo de Errores---------------------------------------------------------#


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404 # De generarse un error, devuelve No Encontrado.


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500 # De generarse un error, devuelve No Encontrado.

#----------------------------------------------------------------------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('home.html', fecha_actual=datetime.utcnow())

#----------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/sobre')
def sobre():
    return render_template('sobre.html') # APARTADO CON DATOS SOBRE EL AUTOR.

#----------------------------------------------------------------------------------------------------------------------------------------#

# Valida el usuario y password ingresados con los que se encuentran guardados en el archivo usuarios.

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv','r') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]: #Realiza la validación.
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Usuario y contraseña incorrectos')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

# Permita registrar un nuevo registo de usuario y password en el archivo usuarios.csv.

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            archivoAgregar('usuarios.csv', [formulario.usuario.data, formulario.password.data]) #Modulo para agregar una línea nueva a un archivo.
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')

# Permite finalizar la sesión del usurio activo.

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

#-----------------------------------------------------------------------LISTADO CLIENTES---------------------------------------------#

# Permite ver la base completa de clientes sin filtrar. 

@app.route('/clientes')
def clientes():
    if 'username' in session:   
        with open('clientes.csv','r',encoding='utf-8') as planillaClientes:
            planilla_csv = csv.reader(planillaClientes)
            encabezado_csv = next(planilla_csv)
            return render_template('clientes.html', encabezado_csv=encabezado_csv, planilla_csv=planilla_csv) #Devuelve al tamplate la informacion para crear la tabla.
    else:
        return render_template('sin_permiso.html')

#-----------------------------------------------------LISTADO PRODCUTOS--------------------------------------------------------------#

# Permite ver la base completa de productos sin filtrar.

@app.route('/productos')
def productos():
    if 'username' in session:   
        with open('productos.csv','r',encoding='utf-8') as planillaProductos:
            planilla_csv = csv.reader(planillaProductos)
            encabezado_csv = next(planilla_csv)
            return render_template('productos.html', encabezado_csv=encabezado_csv, planilla_csv=planilla_csv) #Devuelve al tamplate la informacion para crear la tabla.
    else:
        return render_template('sin_permiso.html')

#-----------------------------------------------------------FILTRO CLIENTES POR PAIS---------------------------------------------------#

# Permite filtar la tabla de la base de datos por país.
#filtra el dato ingrasado en el formulario (formulario.pais.data), lo transforma en mayusculas y lo compara con la informaciön
#de la tabla que tambien transforma en mayusculas para evitar errores por formato al comparar.
# con el "startswith", nos permite hacer buquedas parciales de información.

@app.route('/consultaclienteporpais',methods=['GET', 'POST'])
def clientesPorPais():
    if 'username' in session:
        formulario = ConsultaPais()
        filtro = formulario.pais.data
        resultado = []
        if formulario.validate_on_submit():
            with open('clientes.csv', encoding='utf-8') as planillaClientes:
                planilla_csv = csv.reader(planillaClientes)
                encabezado_csv = next(planilla_csv)
                cliente = next(planilla_csv, None)
                while cliente:      
                    if cliente[3].upper().startswith(filtro.upper()):
                        resultado.append(cliente)
                    cliente = next(planilla_csv, None)
                if resultado == []:
                    flash('No hay resultados para tu búsqueda')
                else:
                    return render_template('resconsultaclienteporpais.html', encabezado_csv=encabezado_csv, resultado=resultado)
        return render_template('consultaclienteporpais.html', form=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')  


#----------------------------------------------------------FILTRO CLIENTES POR EDAD--------------------------------------------------#

# Permite filtar la tabla de la base de datos por país.
# Filtra el dato ingrasado en el formulario (formulario.maxima/minima.data) y o compara con el dato de la tabla, validando con cumpla con el criterio
# del maximo y minimo.
# ambos datos forzamos que se transformen e Integer, para poder compararlos sin problamas.

@app.route('/consultaedad',methods=['GET', 'POST'])
def clientesEdad():
    if 'username' in session:
        formulario = ConsultaEdad()
        edad_Max = formulario.maxima.data
        edad_Min = formulario.minima.data
        resultado = []
        if formulario.validate_on_submit():
            with open('clientes.csv', encoding='utf-8') as planillaClientes:
                planilla_csv = csv.reader(planillaClientes)
                encabezado_csv = next(planilla_csv)
                dato = next(planilla_csv, None)
                while dato:          
                    if (int(dato[1])>=int(edad_Min) and int(dato[1])<=int(edad_Max)):
                        resultado.append(dato)
                    dato = next(planilla_csv, None)
                if resultado == []:
                    flash('No hay resultados para tu búsqueda')
                else:
                    return render_template('resconsultaedad.html', encabezado_csv=encabezado_csv, resultado=resultado)
        return render_template('consultaedad.html', formedad=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')

#----------------------------------------------------------FILTRO CLIENTES POR FECHA--------------------------------------------------#

# Permite filtar la tabla de la base de datos por fecha.
#filtra el dato ingrasado en el formulario (formulario.fecha.data), lo compara con la informaciön de la tabla.
# con el "startswith", nos permite hacer buquedas parciales de información.


@app.route('/consultafecha',methods=['GET', 'POST'])
def clientesFecha():
    if 'username' in session:
        formulario = ConsultaFecha()
        filtro = formulario.fecha.data
        resultado = []
        if formulario.validate_on_submit():
            with open('clientes.csv', encoding='utf-8') as planillaClientes:
                planilla_csv = csv.reader(planillaClientes)
                encabezado_csv = next(planilla_csv)
                dato = next(planilla_csv, None)
                while dato:
                    if dato[5].startswith(filtro):
                        resultado.append(dato)
                    dato = next(planilla_csv, None)
                if resultado == []:
                    flash('No hay resultados para tu búsqueda')
                else:
                    return render_template('resconsultafecha.html', encabezado_csv=encabezado_csv, resultado=resultado)
        return render_template('consultafecha.html', formfecha=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')



#----------------------------------------------------------AGREGAR CLIETES-------------------------------------------------------------#

@app.route('/agregarcliente',methods=['GET', 'POST'])
def agregarCliente():
    if 'username' in session: #Valida que el usuario etnga una sesión activa.
        formulario = AgregarCliente()
        resultado = []
        if formulario.validate_on_submit(): #Modulo para agregar una línea nueva a un archivo.
            archivoAgregar('clientes.csv', [formulario.nombre.data, formulario.edad.data, formulario.direccion.data, formulario.pais.data, formulario.dni.data, formulario.fecha_alta.data, formulario.mail.data, formulario.trabajo.data])
            flash('Cliente creado correctamente')
            return redirect(url_for('clientes'))
        return render_template('agregarcliente.html', formagregarcliente=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')

#----------------------------------------------------------AGREGAR PRODUCTOS-----------------------------------------------------------#

@app.route('/agregarproductos',methods=['GET', 'POST'])
def agregarProducto():
    if 'username' in session:
        formulario = AgregarProducto()
        resultado = []
        if formulario.validate_on_submit(): #Modulo para agregar una línea nueva a un archivo.
            archivoAgregar('productos.csv', [formulario.descripcion_prod.data,formulario.codigo_prod.data, formulario.precio_prod.data, formulario.cant_stock.data])
            flash('Producto creado correctamente')
            return redirect(url_for('productos'))
        return render_template('agregarproductos.html', agregarproducto=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')


#----------------------------------------------------------------------main----------------------------------------------------__-------#

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
