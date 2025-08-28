# File Encryptor / Decryptor

Este repositorio contiene dos scripts en Python para **cifrar y descifrar archivos** usando AES (a través de la librería `cryptography`) con una contraseña proporcionada por el usuario.

- `encrypt.py`: Cifra cualquier archivo seleccionado por el usuario y genera un archivo `.sha256` que contiene el contenido cifrado y la extensión original.
- `decrypt.py`: Descifra un archivo `.sha256` usando la contraseña correcta y restaura el archivo original. Tras descifrar, el archivo `.sha256` se elimina automáticamente.

## Características

- Compatible con Windows, Linux y Mac.
- Los archivos se seleccionan mediante un **cuadro de diálogo gráfico** (Tkinter).
- La contraseña se escribe enmascarada con `*` en Windows, y de forma oculta en Linux/Mac.
- Comprobación automática de la librería `cryptography` y `packaging`, con instalación automática si no están presentes o son versiones antiguas.
- Detecta la extensión del archivo original y la restaura al descifrar.

## Requisitos

- Python 3.8 o superior.
- Librerías externas: `cryptography>=42.0.0`, `packaging`.

> Nota: los scripts instalan estas librerías automáticamente si no están presentes.

## Uso

### Cifrar un archivo

1. Ejecuta el script:
   ```bash
   python encrypt.py
   ```
2. Selecciona el archivo que deseas cifrar mediante el cuadro de diálogo.
3. Ingresa la contraseña (se enmascarará mientras la escribes).
4. Se generará un archivo `archivo_original.sha256` en la misma ubicación.

### Descifrar un archivo

1. Ejecuta el script:
   ```bash
   python decrypt.py
   ```
2. Selecciona el archivo `.sha256` mediante el cuadro de diálogo.
3. Ingresa la contraseña correcta.
4. El archivo descifrado se guardará con `_descifrado` en el nombre y la extensión original.
5. El archivo `.sha256` original se eliminará automáticamente.

## Seguridad

- Las contraseñas **no se almacenan** y los archivos se cifran con AES (Fernet) derivado de la contraseña mediante SHA-256.
- SHA-256 **no se utiliza para cifrar directamente**, sino para derivar la clave de cifrado.

## Ejemplo

```bash
# Cifrar archivo.txt
python encrypt.py

# Descifrar archivo.txt.sha256
python decrypt.py
```

