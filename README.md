# MaWe-Backend
MaWe's python backend
Te recomiendo abrir el proyecto utilizando un IDE más completo que Thonny, yo utilizo VSCode (https://code.visualstudio.com/).\n
Antes de correr el programa debes asegurate de tener instalada la versión 3.x de Python, si esta no está instalada habrá problemas al ejecutar el API. Una vez verificado, abre un terminal en la carpeta del proyecto (si estás en VSCode basta con hacer click en Terminal>Nueva terminal en la barra de herramientas), después de esto deberás instalar virtualenv para crear un entorno virtual.\n
$ pip install virtualenv\n
Una vez completado este paso deberás ejecutar el entorno virual\n
$ ./vnv/Scripts/activate.ps1\n
Luego deberás instalar las dependencias utilizadas para el proyecto\n
$ pip install flask flask-pymongo flask_cors flask_jwt_extended\n
Cuando estas terminan de instalarse podrás ejecutar el proyecto utilizando\n
$ python src/app.py\n
