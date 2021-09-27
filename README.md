# Repositorio del Trabajo Fin de Máster
Repositorio del trabajo fin de máster de Eduardo Graván Serrano.

## Configuración
Para poder usar esta aplicación, es necesario tener una cuenta de desarrollador en Twitter y crear un fichero con nombre "api_keys" en el directorio src/resources.

Este fichero deberá ser rellenado con las claves de la API de nuestra cuenta de desarrollador, escribiendo una clave por línea en el siguiente orden:

* Consumer API Key
* Consumer API Secret
* Access Token Key
* Access Token Secret

En caso de que se desee probar el funcionamiento de la botnet, también se deberá crear este fichero "api_keys" siguiendo las instrucciones descritas anteriormente, ya que el servidor C2 hace uso del endpoint de stream de la API oficial de desarrolladores.

Además, si se desean ejecutar los bots, se deberá crear un fichero de configuración que se le deberá pasar como parámetro al bot en el momento de lanzarlo. El contenido de este fichero de configuración deberá guardará información sobre la cuenta de usuario a utilizar por el bot, y deberá seguir el siguiente formato:

* Email o número de teléfono.
* Nombre de la cuenta (handle de Twitter).
* Contraseña.

Por último, para el correcto funcionamiento de la infraestructura de la botnet, se deberá configurar la IP del servidor C2 en el código de los bots. 