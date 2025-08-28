import sys
import subprocess

# --- Autoinstalación de dependencias con fallback ---
def ensure_package(pkg, min_version=None):
    try:
        mod = __import__(pkg)
        if min_version:
            import importlib.metadata
            current_version = importlib.metadata.version(pkg)
            from packaging import version
            if version.parse(current_version) < version.parse(min_version):
                print(f"📦 '{pkg}' ({current_version}) es más viejo que {min_version}. Actualizando...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg}>={min_version}"])
                except Exception:
                    print(f"⚠️ No se pudo actualizar automáticamente '{pkg}'.")
                    print("👉 Intenta instalar manualmente con:")
                    print(f"   {sys.executable} -m pip install --upgrade {pkg}>={min_version}")
                    sys.exit(1)
    except ImportError:
        print(f"📦 El paquete '{pkg}' no está instalado. Instalando...")
        try:
            if min_version:
                subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg}>={min_version}"])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"✅ '{pkg}' instalado correctamente.")
        except Exception:
            print(f"⚠️ No se pudo instalar automáticamente '{pkg}'.")
            print("👉 Intenta instalar manualmente con:")
            print(f"   {sys.executable} -m pip install {pkg}{'>='+min_version if min_version else ''}")
            sys.exit(1)

# --- Verificar dependencias ---
ensure_package("packaging")
ensure_package("cryptography", "42.0.0")

# --- Librerías principales ---
import os
import hashlib
import base64
import json
from cryptography.fernet import Fernet
from tkinter import Tk, filedialog
import getpass

# --- Función para pedir contraseña con * en Windows ---
def pedir_password(prompt="Contraseña: "):
    try:
        import msvcrt  # Windows
        print(prompt, end='', flush=True)
        pwd = ''
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                print('')
                break
            elif ch == b'\x08':  # Backspace
                if len(pwd) > 0:
                    pwd = pwd[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif ch == b'\x03':
                raise KeyboardInterrupt
            else:
                try:
                    char = ch.decode()
                except:
                    continue
                pwd += char
                sys.stdout.write('*')
                sys.stdout.flush()
        return pwd
    except ImportError:
        return getpass.getpass(prompt)

# --- Funciones de cifrado ---
def generar_clave(password: str) -> bytes:
    sha256 = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha256)

def cifrar_archivo(ruta_archivo: str, password: str):
    clave = generar_clave(password)
    fernet = Fernet(clave)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    datos_cifrados = fernet.encrypt(datos)

    metadata = {
        "extension": os.path.splitext(ruta_archivo)[1],
        "contenido": base64.b64encode(datos_cifrados).decode()
    }

    salida = ruta_archivo + ".sha256"
    with open(salida, "w") as f:
        json.dump(metadata, f)

    print(f"✅ Archivo cifrado guardado en: {salida}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Seleccione el archivo a cifrar")
    root.destroy()
    sys.stdout.flush()

    if not archivo:
        print("❌ No se seleccionó ningún archivo.")
        exit()

    password = pedir_password("Ingrese la contraseña: ")
    cifrar_archivo(archivo, password)
