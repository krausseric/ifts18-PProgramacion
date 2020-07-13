from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class SaludarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('Saludar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class ConsultaPais(FlaskForm):
    pais = StringField('País:', validators=[Required()])
    enviar = SubmitField('Filtrar')

class ConsultaEdad(FlaskForm):
    minima = IntegerField('Edad Minima:', validators=[Required('Ingresar caracteres numéricos')])
    maxima = IntegerField('Edad Maxima:', validators=[Required('Ingresar caracteres numéricos')])
    enviar = SubmitField('Filtrar')

class ConsultaFecha(FlaskForm):
    fecha = StringField('Fecha:', validators=[Required()])
    enviar = SubmitField('Filtrar')    

#Los validators contorlan que el campo completado cumple con los requisitos como:
#Estar completo, largo mínimo, como asi tambien mostrar mensajes el valor enviado es incorrecto.
#El render _kw nos permite mostar un mesaje previo dentro del campo a completar.


class AgregarCliente(FlaskForm):
	nombre = StringField('Nombre', validators=[Required()])
	edad = StringField('Edad', validators=[Required()])
	direccion = StringField('Dirección', validators=[Required()])
	pais = StringField('País', validators=[Required()])
	dni = StringField('Documento', validators=[Required()], render_kw={"placeholder": "Formato DNI sin puntos"})
	fecha_alta = StringField('Fecha Alta', validators=[Required()], render_kw={"placeholder": "Formato fecha AAAA-MM-DD"})
	mail = StringField('Correo Electrónico', validators=[Required()])
	trabajo = StringField('Trabajo', validators=[Required()])
	enviar = SubmitField('Agregar')

class AgregarProducto(FlaskForm):
    descripcion_prod = StringField('Descripcion Producto', validators=[Required()])
    codigo_prod = StringField('Codigo Producto', validators=[Required()])
    precio_prod = DecimalField('Precio Producto', validators=[Required()])
    cant_stock = IntegerField('Cantidad en Stock', validators=[Required("Tiene que ser un número entero sin decimales")])
    enviar = SubmitField('Agregar')
