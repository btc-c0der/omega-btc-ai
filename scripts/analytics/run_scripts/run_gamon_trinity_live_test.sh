#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


# GAMON Trinity Module Test Script
# ================================

echo "Testing module imports..."

python3 -c "
try:
    print('Importing modules...')
    from gamon_trinity_matrix import GAMONTrinityMatrix
    print('✅ Imported GAMONTrinityMatrix')
    
    from variational_inference_btc_cycle import VariationalInferenceBTCCycle
    print('✅ Imported VariationalInferenceBTCCycle')
    
    from hmm_btc_state_mapper import HMMBTCStateMapper, load_btc_data
    print('✅ Imported HMMBTCStateMapper')
    
    from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
    print('✅ Imported PowerMethodBTCEigenwaves')
    
    from omega_ai.utils.redis_manager import RedisManager
    print('✅ Imported RedisManager')
    
    print('\\nAll imports successful!')
except ImportError as e:
    print(f'❌ Import error: {e}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo "Testing Redis connection..."

python3 -c "
import redis
import os

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.ping():
        print('✅ Redis connection successful')
    else:
        print('❌ Redis connection failed')
except Exception as e:
    print(f'❌ Redis error: {e}')
"

echo "Testing complete" 