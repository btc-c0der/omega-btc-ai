# OMEGA BTC AI - API Documentation

This directory contains the OpenAPI (Swagger) documentation for the OMEGA BTC AI system's backend and frontend APIs.

## API Documentation Files

- `backend-api.yaml`: Documentation for the backend Reggae Dashboard API
- `frontend-api.yaml`: Documentation for the frontend Reggae Dashboard API

## Viewing the Documentation

You can view the API documentation using any OpenAPI/Swagger UI tool. Here are some options:

1. **Swagger UI Online Editor**
   - Visit [Swagger Editor](https://editor.swagger.io/)
   - Copy and paste the contents of either YAML file

2. **Redoc**
   - Visit [Redoc](https://redocly.github.io/redoc/)
   - Use the URL to your hosted YAML file

3. **Local Development**

   ```bash
   # Install swagger-ui-cli
   npm install -g swagger-ui-cli

   # Serve the backend API docs
   swagger-ui-cli serve docs/api/backend-api.yaml

   # Serve the frontend API docs
   swagger-ui-cli serve docs/api/frontend-api.yaml
   ```

## API Structure

### Backend API (Port 8000)

The backend API provides core functionality for:

- Health monitoring
- Trap probability data
- Position data
- System information
- Real-time WebSocket updates

### Frontend API (Port 5001)

The frontend API offers:

- Trap metrics and analytics
- Trap detection data
- Price data
- Historical timeline
- Real-time WebSocket streaming

## Development

When adding new endpoints or modifying existing ones:

1. Update the appropriate YAML file
2. Ensure all parameters and responses are properly documented
3. Add examples where possible
4. Update the README if necessary

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This API documentation is part of the OMEGA BTC AI project and is licensed under the same terms as the main project.
