"""
FastAPI Routes for OMEGA BTC AI Bot Personification

This module provides FastAPI routes for the bot personification feature,
allowing interaction with personas through the API.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel

from omega_ai.personification.persona_manager import PersonaManager
from omega_ai.personification.dashboard_integration import DashboardIntegration


# Models for API requests/responses
class PersonaChangeRequest(BaseModel):
    """Request model for changing the active persona."""
    persona: str


class PersonaAnalysisRequest(BaseModel):
    """Request model for persona analysis."""
    dataId: Optional[str] = None


class PersonaResponse(BaseModel):
    """Response model with persona information."""
    name: str
    description: str
    style: Dict[str, Any]
    is_active: bool


class PersonaListResponse(BaseModel):
    """Response model for list of personas."""
    personas: List[PersonaResponse]


class AnalysisResponse(BaseModel):
    """Response model for persona analysis."""
    success: bool
    analysisHtml: Optional[str] = None
    analysisType: Optional[str] = None
    error: Optional[str] = None


# Dependency for getting persona manager
def get_persona_manager():
    """Dependency to get the persona manager instance."""
    return PersonaManager()


def get_dashboard_integration(
    persona_manager: PersonaManager = Depends(get_persona_manager)
):
    """Dependency to get the dashboard integration instance."""
    return DashboardIntegration(persona_manager=persona_manager)


# Create router
router = APIRouter(tags=["personas"])


@router.get("/api/personas", response_model=PersonaListResponse)
async def get_personas(
    persona_manager: PersonaManager = Depends(get_persona_manager)
):
    """Get all available personas."""
    persona_details = persona_manager.get_persona_details()
    return {"personas": persona_details}


@router.get("/api/personas/active", response_model=PersonaResponse)
async def get_active_persona(
    persona_manager: PersonaManager = Depends(get_persona_manager)
):
    """Get the currently active persona."""
    active_persona = persona_manager.get_active_persona()
    
    if not active_persona:
        raise HTTPException(status_code=404, detail="No active persona found")
    
    return {
        "name": active_persona.name,
        "description": active_persona.description,
        "style": active_persona.style.to_dict(),
        "is_active": True
    }


@router.post("/api/change_persona", response_model=Dict[str, Any])
async def change_persona(
    request: PersonaChangeRequest,
    persona_manager: PersonaManager = Depends(get_persona_manager)
):
    """Change the active persona."""
    success = persona_manager.set_active_persona(request.persona)
    
    if success:
        return {"success": True, "persona": request.persona}
    else:
        return {"success": False, "error": f"Persona '{request.persona}' not found"}


@router.post("/api/persona_analysis/{analysis_type}", response_model=AnalysisResponse)
async def get_persona_analysis(
    analysis_type: str,
    request: PersonaAnalysisRequest,
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get persona analysis for the specified type."""
    try:
        # Get appropriate data based on analysis type
        if analysis_type == "market":
            # Mock market data for demonstration
            data = {
                "price": 50000.0,
                "price_change_24h": 2.5,
                "volume_24h": 25000000000,
                "trend": "bullish",
                "signal_strength": 0.7
            }
        elif analysis_type == "position":
            # Get position data (mock for demonstration)
            data = {
                "id": request.dataId,
                "symbol": "BTCUSDT",
                "side": "long",
                "entry_price": 48000.0,
                "current_price": 50000.0,
                "pnl": 2000.0,
                "pnl_percentage": 4.17
            }
        elif analysis_type == "recommendation":
            # Mock recommendation data
            data = {
                "price": 50000.0,
                "trend": "bullish",
                "signal_strength": 0.7,
                "fib_level": "0.618",
                "fib_price": 48310.0,
                "trap_probability": 0.2
            }
        elif analysis_type == "performance":
            # Mock performance data
            data = {
                "total_pnl": 12500.0,
                "win_rate": 0.65,
                "trade_count": 25,
                "avg_win": 1200.0,
                "avg_loss": -400.0
            }
        else:
            return {
                "success": False,
                "error": f"Unknown analysis type: {analysis_type}"
            }
        
        # Generate analysis HTML
        analysis_html = dashboard.get_persona_analysis_html(data, analysis_type)
        
        return {
            "success": True,
            "analysisHtml": analysis_html,
            "analysisType": analysis_type
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/api/persona_css")
async def get_persona_css(
    persona_name: Optional[str] = None,
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get CSS for the specified or active persona."""
    return dashboard.get_persona_css(persona_name)


@router.get("/api/persona_js")
async def get_persona_js(
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get JavaScript for persona functionality."""
    return dashboard.get_persona_js()


@router.get("/api/persona_card_html")
async def get_persona_card_html(
    persona_name: Optional[str] = None,
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get HTML for the persona card."""
    return dashboard.get_persona_card_html(persona_name)


@router.get("/api/bitget_traders_panel")
async def get_bitget_traders_panel(
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get HTML for the Bitget trader profiles panel."""
    return dashboard.get_bitget_traders_panel_html()


@router.get("/api/profile_comparison")
async def get_profile_comparison(
    dashboard: DashboardIntegration = Depends(get_dashboard_integration)
):
    """Get HTML for the profile comparison table."""
    return dashboard.get_profile_comparison_html() 