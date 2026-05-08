import pandas as pd

def process_sales_excel(file_path):
    """Lee un Excel y devuelve un resumen en texto para el LLM."""
    try:
        df = pd.read_excel(file_path)
        
        # Limpieza básica: quitar filas vacías y obtener info clave
        summary_stats = df.describe(include='all').to_string()
        preview_data = df.head(10).to_string()
        
        context = f"""
        Resumen Estadístico del Excel:
        {summary_stats}
        
        Primeras 10 filas de datos:
        {preview_data}
        """
        return context
    except Exception as e:
        return f"Error procesando el archivo: {e}"