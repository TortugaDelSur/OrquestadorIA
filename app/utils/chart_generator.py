import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_sales_chart(file_path):
    try:
        df = pd.read_excel(file_path)
        # Forzar nombres a minúsculas para comparar
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # BUSCAR COLUMNAS (Flexibilidad)
        # Busca cualquier columna que contenga 'prod' o 'item'
        prod_col = next((c for c in df.columns if 'prod' in c or 'item' in c), None)
        # Busca cualquier columna que contenga 'total', 'venta' o 'precio'
        val_col = next((c for c in df.columns if 'total' in c or 'venta' in c or 'precio' in c), None)

        if prod_col and val_col:
            # Agrupar y graficar
            df_plot = df.groupby(prod_col)[val_col].sum().sort_values(ascending=False).head(10)
            
            plt.figure(figsize=(8, 4))
            df_plot.plot(kind='bar', color='#1A237E')
            plt.title('Resumen de Ventas por Producto')
            plt.tight_layout()
            
            c_path = "reports/temp_chart.png"
            plt.savefig(c_path)
            plt.close()
            return c_path
        else:
            print(f"Columnas encontradas: {list(df.columns)}. No coinciden con 'producto'/'total'.")
            return None
    except Exception as e:
        print(f"Error en chart_generator: {e}")
        return None