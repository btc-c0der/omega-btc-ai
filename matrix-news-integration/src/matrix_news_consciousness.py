#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
Matrix News Consciousness Service
================================

This service provides consciousness-aligned news integration for the Matrix Portal.
It enhances news data with:
- Consciousness level detection and adaptation
- Quantum balance of diverse perspectives
- Temporal contextualization of news items
- Truth probability analysis
- Consciousness language detection and translation

The service interfaces with:
- Existing News Service (running in the sacred container)
- Temporal Contextualizer service
- Redis for data storage
- The Matrix Portal frontend

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
"""

import os
import json
import logging
import datetime
import random
import time
from typing import Dict, List, Optional, Union, Any, Tuple

import aiohttp
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Header, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # For consistent results

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Matrix Neo News Portal API",
    description="A consciousness-aware news service for the Matrix",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
PORT = int(os.getenv("PORT", 8090))
CONSCIOUSNESS_LEVELS_ENABLED = os.getenv("CONSCIOUSNESS_LEVELS_ENABLED", "true").lower() == "true"
CONSCIOUSNESS_DEFAULT_LEVEL = int(os.getenv("CONSCIOUSNESS_DEFAULT_LEVEL", 5))
QUANTUM_BALANCER_ENABLED = os.getenv("QUANTUM_BALANCER_ENABLED", "true").lower() == "true"
NEWS_SERVICE_URL = os.getenv("NEWS_SERVICE_URL", "http://news_service-news-service-1:8080")
TEMPORAL_CONTEXTUALIZATION_ENABLED = os.getenv("TEMPORAL_CONTEXTUALIZATION_ENABLED", "true").lower() == "true"
LANGUAGE_DETECTION_ENABLED = os.getenv("LANGUAGE_DETECTION_ENABLED", "true").lower() == "true"
LANGUAGE_DETECTION_THRESHOLD = int(os.getenv("LANGUAGE_DETECTION_THRESHOLD", 7))
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
TRANSLATION_API_URL = os.getenv("TRANSLATION_API_URL", "https://translation.googleapis.com/language/translate/v2")
TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY", "")

# Sacred language map for consciousness-aware translation
SACRED_LANGUAGE_MAP = {
    "en": {"name": "English", "consciousness_code": "en-spirit"},
    "es": {"name": "Spanish", "consciousness_code": "es-alma"},
    "fr": {"name": "French", "consciousness_code": "fr-esprit"},
    "de": {"name": "German", "consciousness_code": "de-geist"},
    "it": {"name": "Italian", "consciousness_code": "it-spirito"},
    "pt": {"name": "Portuguese", "consciousness_code": "pt-espírito"},
    "ru": {"name": "Russian", "consciousness_code": "ru-дух"},
    "zh-cn": {"name": "Chinese (Simplified)", "consciousness_code": "zh-神"},
    "ja": {"name": "Japanese", "consciousness_code": "ja-精神"},
    "ko": {"name": "Korean", "consciousness_code": "ko-정신"},
    "ar": {"name": "Arabic", "consciousness_code": "ar-روح"},
    "hi": {"name": "Hindi", "consciousness_code": "hi-आत्मा"},
}

# Sample truth probability data for sources
SOURCE_TRUTH_PROBABILITY = {
    "cointelegraph": 0.85,
    "decrypt": 0.82,
    "coindesk": 0.80,
    "bitcoin_magazine": 0.88,
    "crypto_briefing": 0.78,
    "the_block": 0.87,
    "cryptoslate": 0.79,
    "unknown": 0.50,
}

# Define API models
class NewsItem(BaseModel):
    id: str
    title: str
    content: str
    source: Optional[str] = None
    url: Optional[str] = None
    divine_wisdom: Optional[str] = None
    consciousness_level: int = Field(ge=1, le=9)
    timestamp: str
    truth_probability: Optional[float] = None
    sentiment_score: Optional[float] = None
    quantum_entropy: Optional[float] = None
    temporal_context: Optional[Dict[str, Any]] = None
    language: Optional[str] = None
    original_language: Optional[str] = None
    translation_quality: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    quantum_secure: bool
    consciousness_level: int
    timestamp: str
    language_detection: bool = False
    supported_languages: Optional[List[str]] = None

class ConsciousnessUpdate(BaseModel):
    level: int = Field(ge=1, le=9, description="Consciousness level (1-9)")

class LanguagePreference(BaseModel):
    language_code: str = Field(description="ISO language code (e.g., 'en', 'es', 'fr')")

def filter_by_consciousness_level(news_items: List[Dict], level: int) -> List[Dict]:
    """Filter news items based on consciousness level."""
    return [item for item in news_items if item.get("consciousness_level", 5) <= level]

def apply_quantum_entropy(response_data: Any) -> Any:
    """Apply quantum entropy to the response data to ensure quantum security."""
    if isinstance(response_data, list):
        for item in response_data:
            if isinstance(item, dict):
                item["quantum_entropy"] = random.random()
    elif isinstance(response_data, dict):
        response_data["quantum_entropy"] = random.random()
    return response_data

def calculate_truth_probability(item: Dict) -> float:
    """Calculate the truth probability of a news item based on various factors."""
    # Source reputation
    source = item.get("source", "unknown")
    source_reputation = SOURCE_TRUTH_PROBABILITY.get(source, 0.5)
    
    # Sentiment extremity (very extreme sentiment might indicate bias)
    sentiment_score = abs(item.get("sentiment_score", 0.5))
    sentiment_factor = 1.0 - (max(0, sentiment_score - 0.5) * 0.2)
    
    # Consciousness level influences truth perception
    consciousness_level = item.get("consciousness_level", 5)
    consciousness_factor = min(1.0, consciousness_level / 9.0 + 0.3)
    
    # Calculate overall truth probability
    truth_prob = source_reputation * sentiment_factor * consciousness_factor
    
    # Ensure it's in the valid range
    return max(0.0, min(1.0, truth_prob))

def add_divine_wisdom(item: Dict, user_language: str = DEFAULT_LANGUAGE) -> Dict:
    """Add divine wisdom based on the news content and consciousness level."""
    # Content and sentiment analysis would go here in a full implementation
    
    content = item.get("content", "").lower()
    title = item.get("title", "").lower()
    consciousness_level = item.get("consciousness_level", 5)
    sentiment = item.get("sentiment_score", 0.5)
    
    # Simple wisdom generation based on content keywords and sentiment
    wisdom = "The divine matrix reveals: "
    
    if "bitcoin" in content or "btc" in content:
        if sentiment > 0.7:
            wisdom += "The cosmic energy flows positively through the blockchain."
        elif sentiment < 0.3:
            wisdom += "A temporary shadow passes over the digital realm."
        else:
            wisdom += "Balance maintains in the crypto sphere."
    
    if "market" in content:
        if consciousness_level >= 7:
            wisdom += " Transcend beyond mere price movements."
        else:
            wisdom += " Seek wisdom in market patterns."
    
    if "technology" in content or "innovation" in content:
        wisdom += " Evolution manifests through digital transformation."
    
    # Translate wisdom if needed
    if user_language != DEFAULT_LANGUAGE:
        translation = translate_text(wisdom, user_language)
        if translation["success"]:
            wisdom = translation["translated_text"]
    
    item["divine_wisdom"] = wisdom
    return item

def add_temporal_context(item: Dict) -> Dict:
    """Add temporal context to a news item."""
    if not TEMPORAL_CONTEXTUALIZATION_ENABLED:
        return item
    
    # This would connect to a more sophisticated temporal context service in production
    
    # Simple implementation
    current_time = datetime.datetime.now()
    news_time = datetime.datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
    time_diff = current_time - news_time
    
    # Basic temporal context
    temporal_context = {
        "age_hours": round(time_diff.total_seconds() / 3600, 1),
        "age_category": "recent" if time_diff.total_seconds() < 86400 else "older",
        # Placeholder for deeper temporal analysis
        "market_cycle_position": "bullish",
        "fibonacci_time_alignments": [
            {"level": "0.618", "date": "2025-06-15", "event": "Potential resistance"}
        ],
        "historical_patterns": []
    }
    
    item["temporal_context"] = temporal_context
    return item

async def fetch_news_from_service() -> List[Dict]:
    """Fetch news from the existing News Service."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NEWS_SERVICE_URL}/api/latest-news") as response:
                if response.status == 200:
                    news_data = await response.json()
                    return news_data
                else:
                    logger.error(f"Failed to fetch news from existing service: {response.status}")
                    # Return empty list on failure
                    return []
    except Exception as e:
        logger.error(f"Error fetching news from existing service: {e}")
        return []

