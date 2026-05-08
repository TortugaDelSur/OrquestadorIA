import sys
import os
import shutil

# Asegurar que la raíz esté en el path para evitar errores de importación
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from openai import OpenAI
from dotenv import load_dotenv

# Imports de tus módulos locales
from agents.memory import AgentMemory
from agents.prompts import SYSTEM_PROMPT
from app.utils.excel_handler import process_sales_excel
from app.utils.pdf_generator import create_pdf_report
from app.utils.chart_generator import generate_sales_chart

load_dotenv()
app = FastAPI(title="Nexo IA Orquestador")
client = OpenAI()
memory = AgentMemory()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-sales/")
async def analyze_sales(file: UploadFile = File(...)):
    # 1. Guardar archivo temporalmente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Inicializamos la variable del gráfico como None por seguridad
    chart_path = None
    
    try:
        # 2. Generar gráfico basado en los datos brutos del Excel
        # Lo hacemos primero para que esté disponible para el PDF
        print(f"Generando gráfico para: {file.filename}")
        chart_path = generate_sales_chart(file_path)
        
        # 3. Procesar datos para la IA y consultar memoria
        current_data = process_sales_excel(file_path)
        past_context = memory.search_past_reports("tendencias generales de ventas")
        
        full_prompt = f"CONTEXTO HISTÓRICO:\n{past_context}\n\nDATOS ACTUALES:\n{current_data}"
        
        # 4. Inteligencia Artificial: Análisis del texto
        print("Consultando a GPT-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_prompt}
            ]
        )
        analysis = response.choices[0].message.content
        
        # 5. Generación del PDF Final (incluye el gráfico si se generó)
        pdf_filename = f"reporte_{file.filename.split('.')[0]}.pdf"
        print(f"📄 Creando PDF: {pdf_filename}")
        pdf_path = create_pdf_report(analysis, pdf_filename, chart_path)
        
        # 6. Guardar el análisis en la memoria de largo plazo
        memory.save_analysis(analysis, {"filename": file.filename})
        
        # 7. RETORNO: Envío del archivo para descarga automática
        return FileResponse(
            path=pdf_path, 
            filename=pdf_filename, 
            media_type='application/pdf'
        )
        
    except Exception as e:
        print(f"Error crítico en el proceso: {str(e)}")
        # Si algo falla, intentamos dar una respuesta clara
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
        
    finally:
        # Limpieza de archivos subidos para mantener el servidor ligero
        if os.path.exists(file_path):
            os.remove(file_path)
        # Nota: El gráfico temp_chart.png se sobreescribe en cada llamada, 
        # puedes borrarlo aquí si prefieres con os.remove(chart_path)

@app.get("/")
def read_root():
    return {"message": "Orquestador de IA Nexo operativo y listo para graficar"}