import sys
import subprocess
import os

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
import hashlib
import base64
import json
from cryptography.fernet import Fernet, InvalidToken
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

# --- Funciones de descifrado ---
def generar_clave(password: str) -> bytes:
    sha256 = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha256)

def descifrar_archivo(ruta_archivo: str, password: str):
    clave = generar_clave(password)
    fernet = Fernet(clave)

    # Leer archivo .sha256
    with open(ruta_archivo, "r") as f:
        metadata = json.load(f)

    extension = metadata["extension"]
    datos_cifrados = base64.b64decode(metadata["contenido"])

    try:
        datos = fernet.decrypt(datos_cifrados)
    except InvalidToken:
        print("❌ Contraseña incorrecta o archivo dañado.")
        return

    salida = ruta_archivo.replace(".sha256", "") + "_descifrado" + extension
    with open(salida, "wb") as f:
        f.write(datos)

    print(f"✅ Archivo descifrado guardado en: {salida}")

    # --- Eliminar el archivo .sha256 original ---
    try:
        os.remove(ruta_archivo)
        print(f"🗑️ Archivo cifrado original eliminado: {ruta_archivo}")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar el archivo cifrado: {e}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        title="Seleccione el archivo .sha256 a descifrar",
        filetypes=[("Archivos cifrados", "*.sha256")]
    )
    root.destroy()
    sys.stdout.flush()

    if not archivo:
        print("❌ No se seleccionó ningún archivo.")
        exit()

    password = pedir_password("Ingrese la contraseña: ")
    descifrar_archivo(archivo, password)