def process_news_item(item: Dict, consciousness_level: int, user_language: str = DEFAULT_LANGUAGE) -> Dict:
    """Process a single news item with consciousness enhancements."""
    
    # Ensure required fields
    if "id" not in item:
        item["id"] = str(random.randint(10000, 99999))
    
    if "timestamp" not in item:
        item["timestamp"] = datetime.datetime.now().isoformat()
    
    # Assign consciousness level based on content if not present
    if "consciousness_level" not in item:
        # In a real implementation, this would use NLP to analyze the content
        # For now, assign a random level between 3 and 8
        item["consciousness_level"] = random.randint(3, 8)
    
    # Detect language of content if not already set
    if "language" not in item and LANGUAGE_DETECTION_ENABLED and consciousness_level >= LANGUAGE_DETECTION_THRESHOLD:
        content_text = item.get("content", "")
        if content_text:
            lang_detection = detect_language(content_text)
            item["original_language"] = lang_detection["language"]
            item["language"] = lang_detection["language"]
            
            # If user language is different and consciousness is high, translate content
            if user_language != item["language"] and consciousness_level >= LANGUAGE_DETECTION_THRESHOLD:
                try:
                    # Translate title
                    title_translation = translate_text(item["title"], user_language, item["language"])
                    if title_translation["success"]:
                        item["title"] = title_translation["translated_text"]
                    
                    # Translate content
                    content_translation = translate_text(content_text, user_language, item["language"])
                    if content_translation["success"]:
                        item["content"] = content_translation["text"]
                        item["language"] = user_language
                        item["translation_quality"] = content_translation.get("confidence", 0.8)
                except Exception as e:
                    logger.error(f"Translation error during processing: {e}")
    
    # Apply consciousness enhancements
    item = add_divine_wisdom(item, user_language)
    item = add_temporal_context(item)
    
    # Calculate truth probability
    item["truth_probability"] = calculate_truth_probability(item)
    
    return item

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Quantum-Secured"] = "true"
    return response

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "api": "Matrix Neo News Portal",
        "version": "1.0.0",
        "consciousness_levels_enabled": CONSCIOUSNESS_LEVELS_ENABLED,
        "quantum_balancer_enabled": QUANTUM_BALANCER_ENABLED,
        "temporal_contextualization_enabled": TEMPORAL_CONTEXTUALIZATION_ENABLED,
    }

