from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField
from wtforms.fields.core import SelectField, StringField, FloatField, BooleanField, DateTimeField, TimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError,NumberRange
from datetime import datetime

def soloHora():
    hora=datetime.now()        
    return (hora.strftime("%H:%M:%S"))

def fechaFormato():
    fecha=datetime.today()
    return (fecha.strftime("%d/%m/%Y"))

def monedasIguales(formulario,campo):
    if campo.data==formulario.fromQ.data:
        raise ValidationError("Cambia la moneda. Las monedas de compra y venta no pueden ser iguales.")


class MovimientosForm(FlaskForm):
    id=HiddenField()
    fecha = StringField("Fecha", default=fechaFormato())
    hora=StringField("Hora", default=soloHora)
    fromQ=SelectField("From", choices=[("ADA","ADA-Cardano"), ("BCH","BCH-Bitcoin Cash"), ("BNB","BNB-Binance Coin"), ("BSV","BSV-Bitcoin SV"), ("BTC","BTC-Bitcoin" ), ("EOS", "EOS-Coin"), ("ETH","ETH-Ethereum"), ("EUR","EUR-Euro"), ("LTC", "LTC-Litecoin"), ("TRX", "TRX-Tron"), ("USDT", "USDT-Tether"), ("XLM", "XLM-Stellar"), ("XRP", "XRP-Ripple")])
    fromQHidden=HiddenField()
    cantidadFromQ= FloatField("Cantidad", validators=[DataRequired("Debe introducir un número mayor de cero."),NumberRange(0.00000001,1000000000, "La cantidad debe estar en el rango [1E-8,1E9].")])
    cantidadFromQHidden=HiddenField()
    calcular=SubmitField("Calcular")
    toQ=SelectField("To", validators=[monedasIguales], choices=[("ADA","ADA-Cardano"), ("BCH","BCH-Bitcoin Cash"), ("BNB","BNB-Binance Coin"), ("BSV","BSV-Bitcoin SV"), ("BTC","BTC-Bitcoin" ), ("EOS", "EOS-Coin"), ("ETH","ETH-Ethereum"), ("EUR","EUR-Euro"), ("LTC", "LTC-Litecoin"), ("TRX", "TRX-Tron"), ("USDT", "USDT-Tether"), ("XLM", "XLM-Stellar"), ("XRP", "XRP-Ripple")])
    toQHidden=HiddenField()
    cantidadToQ= StringField("Cantidad")
    pu= StringField("P.U")
    submit=SubmitField("Aceptar")    


        


    