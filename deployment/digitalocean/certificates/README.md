
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# SSL Certificates Directory

This directory contains SSL certificates used for secure connections in the OMEGA BTC AI deployment.

## Security Considerations

1. **File Permissions**
   - SSL certificates should have restricted permissions (600 or 640)
   - Only the application user should have read access
   - The directory should have restricted permissions (700)

2. **Certificate Management**
   - Keep certificates up to date
   - Rotate certificates regularly
   - Never commit certificates to version control
   - Use environment variables or secrets management for sensitive paths

3. **Certificate Types**
   - Private keys (.pem files)
   - Public certificates
   - Certificate chains
   - Intermediate certificates

## Current Certificates

- `SSL_redis-btc-omega-redis.pem`: Private key for Redis SSL connection

## Usage

The certificates are used by the Redis manager for secure connections to the Redis database. The path to the certificate is configured in:

- `redis_manager.py`
- `app.yaml` environment variables

## Maintenance

1. **Certificate Rotation**

   ```bash
   # Update certificate permissions
   chmod 600 SSL_redis-btc-omega-redis.pem
   
   # Update directory permissions
   chmod 700 .
   ```

2. **Certificate Validation**

   ```bash
   # Check certificate validity
   openssl x509 -in SSL_redis-btc-omega-redis.pem -text -noout
   ```

## Security Best Practices

1. Never commit certificates to version control
2. Use secrets management for certificate storage
3. Implement certificate rotation policies
4. Monitor certificate expiration
5. Use strong encryption algorithms
6. Keep certificates in a secure location
7. Implement proper access controls
