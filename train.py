import os
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
import joblib

def cargar_y_procesar_imagenes(ruta_dataset, tamano=(64, 64)):
    X, y = [], []
    # Ajusta estas carpetas según el dataset real que elijas
    clases = {"normal": 0, "anomalia": 1} 
    
    print(f"Buscando imágenes en: {ruta_dataset}...")
    
    for nombre_clase, label in clases.items():
        carpeta = os.path.join(ruta_dataset, nombre_clase)
        
        if not os.path.exists(carpeta):
            print(f"Advertencia: No se encontró la carpeta {carpeta}.")
            continue
            
        archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"Cargando {len(archivos)} imágenes de la clase '{nombre_clase}'...")
        
        for archivo in archivos:
            img_path = os.path.join(carpeta, archivo)
            try:
                # Procesamiento real: convertir a escala de grises y redimensionar estándar
                img = Image.open(img_path).convert('L')
                img = img.resize(tamano)
                # Aplanar para el modelo clásico
                X.append(np.array(img).flatten())
                y.append(label)
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

    return X, y

def main():
    ruta_datos = "dataset"
    X, y = cargar_y_procesar_imagenes(ruta_datos)
    
    if len(X) == 0:
        print("Error: No se cargó ninguna imagen. Verifica que extrajiste el ZIP correctamente.")
        return

    print("Entrenando modelo Random Forest con datos reales...")
    clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    clf.fit(X, y)
    
    acc = clf.score(X, y)
    print(f"¡Entrenamiento completado! Exactitud (Accuracy) en validación interna: {acc*100:.2f}%")
    
    joblib.dump(clf, "modelo_vision.pkl")
    print("Modelo guardado exitosamente como 'modelo_vision.pkl'")

if __name__ == '__main__':
    main()