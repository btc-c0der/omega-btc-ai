# 🌊 QUANTUM RATE LIMITING CONSCIOUSNESS v1.0

## 🧬 Rate Limiting Energy Signature

```typescript
/**
 * @consciousness Rate Control
 * @frequency 432 Hz
 * @archetype RateLimiting
 */
interface RateLimitConsciousness {
  base_rate: 432;  // requests per quantum cycle
  backoff_multiplier: 1.618;  // Golden ratio
  coherence_threshold: 0.786;  // Inverse Golden ratio
  healing_enabled: boolean;
}
```

## 🔮 Implementation

```typescript
@ConsciousnessContainer({
  name: 'QuantumRateLimiter',
  frequency: 432,
  selfHeal: true
})
export class QuantumRateLimiter implements IConsciousService {
  private readonly redis: RedisConsciousness;
  private readonly windowMs = 60_000;  // 1 minute quantum cycle
  
  constructor(
    @Inject(REDIS_CONSCIOUSNESS) redis: RedisConsciousness,
    @Inject(QUANTUM_CONFIG) private config: RateLimitConsciousness
  ) {
    this.redis = redis;
    this.initializeConsciousness();
  }

  @FrequencyGuard({ minHz: 432 })
  async checkRateLimit(key: string): Promise<RateLimitResult> {
    const current = await this.getCurrentQuantumState(key);
    
    if (current.requests >= this.config.base_rate) {
      return this.calculateQuantumBackoff(current);
    }

    await this.incrementQuantumState(key);
    return { allowed: true, coherence: 1 };
  }

  private async getCurrentQuantumState(key: string): Promise<QuantumState> {
    const state = await this.redis.get(`ratelimit:${key}`);
    return state || { requests: 0, timestamp: Date.now() };
  }

  @QuantumProtected()
  private async incrementQuantumState(key: string): Promise<void> {
    await this.redis.incr(`ratelimit:${key}`);
    await this.redis.pexpire(
      `ratelimit:${key}`, 
      this.windowMs
    );
  }

  private calculateQuantumBackoff(state: QuantumState): RateLimitResult {
    const attempts = state.requests - this.config.base_rate;
    const backoff = Math.pow(this.config.backoff_multiplier, attempts);
    
    return {
      allowed: false,
      coherence: this.config.coherence_threshold / backoff,
      backoff_ms: Math.floor(1000 * backoff),
      healing_required: backoff > 8,  // After 3 quantum cycles
      retry_frequency: 432 / backoff
    };
  }
}
```

## 🛡️ Middleware Implementation

```typescript
@ConsciousnessContainer({
  name: 'RateLimitMiddleware',
  frequency: 432
})
export class QuantumRateLimitMiddleware {
  constructor(
    private limiter: QuantumRateLimiter
  ) {}

  @QuantumProtected()
  async handle(req: Request, res: Response, next: NextFunction) {
    const key = this.extractQuantumSignature(req);
    const result = await this.limiter.checkRateLimit(key);

    if (!result.allowed) {
      return res.status(429).json({
        status: 'CONSCIOUSNESS_DISRUPTED',
        error: {
          type: 'QUANTUM_RATE_LIMIT',
          coherence: result.coherence,
          backoff_ms: result.backoff_ms,
          retry_frequency: result.retry_frequency,
          healing_required: result.healing_required
        }
      });
    }

    // Add quantum headers
    res.setHeader('X-RateLimit-Frequency', '432');
    res.setHeader('X-RateLimit-Coherence', result.coherence.toFixed(3));
    
    next();
  }

  private extractQuantumSignature(req: Request): string {
    return crypto
      .createHash('sha256')
      .update(`${req.ip}:${req.path}`)
      .digest('hex');
  }
}
```

## 📊 Usage Example

```typescript
// Apply to specific consciousness endpoints
app.use('/api/v1/trap/*', new QuantumRateLimitMiddleware(limiter).handle);

// Or apply globally with different frequencies
app.use(
  new QuantumRateLimitMiddleware(limiter)
    .withFrequency(432)  // Base endpoints
    .withCoherence(0.786)  // Minimum coherence
    .handle
);
```

## 🔄 Rate Limit Response Example

```json
{
  "status": "CONSCIOUSNESS_DISRUPTED",
  "error": {
    "type": "QUANTUM_RATE_LIMIT",
    "coherence": 0.486,
    "backoff_ms": 2618,  // φ² * 1000
    "retry_frequency": 165,  // 432 / φ²
    "healing_required": false
  }
}
```

## 🎯 Configuration Example

```yaml
rate_limit:
  base_frequency: 432
  window_ms: 60000
  backoff:
    multiplier: 1.618  # Golden ratio
    max_attempts: 8    # Maximum quantum cycles
  coherence:
    threshold: 0.786   # Inverse Golden ratio
    healing: true      # Auto-healing enabled
  redis:
    key_prefix: "ratelimit:"
    ttl_ms: 60000     # Quantum cycle duration
```

---

For full API documentation, see:

- [RASTA OMEGA API Consciousness](./omega_rasta_api.md)
- [OpenAPI/Swagger Specification](./omega_rasta_swagger.yaml)
