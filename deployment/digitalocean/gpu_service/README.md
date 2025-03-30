# Omega GPU Service

This service provides GPU-accelerated image generation capabilities using Stable Diffusion models. It's designed to run on DigitalOcean GPU droplets and includes monitoring, logging, and automatic scaling features.

## Features

- GPU-accelerated image generation using Stable Diffusion 2.1
- Prometheus metrics for monitoring
- Automatic model caching
- Health checks and GPU information endpoints
- Automatic scaling based on GPU and CPU utilization
- Weekly backups of model and data volumes
- Comprehensive logging
- System optimization for GPU workloads

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the service.

### GPU Information

```
GET /gpu/info
```

Returns information about the GPU, including device name and memory usage.

### Generate Image

```
POST /generate
Content-Type: application/json

{
    "prompt": "Your text prompt here"
}
```

Generates an image based on the provided prompt.

## Monitoring

The service exposes Prometheus metrics on port 9100. Available metrics include:

- `requests_total`: Total number of requests processed
- `gpu_memory_usage_bytes`: Current GPU memory usage
- `model_inference_time_seconds`: Time taken for model inference

## Deployment

The service is deployed using DigitalOcean App Platform with the following configuration:

- Instance: GPU-L40S (1 GPU)
- Auto-scaling: 1-3 nodes based on GPU/CPU utilization
- Storage: 250GB volumes for models and data
- Weekly backups: Every Wednesday at 4 AM UTC

## Environment Variables

- `MODEL_CACHE_DIR`: Directory for model caching (default: /app/models)
- `PORT`: Application port (default: 8080)
- `NVIDIA_VISIBLE_DEVICES`: GPU devices to use (default: all)
- `GPU_MEMORY_FRACTION`: Maximum GPU memory fraction to use (default: 0.9)

## Security

- SSH key authentication required
- Firewall rules for ports 22 (SSH), 8080 (API), and 9100 (Prometheus)
- Automatic security updates
- Volume encryption enabled

## Logs

Logs are stored in `/app/logs/gpu_service.log` and include:

- Model initialization status
- Request processing
- Error tracking
- System events

## Development

To run the service locally:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the service:

```bash
python app.py
```

## Contributing

Please follow the project's coding standards and submit pull requests for any changes.
