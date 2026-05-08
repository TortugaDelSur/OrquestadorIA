# Nexo IA: Orquestador de Agentes con Memoria y Visualización 🧠📊

Este proyecto es un Orquestador de Inteligencia Artificial diseñado para PyMEs. Analiza datos de ventas desde Excel, genera gráficos automáticos y redacta informes ejecutivos en PDF, utilizando memoria vectorial para recordar contextos de análisis previos.

## ✨ Funcionalidades
- **Análisis Predictivo**: Utiliza GPT-4o-mini para identificar tendencias.
- **Memoria Vectorial**: ChromaDB permite al agente comparar datos con meses anteriores.
- **Visualización Automatizada**: Generación de gráficos de barras con Matplotlib.
- **API Profesional**: Interfaz lista para integración con FastAPI.

## 🛠️ Tecnologías
- Python 3.10+
- FastAPI (Backend)
- OpenAI API (LLM & Embeddings)
- ChromaDB (Vector Store)
- ReportLab (PDF Engine)
- Matplotlib & Pandas (Data Science)

## 🚀 Instalación Rápida
1. Clonar: `git clone <tu-url-de-repo>`
2. Instalar: `pip install -r requirements.txt`
3. Configurar `.env`: Agrega tu `OPENAI_API_KEY`.
4. Run: `python -m uvicorn app.main:app --reload`