import os

# Carpetas y archivos a ignorar
ignorar = {'.git', 'node_modules', 'venv', '__pycache__', '.env', 'dist', 'build', 'contexto_proyecto'}
carpeta_salida = 'contexto_proyecto'
os.makedirs(carpeta_salida, exist_ok=True)

# Límite de caracteres por archivo para evitar saturación y respetar límites de adjuntos
limite_caracteres = 15000 
parte = 1
contenido_actual = ""
archivos_generados = []

def guardar_parte(texto, num):
    nombre_archivo = os.path.join(carpeta_salida, f"parte_{num}.txt")
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    return nombre_archivo

for raiz, dirs, archivos in os.walk('.'):
    # Filtrar directorios excluidos
    dirs[:] = [d for d in dirs if d not in ignorar]
    for archivo in archivos:
        if archivo.endswith(('.py', '.js', '.md', '.json', '.txt', '.html', '.css')):
            ruta_completa = os.path.join(raiz, archivo)
            try:
                with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as f:
                    texto_archivo = f.read()
                
                bloque = f"\n\n=== ARCHIVO: {ruta_completa} ===\n{texto_archivo}\n"
                
                # Si agregar este archivo supera el límite, guardamos la parte actual y abrimos otra
                if len(contenido_actual) + len(bloque) > limite_caracteres:
                    if contenido_actual:
                        archivos_generados.append(guardar_parte(contenido_actual, parte))
                        parte += 1
                        contenido_actual = ""
                
                contenido_actual += bloque
            except Exception as e:
                print(f"Error leyendo {ruta_completa}: {e}")

# Guardar el sobrante final
if contenido_actual:
    archivos_generados.append(guardar_parte(contenido_actual, parte))

print(f"\n¡Proceso completado! Se han creado {len(archivos_generados)} archivos dentro de la carpeta '{carpeta_salida}/'. Ya puedes adjuntarlos.")