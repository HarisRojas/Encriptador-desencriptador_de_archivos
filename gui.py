import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import hashlib
import base64
import json
from cryptography.fernet import Fernet, InvalidToken

# -------------------
# Funciones compartidas
# -------------------
def generar_clave(password: str) -> bytes:
    sha256 = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha256)

def cifrar_archivo(ruta_archivo: str, password: str):
    clave = generar_clave(password)
    fernet = Fernet(clave)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    datos_cifrados = fernet.encrypt(datos)
    extension = os.path.splitext(ruta_archivo)[1]

    salida = ruta_archivo + ".sha256"
    with open(salida, "w") as f:
        json.dump({
            "extension": extension,
            "contenido": base64.b64encode(datos_cifrados).decode()
        }, f)

    return salida

def descifrar_archivo(ruta_archivo: str, password: str):
    clave = generar_clave(password)
    fernet = Fernet(clave)

    with open(ruta_archivo, "r") as f:
        metadata = json.load(f)

    extension = metadata["extension"]
    datos_cifrados = base64.b64decode(metadata["contenido"])

    try:
        datos = fernet.decrypt(datos_cifrados)
    except InvalidToken:
        raise ValueError("Contraseña incorrecta o archivo dañado.")

    salida = ruta_archivo.replace(".sha256", "") + "_descifrado" + extension
    with open(salida, "wb") as f:
        f.write(datos)

    # eliminar archivo cifrado después de descifrar
    try:
        os.remove(ruta_archivo)
    except Exception:
        pass

    return salida

# -------------------
# GUI
# -------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Cifrador/Descifrador de Archivos")
        root.geometry("400x250")
        root.resizable(False, False)

        self.label = tk.Label(root, text="Selecciona una acción:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.btn_encrypt = tk.Button(root, text="Cifrar archivo(s)", width=20, command=self.encrypt)
        self.btn_encrypt.pack(pady=10)

        self.btn_decrypt = tk.Button(root, text="Descifrar archivo(s)", width=20, command=self.decrypt)
        self.btn_decrypt.pack(pady=10)

        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack(pady=20)

    def pedir_password(self, titulo="Ingrese contraseña"):
        top = tk.Toplevel(self.root)
        top.title(titulo)
        top.geometry("300x120")
        top.resizable(False, False)

        tk.Label(top, text="Contraseña:").pack(pady=5)
        pwd_entry = tk.Entry(top, show="*", width=25)
        pwd_entry.pack(pady=5)
        pwd_entry.focus_set()

        resultado = {"pwd": None}

        def confirmar():
            resultado["pwd"] = pwd_entry.get()
            top.destroy()

        btn = tk.Button(top, text="OK", command=confirmar)
        btn.pack(pady=5)

        top.grab_set()
        self.root.wait_window(top)
        return resultado["pwd"]

    def encrypt(self):
        archivos = filedialog.askopenfilenames(title="Seleccione archivo(s) a cifrar")
        if not archivos:
            return
        pwd = self.pedir_password("Contraseña para cifrar")
        if not pwd:
            return

        procesados = []
        for archivo in archivos:
            try:
                salida = cifrar_archivo(archivo, pwd)
                procesados.append(salida)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cifrar {archivo}:\n{e}")

        if procesados:
            messagebox.showinfo("Éxito", f"Archivos cifrados:\n" + "\n".join(procesados))
            self.status.config(text=f"{len(procesados)} archivo(s) cifrado(s)", fg="green")

    def decrypt(self):
        archivos = filedialog.askopenfilenames(title="Seleccione archivo(s) .sha256", filetypes=[("Archivos cifrados", "*.sha256")])
        if not archivos:
            return
        pwd = self.pedir_password("Contraseña para descifrar")
        if not pwd:
            return

        procesados = []
        for archivo in archivos:
            try:
                salida = descifrar_archivo(archivo, pwd)
                procesados.append(salida)
            except ValueError as ve:
                messagebox.showerror("Error", f"{archivo}: {ve}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al descifrar {archivo}:\n{e}")

        if procesados:
            messagebox.showinfo("Éxito", f"Archivos descifrados:\n" + "\n".join(procesados))
            self.status.config(text=f"{len(procesados)} archivo(s) descifrado(s)", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
