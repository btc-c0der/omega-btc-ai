import Redis from 'ioredis';
import * as fs from 'fs';

interface RemovalStats {
    removedKeys: string[];
    errorKeys: string[];
    totalRemoved: number;
}

const SIMULATION_PATTERNS = [
    'sim_*',                    // Simulation prefixed keys
    'test:*',                   // Test data keys
    'mock_*',                   // Mock data keys
    'fake_*',                   // Fake data keys
];

const SIMULATION_EXACT_KEYS = [
    'sim_timestamp',
    'test:btc:history',
    'mock_position_data',
    'fake_market_data'
];

async function removeSimulationData(): Promise<RemovalStats> {
    const redis = new Redis();
    const stats: RemovalStats = {
        removedKeys: [],
        errorKeys: [],
        totalRemoved: 0
    };

    try {
        // 1. First backup the keys we're about to remove
        console.log('🔮 Creating backup of simulation keys...');
        const timestamp = Date.now();

        // Get all simulation keys
        let simulationKeys: string[] = [];
        for (const pattern of SIMULATION_PATTERNS) {
            const keys = await redis.keys(pattern);
            simulationKeys = [...simulationKeys, ...keys];
        }
        simulationKeys = [...simulationKeys, ...SIMULATION_EXACT_KEYS];

        // Backup key data
        const backupData: { [key: string]: any } = {};
        for (const key of simulationKeys) {
            const type = await redis.type(key);
            switch (type) {
                case 'string':
                    backupData[key] = await redis.get(key);
                    break;
                case 'hash':
                    backupData[key] = await redis.hgetall(key);
                    break;
                case 'set':
                    backupData[key] = await redis.smembers(key);
                    break;
                case 'zset':
                    backupData[key] = await redis.zrange(key, 0, -1, 'WITHSCORES');
                    break;
                case 'list':
                    backupData[key] = await redis.lrange(key, 0, -1);
                    break;
            }
        }

        // Save backup
        const backupPath = `backups/redis/simulation_data_${timestamp}.json`;
        fs.writeFileSync(backupPath, JSON.stringify(backupData, null, 2));
        console.log(`📝 Simulation data backed up to: ${backupPath}`);

        // 2. Remove simulation keys
        console.log('\n🧹 Removing simulation data...');

        for (const key of simulationKeys) {
            try {
                await redis.del(key);
                stats.removedKeys.push(key);
                stats.totalRemoved++;
                console.log(`✅ Removed: ${key}`);
            } catch (error) {
                stats.errorKeys.push(key);
                console.error(`❌ Error removing ${key}:`, error);
            }
        }

        // 3. Print summary
        console.log('\n=== Simulation Data Removal Summary ===');
        console.log(`Total keys removed: ${stats.totalRemoved}`);
        console.log(`Failed removals: ${stats.errorKeys.length}`);

        if (stats.errorKeys.length > 0) {
            console.log('\nFailed keys:');
            stats.errorKeys.forEach(key => console.log(`  - ${key}`));
        }

    } catch (error) {
        console.error('❌ Error during simulation data removal:', error);
    } finally {
        await redis.quit();
    }

    return stats;
}

// Run removal process
removeSimulationData().then(() => {
    console.log('\n✨ Simulation data removal complete');
}).catch(error => {
    console.error('❌ Fatal error:', error);
    process.exit(1);
}); 