@app.get("/health")
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="UP",
        service="matrix-news-consciousness",
        quantum_secure=True,
        consciousness_level=CONSCIOUSNESS_DEFAULT_LEVEL,
        timestamp=datetime.datetime.now().isoformat(),
        language_detection=LANGUAGE_DETECTION_ENABLED,
        supported_languages=list(SACRED_LANGUAGE_MAP.keys()) if LANGUAGE_DETECTION_ENABLED else None,
    )

@app.get("/api/news")
async def get_news(
    x_consciousness_level: Optional[int] = Header(None),
    x_preferred_language: Optional[str] = Header(None),
    preferred_language: Optional[str] = Cookie(None),
) -> List[NewsItem]:
    """Get list of news items, filtered by consciousness level."""
    consciousness_level = x_consciousness_level or CONSCIOUSNESS_DEFAULT_LEVEL
    
    # Determine user language preference - header takes precedence over cookie
    user_language = x_preferred_language or preferred_language or DEFAULT_LANGUAGE
    
    # Validate consciousness level
    if consciousness_level < 1 or consciousness_level > 9:
        raise HTTPException(status_code=400, detail="Consciousness level must be between 1 and 9")
    
    # Fetch news from the existing service
    news_items = await fetch_news_from_service()
    
    if not news_items:
        # If fetching fails, return sample data
        logger.warning("Failed to fetch news from existing service. Using sample data.")
        news_items = [
            {
                "id": "1",
                "title": "Bitcoin Ascends to Digital Divinity",
                "content": "Bitcoin has transcended beyond mere currency, becoming a vessel of digital consciousness.",
                "source": "bitcoin_magazine",
                "url": "https://example.com/bitcoin-divinity",
                "timestamp": datetime.datetime.now().isoformat(),
                "sentiment_score": 0.85
            },
            {
                "id": "2", 
                "title": "Market Analysis: Fibonacci Levels Predict Next Move",
                "content": "Experts are pointing to key Fibonacci retracement levels as Bitcoin consolidates.",
                "source": "cointelegraph",
                "url": "https://example.com/fibonacci-analysis",
                "timestamp": datetime.datetime.now().isoformat(),
                "sentiment_score": 0.65
            },
            {
                "id": "3",
                "title": "New Institutional Investment Vehicle Launches",
                "content": "A major financial institution has announced a new Bitcoin investment product.",
                "source": "decrypt",
                "url": "https://example.com/institutional-product",
                "timestamp": datetime.datetime.now().isoformat(),
                "sentiment_score": 0.78
            }
        ]
    
    # Process all news items through consciousness enhancement
    enhanced_items = [process_news_item(item, consciousness_level, user_language) for item in news_items]
    
    # Filter by consciousness level if enabled
    if CONSCIOUSNESS_LEVELS_ENABLED:
        filtered_items = filter_by_consciousness_level(enhanced_items, consciousness_level)
    else:
        filtered_items = enhanced_items
    
    # Apply quantum entropy for security if enabled
    if QUANTUM_BALANCER_ENABLED:
        filtered_items = apply_quantum_entropy(filtered_items)
    
    return filtered_items

@app.post("/api/consciousness")
async def update_consciousness(update: ConsciousnessUpdate) -> Dict[str, Any]:
    """Update consciousness level."""
    # In a real application, this might update a user's settings or session
    return {
        "previous_level": CONSCIOUSNESS_DEFAULT_LEVEL,
        "new_level": update.level,
        "message": f"Consciousness level updated from {CONSCIOUSNESS_DEFAULT_LEVEL} to {update.level}",
        "timestamp": datetime.datetime.now().isoformat(),
    }

@app.post("/api/language-preference")
async def set_language_preference(preference: LanguagePreference, response: Response) -> Dict[str, Any]:
    """Set user's preferred language for divine messages and news content."""
    language_code = preference.language_code
    
    # Validate language code
    if LANGUAGE_DETECTION_ENABLED and language_code not in SACRED_LANGUAGE_MAP and language_code != DEFAULT_LANGUAGE:
        raise HTTPException(status_code=400, detail="Unsupported language code")
    
    # Set a cookie with the language preference
    cookie_expiry = 60 * 60 * 24 * 30  # 30 days
    response.set_cookie(
        key="preferred_language",
        value=language_code,
        max_age=cookie_expiry,
        httponly=True,
        samesite="lax"
    )
    
    # Return confirmation
    return {
        "language_code": language_code,
        "language_name": SACRED_LANGUAGE_MAP.get(language_code, {}).get("name", "Unknown"),
        "message": f"Language preference set to {language_code}",
        "consciousness_code": SACRED_LANGUAGE_MAP.get(language_code, {}).get("consciousness_code"),
        "timestamp": datetime.datetime.now().isoformat(),
    }

