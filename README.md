# proyecto Flask classic - MyCrypto

Python, Flask, Sqlite.
PROYECTO FIN DE BOOTCAMP VII- ZERO, FLASK CLASSIC.
María Megía Cardeñoso.

## **APLICACIÓN WEB-REGISTRO DE CRIPTOMONEDAS**

### INSTALACIÓN:

-Creamos un entorno virtual en la carpeta donde vayamos a instalar la aplicación:  
python -m venv venv  
Lo activamos:  
venv\Scripts\activate (Windows)  
. venv/bin/activate (Linux/MAC)  
  
-Comenzamos instalando las dependencias:  
pip install -r requirements.txt  
  
-Creamos las variables de entorno:  
Duplicamos el fichero .env_template  
Renombramos la copia a .env  
Informamos a FLASK_ENV si se trata de una versión para "development" o para "production".  
  
-Creamos el fichero de configuración:  
Duplicamos el fichero config_template.py  
Renombramos la copia a config.py  
Informar la SECRET_KEY para Flask-WTF  
Informar la API_KEY  
Informar la ruta al fichero de base de datos; la ruta debe estar dentro de la carpeta de la aplicación.  
  
-Crear la base de datos ejecutando el fichero migrations/initial.sql  
Puede hacerse con un cliente gráfico (DBBrowser..) o con sqlite3.  
Ejecutar:  
sqlite3 <ruta al fichero según figura en config.py>  
.read <ruta relativa a migrations/initial.sql>  
.tables  
.q  
  
### EJECUCIÓN EN LOCAL:  
  
Escribir en la terminal:  
flask run  
Levantar   
  
### VISTAS:  
  
Esta aplicación consta de 3 vistas, accesibles por los links superiores de "Inicio", "Compra" y "Status":  
  
* **VISTA INICIO - ROUTE:/**  
Muestra el listado de movimientos grabados en la base de datos.  
Los campos son: fecha (de la compra), Hora (de la compra), From (moneda inicial), Q (Cantidad de moneda inicial), To (moneda final), Q (Cantidad de moneda final), P.U. (Precio Unitario, en la moneda señalada).  
Si no existen movimientos, muestra el mensaje "NO HAY MOVIMIENTOS".  
  
  
* **VISTA COMPRA - ROUTE:/compra:**  
Es una vista que ofrece la fecha y hora actual, ofrece 3 campos formularios a rellenar: los selectores From (moneda inicial), To (moneda final) y Cantidad (Cantidad de moneda inicial),
y otros 2 campos autocompletables: Cantidad (Cantidad de moneda final) y P.U. (Precio Unitario, de la moneda inicial respecto a la final).  
Existen una serie de validaciones que impiden la compra en el caso de no cumplirse lo siguiente:  
    - Las monedas inicial y final no pueden ser iguales.
    - No se puede comprar con una moneda si no se dispone de un saldo suficiente de dicha moneda, a excepción de los Euros (EUR).
    - La fecha y hora no pueden modificarse.
    - Una vez hecha la conversión de la moneda inicial y su cantidad inicial en la moneda final y su cantidad final a través del botón "Calcular", no podrán modificarse ninguno de estos campos.

Si todo lo anterior se cumple, la compra quedará ejecutada y grabada en la base de datos una vez se pulse el botón "Aceptar".
Si existiera un fallo temporal en la base de datos o en la comunicación con la API de conversión, se avisará del error en cada caso mediante un mensaje.


* **VISTA STATUS - ROUTE:/status:**
En esta vista se ofrecen 4 campos calculados en función de la inversión en Euros, las compras realizadas y la cotización de cada moneda en el momento actual:
    - Total de Euros Invertidos: Es la suma de las cantidades de moneda inicial, siendo esta en Euros.
    - Saldo de Euros Invertidos: Es la suma de las cantidades de moneda final menos la suma de las cantidades de moneda inicial, siendo ambas en Euros.
    - Valor Actual de las Criptos (Euros): Es la suma de las cantidades de moneda final menos la suma de las cantidades de moneda inicial, para cada criptomoneda, expresadas en Euros según la cotización de cada una en el momento actual.
    - Valor Actual Total (Euros): Es igual a la suma del Total de Euros Invertidos más el Saldo de Euros Invertidos más el Valor Actual de las Criptos de que disponemos, todo ello expresado en Euros y correspondiente al momento actual.