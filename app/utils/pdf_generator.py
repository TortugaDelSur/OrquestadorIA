from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
import os

def create_pdf_report(analysis_text, filename="reporte_ia.pdf", chart_path=None):
    """
    Toma el texto generado por la IA y lo convierte en un PDF estructurado.
    """
    # 1. Asegurar que la carpeta de reportes exista
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    report_path = os.path.join(output_dir, filename)
    
    # 2. Configuración del lienzo (Canvas)
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter # Tamaño estándar (612 x 792 puntos)
    
    # 3. Dibujar Encabezado
    c.setFillColor(colors.HexColor("#1A237E")) # Azul institucional
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "NEXO IA: Informe de Ventas")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, "Análisis automático generado por Orquestador de Inteligencia Artificial")

    # 4. Configuración de cuerpo de texto
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    
    # Margen izquierdo y superior inicial
    margin_x = 50
    current_y = height - 120
    line_width = width - 100 # Margen derecho de 50 (50 + 50 = 100)
    
    # 5. Procesar el texto para que no se salga de los márgenes (Word Wrap)
    # Reemplazamos los saltos de línea dobles por uno simple para procesar
    paragraphs = analysis_text.split('\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip(): # Espacio entre párrafos
            current_y -= 15
            continue
            
        # Dividir el párrafo en líneas que quepan en el ancho definido
        wrapped_lines = simpleSplit(paragraph, "Helvetica", 12, line_width)
        
        for line in wrapped_lines:
            # Control de salto de página
            if current_y < 50:
                c.showPage() # Crear nueva página
                c.setFont("Helvetica", 12)
                current_y = height - 50
            
            c.drawString(margin_x, current_y, line)
            current_y -= 15 # Espaciado entre líneas
        
        current_y -= 5 # Espacio extra tras cada párrafo

    if chart_path and os.path.exists(chart_path):
        if current_y < 300: # Si no queda espacio, nueva página
            c.showPage()
            current_y = height - 50
        
        c.drawImage(chart_path, 50, current_y - 250, width=500, preserveAspectRatio=True)
        # Limpiar la imagen temporal después de usarla
        os.remove(chart_path)
    # 6. Finalizar y guardar
    c.save()
    print(f"PDF generado exitosamente en: {report_path}")
    return report_path