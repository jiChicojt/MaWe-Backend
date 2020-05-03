# MaWe-Backend
MaWe's python backend\
Te recomiendo abrir el proyecto utilizando un IDE más completo que Thonny, yo utilizo VS Code (https://code.visualstudio.com/).</br></br>
Antes de correr el programa debes asegurate de tener instalada la versión 3.x de Python, si esta no está instalada habrá problemas al ejecutar el API. Una vez verificado, abre un terminal en la carpeta del proyecto (*si estás en VS Code basta con hacer click en **Terminal>Nueva terminal** en la barra de herramientas*), después de esto deberás instalar virtualenv para crear un entorno virtual.</br></br>
***$ pip install virtualenv***</br></br>
Una vez completado este paso deberás ejecutar el entorno virual (*si estás usando VS Code el entorno se levanta al abrir una nueva terminal*)</br></br>
***$ ./vnv/Scripts/activate.ps1***</br></br>
Luego deberás instalar las dependencias utilizadas para el proyecto</br></br>
***$ pip install flask flask-pymongo flask_cors flask_jwt_extende***</br></br>
Cuando estas terminan de instalarse podrás ejecutar el proyecto utilizando</br></br>
***$ python src/app.py***</br></br>
