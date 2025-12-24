import csv
import json
from pathlib import Path

# --- Configuración Inicial ---
ARCHIVO_ENTRADA = "datos_brutos.csv"
ARCHIVO_SALIDA = "reporte_analisis.json"

# --- Crear Archivo CSV de Ejemplo (Para Pruebas) ---
# **ESTUDIANTE A DEBE CREAR MANUALMENTE ESTE ARCHIVO Y AÑADIR ERRORES**
def crear_csv_ejemplo():
    """Crea un archivo CSV de ejemplo que contiene errores intencionales."""
    data = [
        ["Fecha", "Sensor", "Temperatura"],
        ["2025-11-01", "SensorA", "25.0"],
        ["2025-11-01", "SensorB", "24.5"],
        ["2025-11-02", "SensorC", "ERROR"],  # <--- ERROR INTENCIONAL (ValueError)
        ["2025-11-02", "SensorA", "26.1"],
        ["2025-11-03", "SensorB", ""],      # <--- ERROR INTENCIONAL (ValueError/Empty)
        ["2025-11-03", "SensorC", "23.9"]
    ]
    try:
        with open(ARCHIVO_ENTRADA, 'w', newline='', encoding='utf-8') as f:
            escritor_csv = csv.writer(f)
            escritor_csv.writerows(data)
        print(f"✅ Archivo '{ARCHIVO_ENTRADA}' creado con datos de prueba. ¡Añada sus propios errores!")
    except Exception as e:
        print(f"❌ Error al crear el archivo de prueba: {e}")

# --- Funciones Principales ---

def analizar_datos():
    """
    [Implementación obligatoria - Tarea para Estudiante A/B]
    Lee el CSV, valida los datos, calcula métricas y genera un reporte JSON.
    """
    datos_validos = []
    registros_totales = 0
    errores_omitidos = 0

    try:
        # 1. IMPLEMENTAR LECTURA SEGURA DE ARCHIVO (Issue #5)
        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
            lector = csv.reader(f)
            next(lector) # Omitir encabezado
            
            for fila in lector:
                registros_totales += 1
                try:
                    # 2. IMPLEMENTAR VALIDACIÓN DE VALOR (Issue #6)
                    # La temperatura es el tercer elemento (índice 2)
                    temperatura = float(fila[2])
                    datos_validos.append(temperatura)
                
                # 3. CAPTURAR ERROR ESPECÍFICO (ValueError) (Issue #6)
                except ValueError:
                    errores_omitidos += 1
                    print(f"⚠️ Dato no numérico omitido en registro: {fila[2]}")
                
                # 4. Manejar IndexError si alguna fila tiene menos columnas
                except IndexError:
                    errores_omitidos += 1
                    print(f"⚠️ Fila incompleta omitida: {fila}")

    # 5. CAPTURAR ERROR DE ARCHIVO NO ENCONTRADO (Issue #5)
    except FileNotFoundError:
        print(f"❌ Error: El archivo de datos '{ARCHIVO_ENTRADA}' no existe. Ejecute el script en la ubicación correcta.")
        return

    # 6. GENERAR Y GUARDAR REPORTE JSON (Issues #7 y #8)
    if datos_validos:
        promedio = sum(datos_validos) / len(datos_validos)
    else:
        promedio = 0

    reporte = {
        "fecha_analisis": os.popen('date +%Y-%m-%d').read().strip(), # Obtener la fecha del sistema
        "archivo_fuente": ARCHIVO_ENTRADA,
        "metricas": {
            "registros_totales": registros_totales,
            "registros_validos": len(datos_validos),
            "errores_identificados": errores_omitidos,
            "promedio_valores_validos": round(promedio, 2)
        }
    }
    
    # 7. IMPLEMENTAR ESCRITURA SEGURA JSON (Issue #8)
    try:
        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=4)
        print(f"\n✅ Análisis completado. Reporte guardado en '{ARCHIVO_SALIDA}'.")
    except Exception as e:
        print(f"❌ Error al guardar el reporte JSON: {e}")


def main():
    if not Path(ARCHIVO_ENTRADA).exists():
        crear_csv_ejemplo()

    analizar_datos()

if __name__ == "__main__":
    main()