# 🔐 Encriptador de Archivos con SHA-256 y AES

Este proyecto permite **cifrar y descifrar archivos** utilizando contraseñas seguras basadas en **SHA-256** y **AES (Fernet)**. 

Se incluyen:
- Scripts de consola (`encrypt.py` y `decrypt.py`).
- Una **interfaz gráfica (GUI)** (`gui.py`).
- **ejecutable unificado** (`.exe` en Windows).

---

## 🚀 Características
- Cifrado y descifrado de archivos con contraseña.
- Enmascaramiento de la contraseña al escribirla.
- Posibilidad de seleccionar **uno o varios archivos** a la vez.
- Eliminación automática del archivo `.sha256` tras el descifrado.
- Interfaz gráfica sencilla con **Tkinter**.
- Ejecución también desde **consola**.

---

## 📦 Instalación

Clona este repositorio y entra en el directorio:
```bash
git clone https://github.com/usuario/encriptador.git
cd encriptador
```

---

## 🖥️ Uso desde Consola

### 🔒 Cifrar un archivo
```bash
python encrypt.py
```

### 🔓 Descifrar un archivo
```bash
python decrypt.py
```

---

## 🖱️ Uso con Interfaz Gráfica

Ejecuta:
```bash
python gui.py
```

Se abrirá una ventana que permite:
- Cifrar uno o varios archivos.
- Descifrar uno o varios archivos `.sha256`.
- Usar la misma contraseña para todos los seleccionados.

---

## ⚙️ ¿Donde está el ejecutable?


El ejecutable estará disponible en:
```
dist/gui.exe   (Windows)
```

---

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

