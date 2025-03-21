from flask import jsonify

class ReggaeDashboardServer:
    def api_health(self):
        """Get health status endpoint."""
        if not self.redis_client:
            return jsonify({"status": "error", "message": "No Redis connection"})
        try:
            self.redis_client.ping()
            return jsonify({"status": "healthy"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    def api_redis_keys(self):
        """Get Redis keys information."""
        if not self.redis_client:
            return jsonify({"status": "error", "message": "No Redis connection", "keys": []})
        
        try:
            # Get all keys
            all_keys = self.redis_client.keys("*")
            keys_info = []
            
            # Collect information about each key
            for key in all_keys:
                key_str = key.decode("utf-8") if isinstance(key, bytes) else key
                key_type = self.redis_client.type(key).decode("utf-8")
                
                key_data = {
                    "key": key_str,
                    "type": key_type
                }
                
                # Add additional type-specific information
                if key_type == "string":
                    value = self.redis_client.get(key)
                    key_data["length"] = len(value) if value else 0
                elif key_type == "list":
                    key_data["length"] = self.redis_client.llen(key)
                elif key_type == "hash":
                    key_data["fields"] = len(self.redis_client.hkeys(key))
                elif key_type == "set":
                    key_data["members"] = self.redis_client.scard(key)
                elif key_type == "zset":
                    key_data["members"] = self.redis_client.zcard(key)
                
                keys_info.append(key_data)
            
            # Sort keys alphabetically
            keys_info.sort(key=lambda k: k.get("key", ""))
            
            return jsonify({"status": "success", "keys": keys_info})
        except Exception as e:
            self.logger.error(f"Error getting Redis keys: {e}")
            return jsonify({"status": "error", "message": str(e), "keys": []})

    @app.route("/api/trap-probability", methods=["GET"])
    def api_trap_probability(self):
        # Implementation of the new endpoint
        pass 