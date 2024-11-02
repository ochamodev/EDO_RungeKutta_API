# Pasos a seguir para ejecutar el proyecto
## 1. Creación de entorno virtual de python
    `python -m venv venv`

## 2. Activacioón del entorno virtual
    `source env/bin/activate` Funciona para Mac o Linux
    `env/Scripts/activate.bat` En CMD
    `env/Scripts/activate.ps1` En Powershell
## 2.  Instalación de librerías
    `pip install -r requirements.txt`
## 3. Como ejecutar el servidor
    `uvicorn server:app --reload`