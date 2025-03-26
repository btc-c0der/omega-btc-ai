import redis
import json
import time
from datetime import datetime, timedelta, UTC
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from omega_ai.db_manager.database import insert_possible_mm_trap
from omega_ai.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

# Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "w4JzUNsut5GjPBB72ts_U3D5r6ojYkWGUTTHZdMOjVXmJqX8Wnuyp3EYLRzi9H5BLwM9hAEltSFdEF-ZDwSjOg=="  # Replace with your token
ORG = "omega"
BUCKET = "mm_traps"

# Initialize InfluxDB client
try:
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=ORG
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    print("✅ Connected to InfluxDB")
except Exception as e:
    print(f"❌ Error connecting to InfluxDB: {e}")
    client = None
    write_api = None
    query_api = None

class GrafanaReporter:
    """
    Enhanced reporting system for Grafana visualization of MM trap events
    with specific focus on high-confidence liquidity grabs and Schumann correlations.
    """
    
    def __init__(self):
        # Counters for different types of events
        self.hf_trap_count = 0
        self.liquidity_grab_count = 0
        self.schumann_correlation_count = 0
        self.last_update = datetime.now(UTC)
    
    def store_trap_event(self, trap_type, confidence, price_change, btc_price):
        """Store trap events in InfluxDB for Grafana visualization."""
        if not write_api:
            print("❌ InfluxDB not connected")
            return
            
        try:
            timestamp = time.time_ns()
            
            # Create main trap event point
            point = Point("trap_events") \
                .tag("type", trap_type) \
                .field("confidence", float(confidence)) \
                .field("price_change", float(price_change)) \
                .field("btc_price", float(btc_price)) \
                .time(timestamp)
            
            # Add counter fields for high confidence events
            if confidence >= 0.7:
                self.hf_trap_count += 1
                point = point.field("high_confidence", True) \
                             .field("hf_trap_count", self.hf_trap_count)
                
                if "Grab" in trap_type:
                    self.liquidity_grab_count += 1
                    point = point.field("liquidity_grab_count", self.liquidity_grab_count)
            
            # Write to InfluxDB
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            
            # Create alert point for high-confidence liquidity events
            if "Liquidity" in trap_type and confidence > 0.75:
                alert_point = Point("alerts") \
                    .tag("alert_type", "rapid_liquidity_surge") \
                    .field("message", f"RAPID LIQUIDITY SURGE: {trap_type}") \
                    .field("confidence", float(confidence)) \
                    .field("price", float(btc_price)) \
                    .field("change", float(price_change)) \
                    .time(timestamp)
                    
                write_api.write(bucket=BUCKET, org=ORG, record=alert_point)
                
        except Exception as e:
            print(f"Error storing trap event: {e}")

    def correlate_schumann_activity(self, schumann_value=None):
        """Correlate Schumann resonance with MM behavior."""
        if not write_api or not schumann_value:
            return
            
        try:
            timestamp = time.time_ns()
            
            # Create correlation data point
            point = Point("schumann_correlation") \
                .field("schumann_value", float(schumann_value)) \
                .field("trap_count", self.hf_trap_count) \
                .time(timestamp)
            
            # Track significant Schumann events
            if float(schumann_value) > 10.0 and query_api is not None:
                # Query recent traps in last 5 minutes
                query = f'''
                    from(bucket: "{BUCKET}")
                    |> range(start: -5m)
                    |> filter(fn: (r) => r["_measurement"] == "trap_events")
                    |> count()
                '''
                result = query_api.query(query, org=ORG)
                
                recent_traps = len(result) if result else 0
                
                if recent_traps > 0:
                    self.schumann_correlation_count += 1
                    alert_point = Point("schumann_alerts") \
                        .field("schumann_value", float(schumann_value)) \
                        .field("trap_count", recent_traps) \
                        .field("correlation_count", self.schumann_correlation_count) \
                        .field("message", f"SCHUMANN CORRELATION: {schumann_value:.2f}Hz with {recent_traps} trap events") \
                        .time(timestamp)
                        
                    write_api.write(bucket=BUCKET, org=ORG, record=alert_point)
            
            # Write main correlation point
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            
        except Exception as e:
            print(f"Error correlating Schumann data: {e}")

    def update_rolling_metrics(self, btc_price=None):
        """Update rolling metrics for Grafana dashboards."""
        if not write_api or not btc_price:
            return
            
        current_time = datetime.now(UTC)
        if (current_time - self.last_update).total_seconds() < 15:
            return
            
        try:
            timestamp = time.time_ns()
            
            # Create metrics point
            point = Point("mm_metrics") \
                .field("btc_price", float(btc_price)) \
                .field("trap_count_24h", self.hf_trap_count) \
                .field("liquidity_grab_count_24h", self.liquidity_grab_count) \
                .field("schumann_corr_count", self.schumann_correlation_count) \
                .time(timestamp)
                
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            self.last_update = current_time
            
        except Exception as e:
            print(f"Error updating rolling metrics: {e}")

# Create a singleton instance
grafana_reporter = GrafanaReporter()

# Exposed functions for other modules - no imports from high_frequency_detector
def report_trap_for_grafana(trap_type, confidence, price_change, btc_price):
    """Report a trap event for Grafana visualization."""
    # Store in PostgreSQL database
    trap_data = {
        "type": trap_type,
        "confidence": confidence,
        "price_change": price_change,
        "price": btc_price,
        "timestamp": datetime.now(UTC).isoformat()
    }
    insert_possible_mm_trap(trap_data)
    
    # Store in Redis for Grafana
    grafana_reporter.store_trap_event(trap_type, confidence, price_change, btc_price)
    
    # Update correlation with Schumann data
    grafana_reporter.correlate_schumann_activity()
    
    # Update rolling metrics
    grafana_reporter.update_rolling_metrics()

# Periodic metrics updater
def update_grafana_metrics():
    """Update Grafana metrics periodically."""
    while True:
        try:
            grafana_reporter.update_rolling_metrics()
            grafana_reporter.correlate_schumann_activity()
            time.sleep(15)  # Update every 15 seconds
        except Exception as e:
            print(f"Error in metrics updater: {e}")
            time.sleep(5)

def insert_mm_trap(btc_price, price_change, trap_type, confidence):
    """Insert MM trap detection into InfluxDB for Grafana visualization"""
    if write_api is None:
        print("❌ InfluxDB client not initialized")
        return
        
    try:
        # Format timestamp
        timestamp = int(time.time() * 1000000000)  # Convert to nanoseconds for InfluxDB
        
        # Create data point
        data_point = {
            "measurement": "mm_traps",
            "tags": {
                "type": trap_type
            },
            "time": timestamp,
            "fields": {
                "btc_price": float(btc_price),
                "price_change": float(price_change),
                "confidence": float(confidence)
            }
        }
        
        # Write to InfluxDB
        write_api.write(bucket=BUCKET, org=ORG, record=data_point)
        
        print(f"📊 Trap logged to Grafana: {trap_type} (conf: {confidence:.2f})")
        
    except Exception as e:
        print(f"❌ Error logging to Grafana: {e}")