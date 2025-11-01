# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any

from config import settings
from schemas import PatientData, AnalysisResponse
from model_loader import ModelLoader
from unified_analyzer import UnifiedAnalyzer

# Initialize FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model_loader = None
analyzer = None

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global model_loader, analyzer
    try:
        model_loader = ModelLoader(settings)
        analyzer = UnifiedAnalyzer(model_loader)
        print("🎉 Multi-Modal Breast Cancer API Started Successfully!")
    except Exception as e:
        print(f"❌ Startup error: {e}")

# Alternative lifespan context manager for newer FastAPI versions
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model_loader, analyzer
    try:
        model_loader = ModelLoader(settings)
        analyzer = UnifiedAnalyzer(model_loader)
        print("🎉 Multi-Modal Breast Cancer API Started Successfully!")
    except Exception as e:
        print(f"❌ Startup error: {e}")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down API...")

# Update app initialization to use lifespan
# app = FastAPI(
#     title=settings.API_TITLE,
#     version=settings.API_VERSION,
#     description=settings.API_DESCRIPTION,
#     lifespan=lifespan
# )

@app.get("/")
async def root():
    return {
        "message": "Multi-Modal Breast Cancer AI API",
        "version": settings.API_VERSION,
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    if not model_loader:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    available_modalities = model_loader.get_available_modalities()
    
    return {
        "status": "healthy",
        "available_modalities": available_modalities,
        "total_models_loaded": len([m for m in model_loader.models.values() if m is not None])
    }

@app.get("/models/available")
async def get_available_models():
    """Get list of available models and capabilities"""
    if not model_loader:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    modalities = model_loader.get_available_modalities()
    
    return {
        "available_modalities": modalities,
        "genomics_available": 'genomics' in modalities,
        "imaging_available": 'imaging' in modalities or 'lightweight_imaging' in modalities,
        "nlp_available": 'nlp' in modalities
    }

@app.post("/analyze/comprehensive", response_model=AnalysisResponse)
async def comprehensive_analysis(patient_data: PatientData):
    """
    Comprehensive multi-modal breast cancer analysis
    
    Integrates genomics, imaging, and clinical data for complete assessment
    """
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")
    
    try:
        results = analyzer.comprehensive_analysis(patient_data.dict())
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/analyze/genomics")
async def analyze_genomics(patient_data: PatientData):
    """Genomics-only analysis"""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")
    
    try:
        results = analyzer.genomics_analysis(patient_data.dict())
        return {"modality": "genomics", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Genomics analysis error: {str(e)}")

@app.post("/analyze/imaging")
async def analyze_imaging(patient_data: PatientData):
    """Imaging-only analysis (all modalities)"""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")
    
    try:
        results = analyzer.imaging_analysis(patient_data.dict())
        return {"modality": "imaging", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Imaging analysis error: {str(e)}")

@app.post("/analyze/clinical-text")
async def analyze_clinical_text(patient_data: PatientData):
    """Clinical text NLP analysis"""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")
    
    try:
        results = analyzer.nlp_analysis(patient_data.dict())
        return {"modality": "clinical_nlp", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NLP analysis error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )