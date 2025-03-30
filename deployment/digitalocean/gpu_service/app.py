import os
import time
import torch
from flask import Flask, request, jsonify
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
import logging
from prometheus_client import start_http_server, Counter, Gauge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/gpu_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
REQUESTS_TOTAL = Counter('requests_total', 'Total number of requests processed')
GPU_MEMORY_USAGE = Gauge('gpu_memory_usage_bytes', 'Current GPU memory usage in bytes')
MODEL_INFERENCE_TIME = Gauge('model_inference_time_seconds', 'Time taken for model inference')

app = Flask(__name__)

# Initialize models
def init_models():
    logger.info("Initializing models...")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    
    model_path = os.getenv("MODEL_CACHE_DIR", "/app/models")
    
    try:
        txt2img_model = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            cache_dir=model_path
        ).to(device)
        
        logger.info("Models initialized successfully")
        return txt2img_model
    except Exception as e:
        logger.error(f"Error initializing models: {str(e)}")
        raise

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# GPU info endpoint
@app.route('/gpu/info')
def gpu_info():
    if torch.cuda.is_available():
        return jsonify({
            "device_name": torch.cuda.get_device_name(0),
            "memory_allocated": torch.cuda.memory_allocated(),
            "memory_cached": torch.cuda.memory_reserved()
        })
    elif torch.backends.mps.is_available():
        return jsonify({
            "device_name": "Apple MPS",
            "memory_allocated": "N/A",
            "memory_cached": "N/A"
        })
    else:
        return jsonify({
            "device_name": "CPU",
            "memory_allocated": "N/A",
            "memory_cached": "N/A"
        })

# Image generation endpoint
@app.route('/generate', methods=['POST'])
def generate():
    REQUESTS_TOTAL.inc()
    
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        logger.info(f"Generating image for prompt: {prompt}")
        
        with MODEL_INFERENCE_TIME.time():
            image = model.generate(prompt)
            
        if torch.cuda.is_available():
            GPU_MEMORY_USAGE.set(torch.cuda.memory_allocated())
        
        # Save the image
        output_path = os.path.join("/app/data", "generated_images")
        os.makedirs(output_path, exist_ok=True)
        image_path = os.path.join(output_path, f"generated_{int(time.time())}.png")
        image.save(image_path)
        
        return jsonify({
            "status": "success",
            "image_path": image_path
        })
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9100)
    
    # Initialize models
    model = init_models()
    
    # Start Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 