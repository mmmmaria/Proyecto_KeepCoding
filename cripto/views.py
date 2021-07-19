from cripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash, Response
from cripto.forms import MovimientosForm
import sqlite3
from cripto.dataaccess import *
from cripto.helper import *

dbManager = DBManager()

@app.route("/", methods=["GET","POST"])
def index():
    query ="SELECT * FROM movimientos WHERE 1=1"
    parametros=[]
    movimientos = dbManager.consultaSQL(query,parametros)
    if movimientos == False:
        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos.", "error")
        return render_template("inicio.html") 

    else:
        if not movimientos:
                flash("NO HAY MOVIMIENTOS")
        
        else:
            for f in movimientos:
                #f["pa"]=("{0:.4f}".format(float(llamaApi(f["cantidadToQ"],f["toQ"],"EUR")))) #Utilidad para comprobación del Status
                f["cantidadToQ"]=("{0:.4f}".format(float(f["cantidadToQ"])))
                f["pu"]=("{0:.4f}".format(float(f["pu"])))
               
    return render_template("inicio.html", datos = movimientos) 

@app.route("/compra", methods =["GET","POST"])
def compra():
    formulario=MovimientosForm()

    if request.method =="GET":
        return render_template ("compra.html", form=formulario)
    
    else:

        if formulario.validate():
    
            if  formulario.calcular.data is True: 

                formulario.fromQHidden.data=formulario.fromQ.data
                formulario.toQHidden.data=formulario.toQ.data
                formulario.cantidadFromQHidden.data=formulario.cantidadFromQ.data
                          
                b=formulario.fromQ.data 
                b=str(b)
                transacMON= transacMon()

                if transacMON ==False:
                    flash("Se ha producido un error en la base de datos. Pruebe en unos minutos.", "error")
                    return render_template("compra.html", form=formulario) 

                else:
                    c=transacMON["SalMON"][b]
                    movimientos=transacMON["movimientos"]

                    if not movimientos and formulario.fromQ.data != "EUR":
                        flash("El primer movimiento debe ser con Euros", "error")
                        return render_template("compra.html", form=formulario)

                    elif b !="EUR":
                        if formulario.cantidadFromQ.data <= c:
                            resultado=llamaApi(formulario.cantidadFromQ.data,formulario.fromQ.data,formulario.toQ.data)
    
                            if resultado:
                                formulario.cantidadToQ.data= resultado
                                pu=formulario.cantidadFromQ.data/formulario.cantidadToQ.data
                                formulario.pu.data= pu
                                
                            else:
                                flash("No se ha podido conectar con éxito con el conversor de moneda.", "error")
                                return render_template("compra.html", form=formulario)
                                                        
                            return render_template ("compra.html", form=formulario)

                        else:
                            flash("No tienes suficiente cantidad de moneda para efectuar esta compra. Prueba con una cantidad menor u otra moneda que tengas disponible.")    
                            return render_template("compra.html", form=formulario)

                    else:
                        resultado=llamaApi(formulario.cantidadFromQ.data,formulario.fromQ.data,formulario.toQ.data)
    
                        if resultado:
                            formulario.cantidadToQ.data= resultado
                            pu=formulario.cantidadFromQ.data/formulario.cantidadToQ.data
                            formulario.pu.data= pu
                            
                        else:
                            flash("No se ha podido conectar con éxito con el conversor de moneda.", "error")
                            return render_template("compra.html", form=formulario)
                        
                    return render_template ("compra.html", form=formulario)
                   

            elif formulario.submit.data is True:
                StringcantidadFromQ = str(formulario.cantidadFromQ.data)
                
                if formulario.fromQHidden.data == formulario.fromQ.data and formulario.toQHidden.data == formulario.toQ.data and formulario.cantidadFromQHidden.data == StringcantidadFromQ:
                    query = "INSERT INTO movimientos (fecha, hora, fromQ, cantidadFromQ, toQ, cantidadToQ, pu) VALUES (?, ?, ?, ?, ?, ?, ?)"
                            
                    try:
                        dbManager.modificaTablaSQL(query,[formulario.fecha.data, formulario.hora.data, formulario.fromQ.data, 
                        formulario.cantidadFromQ.data, formulario.toQ.data, formulario.cantidadToQ.data, formulario.pu.data])

                    except sqlite3.Error as el_error:
                        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos.", "error")
                        return render_template("compra.html", form=formulario)
                        
                    return redirect(url_for("index"))
                
                else:
                    flash("No puedes cambiar los datos para efectuar la compra.")    
                    return render_template("compra.html", form=formulario)
                
        else:
            flash("Hay un error en el formulario. Inténtalo otra vez.") 
            return render_template ("compra.html", form=formulario)
    

@app.route("/status", methods=["GET"])
def status():
   
    formulario={"InvEur":0, "SalEUR":0, "ValAct":0, "ValActTot":0}
    
    transacMON=transacMon()
    if transacMON ==False:
        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos.", "error")
        return render_template("status.html", formulario = formulario) 

    else:
        monedas=transacMON["monedas"]
        ValActMON=transacMON["ValActMON"]
        InvMON=transacMON["InvMON"]
        SalMON=transacMON["SalMON"]
        GasMON=transacMON["GasMON"]

        for m in monedas:
            if SalMON[m] > 0 and m !="EUR":          
                resultado=llamaApi(SalMON[m],m,"EUR")
                
                if resultado:
                    ValActMON[m]= resultado
                else:
                    flash("No se ha podido conectar con éxito con el conversor de moneda.", "error")
                    return render_template("status.html", formulario=formulario)            
                                    
            else:
                SalMON[m]=0
                ValActMON[m]=0

        SalMON["EUR"]=GasMON["EUR"]-InvMON["EUR"]
        ValAct = sum(ValActMON.values())
        formulario["InvEUR"]=InvMON["EUR"]
        formulario["SalEUR"]=SalMON["EUR"]
        formulario["ValAct"]=ValAct
        formulario["ValActTot"]= formulario["InvEUR"] + formulario["SalEUR"] + formulario["ValAct"]

        formulario["InvEUR"]= ("{0:.2f}".format(InvMON["EUR"]))
        formulario["SalEUR"]=("{0:.2f}".format(SalMON["EUR"]))
        formulario["ValAct"]= ("{0:.2f}".format(formulario["ValAct"]))
        formulario["ValActTot"]=("{0:.2f}".format(formulario["ValActTot"]))
            
        return render_template("status.html", formulario = formulario) 