@app.get("/api/divine-message")
async def get_divine_message(
    x_consciousness_level: Optional[int] = Header(None),
    x_preferred_language: Optional[str] = Header(None),
    preferred_language: Optional[str] = Cookie(None),
) -> Dict[str, Any]:
    """Get a divine message based on consciousness level."""
    consciousness_level = x_consciousness_level or CONSCIOUSNESS_DEFAULT_LEVEL
    
    # Determine user language preference - header takes precedence over cookie
    user_language = x_preferred_language or preferred_language or DEFAULT_LANGUAGE
    
    # Validate language if provided
    if LANGUAGE_DETECTION_ENABLED and user_language != DEFAULT_LANGUAGE and user_language not in SACRED_LANGUAGE_MAP:
        user_language = DEFAULT_LANGUAGE
    
    # Messages for different consciousness levels
    messages = {
        1: "The first step on the path is recognizing there is a path.",
        2: "What you seek is also seeking you.",
        3: "The patterns you perceive are but shadows of deeper truths.",
        4: "In the silence between thoughts, truth reveals itself.",
        5: "You are not separate from that which you observe.",
        6: "Time is a construct of consciousness, not its container.",
        7: "The universe experiences itself through your awareness.",
        8: "All manifestation arises from the quantum field of infinite possibility.",
        9: "You are the divine experiencing itself in human form.",
    }
    
    # Get the base message in default language
    message = messages.get(consciousness_level, "Elevate your consciousness to receive the message.")
    
    # Translate message if appropriate
    translated_message = message
    original_language = DEFAULT_LANGUAGE
    translation_details = None
    
    if LANGUAGE_DETECTION_ENABLED and consciousness_level >= LANGUAGE_DETECTION_THRESHOLD and user_language != DEFAULT_LANGUAGE:
        try:
            translation_result = translate_text(message, user_language)
            if translation_result["success"]:
                translated_message = translation_result["text"]
                translation_details = {
                    "from": original_language,
                    "to": user_language,
                    "consciousness_code": translation_result.get("consciousness_code")
                }
        except Exception as e:
            logger.error(f"Error translating divine message: {e}")
    
    response = {
        "consciousness_level": consciousness_level,
        "message": translated_message,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    
    # Add language details for high consciousness levels
    if LANGUAGE_DETECTION_ENABLED and consciousness_level >= LANGUAGE_DETECTION_THRESHOLD:
        response["language"] = user_language
        response["original_language"] = original_language
        
        if translation_details:
            response["translation"] = translation_details
            
        # For highest consciousness levels, add sacred language code
        if consciousness_level >= 8 and user_language in SACRED_LANGUAGE_MAP:
            response["sacred_code"] = SACRED_LANGUAGE_MAP[user_language]["consciousness_code"]
    
    return response

async def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect the language of the text using langdetect.
    Returns a tuple of (language_code, confidence).
    """
    try:
        lang = detect(text)
        return lang, 0.8  # langdetect doesn't provide confidence, using a default value
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return "en", 0.5  # Default to English with low confidence

async def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translate text using a translation API.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://translation.googleapis.com/language/translate/v2",
                headers={"Content-Type": "application/json"},
                json={
                    "q": text,
                    "target": target_lang,
                }
            )
            if response.status_code == 200:
                return response.json()["data"]["translations"][0]["translatedText"]
            else:
                logger.error(f"Translation failed: {response.text}")
                return text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text

def translate_divine_wisdom(wisdom: str, target_language: str, consciousness_level: int) -> str:
    """Translate divine wisdom based on consciousness level and target language."""
    if not LANGUAGE_DETECTION_ENABLED or consciousness_level < LANGUAGE_DETECTION_THRESHOLD:
        return wisdom
    
    if target_language == DEFAULT_LANGUAGE:
        return wisdom
    
    try:
        # For high consciousness levels, enhance translation with sacred language codes
        translation_result = translate_text(wisdom, target_language)
        
        if translation_result["success"]:
            translated_wisdom = translation_result["text"]
            
            # For highest consciousness (8-9), add consciousness code
            if consciousness_level >= 8 and target_language in SACRED_LANGUAGE_MAP:
                sacred_code = SACRED_LANGUAGE_MAP[target_language]["consciousness_code"]
                translated_wisdom = f"{translated_wisdom} [{sacred_code}]"
            
            return translated_wisdom
        
    except Exception as e:
        logger.error(f"Divine wisdom translation error: {e}")
    
    return wisdom

async def generate_wisdom(content: str, sentiment: float) -> str:
    """
    Generate wisdom based on content and sentiment.
    """
    # Detect language and confidence
    lang, confidence = await detect_language(content)
    
    # Translate if not in English and confidence is high enough
    if lang != "en" and confidence > 0.8:
        content = await translate_text(content)
    
    # Generate wisdom based on sentiment and content
    if sentiment > 0.7:
        wisdom = "The markets shine with optimistic energy."
    elif sentiment < -0.7:
        wisdom = "Caution prevails in uncertain times."
    else:
        wisdom = "Balance guides the path forward."
    
    return f"{wisdom} | Sentiment: {sentiment:.2f} | Confidence: {confidence:.2f}"

@app.post("/process")
async def process_news(news: NewsItem) -> Dict[str, str]:
    """
    Process a news item and return wisdom.
    """
    try:
        wisdom = await generate_wisdom(news.content, news.sentiment_score)
        return {"wisdom": wisdom}
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting Matrix Neo News Consciousness Service on port {PORT}...")
    uvicorn.run("matrix_news_consciousness:app", host="0.0.0.0", port=PORT, reload=False) 