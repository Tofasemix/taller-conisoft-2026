[README.md](https://github.com/user-attachments/files/34024135/README.md)
# Taller: Prácticas Profesionales de Versionado de Código y Datos con Git & DVC

**CONISOFT 2026**

Este repositorio contiene la guía paso a paso utilizada durante el taller práctico de MLOps y versionado de datos/modelos para visión artificial utilizando imágenes de radiografías de tórax (Chest X-Ray).

## 📋 Prerrequisitos

Asegúrate de contar con:
1. **Miniconda / Anaconda** o Python 3.10+ instalado.
2. **Git** instalado y configurado en tu terminal.
3. Una cuenta gratuita en **GitHub** y **DAGsHub**.

---

## 🚀 Paso 1: Configuración del Entorno de Python

Abre tu terminal (PowerShell en Windows, Terminal en Mac/Linux) y crea/activa un entorno limpio:

```bash
# 1. Crear e instalar el entorno virtual con Python 3.10
conda create -n taller_dvc python=3.10 -y
conda activate taller_dvc
```

*(Continuaremos con el resto de la instalación después de clonar el repositorio en el Paso 2).*

---

## 🛠️ Paso 2: Crear tu propia copia (Fork) y Clonar

Para que puedas subir tus cambios a GitHub y conectar DAGsHub sin problemas de permisos, necesitas tu propio repositorio. **No clones el repositorio original directamente.**

1. Ve al repositorio base del taller: `https://github.com/TU_USUARIO_ORIGINAL/taller-conisoft-2026`
2. En la esquina superior derecha de GitHub, haz clic en el botón **Fork** (Bifurcar) y luego en **Create fork**. Esto creará una copia exacta del proyecto en tu propia cuenta.
3. Ahora, abre tu terminal y clona **tu** nueva copia (cambia `TU_USUARIO` por tu usuario de GitHub):

```bash
git clone https://github.com/TU_USUARIO/taller-conisoft-2026.git
cd taller-conisoft-2026
```

4. Instala las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

5. Inicializa DVC en el proyecto:
```bash
dvc init
git add .
git commit -m "Inicializar DVC"
```

---

## 📂 Paso 3: Descargar Datos y Entrenar el Modelo Inicial

1. Descarga el dataset del taller desde el enlace oficial:
   👉 [**Descargar Datasets de Radiografías (Google Drive)**](https://drive.google.com/drive/folders/1OhgnAX1wnNfogzM4GGrA48_V059kkUBz?usp=sharing)

2. Extrae el archivo `dataset_A.zip` dentro de la raíz de tu proyecto. La estructura debe quedar exactamente así:
   ```text
   taller-conisoft-2026/
   └── dataset/
       ├── normal/
       └── anomalia/
   ```

3. Ejecuta el script de entrenamiento para procesar las radiografías y generar el primer modelo:
   ```bash
   python train.py
   ```
   *Esto generará el archivo binario del modelo: `modelo_vision.pkl`.*

---

## 📦 Paso 4: Rastrear Archivos Pesados con DVC

Le indicamos a DVC que tome el control de las imágenes y del modelo binario. Esto creará los archivos de punteros ligeros (`.dvc`) que sí irán a GitHub:

```bash
dvc add dataset modelo_vision.pkl
```

Guarda los punteros en Git:
```bash
git add dataset.dvc modelo_vision.pkl.dvc .gitignore
git commit -m "Registra dataset A y modelo v1 con DVC"
```

---

## ☁️ Paso 5: Conectar el Almacenamiento Remoto (DAGsHub)

Para compartir datos y modelos sin saturar Git, vinculamos DAGsHub como nuestro servidor remoto de DVC:

1. Ve a [DAGsHub](https://dagshub.com/) e inicia sesión.
2. Haz clic en **Create > New Repository > Connect a repository** y selecciona tu fork de `taller-conisoft-2026`.
3. Una vez conectado, haz clic en el botón verde **Data** > pestaña **DVC** > **HTTPS**.
4. Ejecuta los comandos en tu terminal sustituyendo tus credenciales:

```bash
# Agregar el almacenamiento remoto
dvc remote add -d -f almacenamiento https://dagshub.com/TU_USUARIO/taller-conisoft-2026.dvc

# Configurar autenticación local
dvc remote modify almacenamiento --local auth basic
dvc remote modify almacenamiento --local user TU_USUARIO_DAGSHUB
dvc remote modify almacenamiento --local password TU_TOKEN_DAGSHUB
```

---

## 📤 Paso 6: Subir y Sincronizar Datos (DVC Push & Pull)

### Subir los datos y modelo a DAGsHub:
```bash
dvc push
```
*(Luego, sube tus cambios de código a GitHub con `git push`)*.

### Prueba de simulación (Disaster Recovery):
Si borras los archivos locales para simular un cambio de máquina o pérdida de datos:

```bash
# Borrar archivos locales pesados (Windows PowerShell)
Remove-Item -Recurse -Force dataset
Remove-Item -Force modelo_vision.pkl

# (En Mac/Linux: rm -rf dataset modelo_vision.pkl)
```

Recupera todo desde DAGsHub en segundos:
```bash
dvc pull
```

---

## 🤝 Paso 7: Flujo Colaborativo en Vivo (Simulación en Parejas)

Formen equipos de dos personas (**Estudiante A** y **Estudiante B**). El Estudiante A debe invitar al Estudiante B como colaborador en su repositorio de GitHub y en la configuración de su repositorio en DAGsHub.

### Dinámica de colaboración:

1. **Estudiante B (Colaborador):**
   * Clona el repositorio del Estudiante A desde GitHub: `git clone <URL_DEL_ESTUDIANTE_A>`
   * Recupera las radiografías y el modelo original con: `dvc pull`
   * Extrae el contenido de `dataset_B.zip` (descargado del Drive) y añade las nuevas imágenes a la carpeta `dataset/`.
   * Re-entrena el modelo para mejorar la métrica con los nuevos datos:
     ```bash
     python train.py
     ```
   * Actualiza el versionado de los datos y el nuevo modelo en DVC:
     ```bash
     dvc add dataset modelo_vision.pkl
     dvc push
     ```
   * Sube los nuevos punteros a Git para avisar a su compañero:
     ```bash
     git add dataset.dvc modelo_vision.pkl.dvc
     git commit -m "Actualiza modelo v2 con Dataset B"
     git push
     ```

2. **Estudiante A (Creador Original):**
   * En su propia terminal, sincroniza los cambios de código y datos:
     ```bash
     git pull
     dvc pull
     ```
   * ¡Listo! El entorno del Estudiante A se actualizará al instante con las nuevas imágenes y el modelo v2 entrenado por su compañero.
