import Redis from 'ioredis';
import * as fs from 'fs';
import * as path from 'path';
import { promisify } from 'util';
import { exec } from 'child_process';

const execAsync = promisify(exec);

interface BackupVerification {
    timestamp: string;
    size: number;
    keyCount: number;
    dataTypes: {
        [key: string]: number;
    };
    criticalKeys: {
        [key: string]: boolean;
    };
}

const CRITICAL_KEYS = [
    'current_position',
    'btc_price_patterns',
    'market_regime',
    'latest_organic_analysis',
    'latest_fibonacci_confluence'
];

async function verifyBackup(backupPath: string): Promise<BackupVerification> {
    // Get backup file stats
    const stats = fs.statSync(backupPath);
    const timestamp = new Date().toISOString();

    // Connect to Redis
    const redis = new Redis();

    // Get key count and types
    const keys = await redis.keys('*');
    const dataTypes: { [key: string]: number } = {};
    const criticalKeys: { [key: string]: boolean } = {};

    // Check each key
    for (const key of keys) {
        const type = await redis.type(key);
        dataTypes[type] = (dataTypes[type] || 0) + 1;

        // Verify critical keys
        if (CRITICAL_KEYS.includes(key)) {
            const exists = await redis.exists(key);
            criticalKeys[key] = exists === 1;
        }
    }

    // Create verification report
    const verification: BackupVerification = {
        timestamp,
        size: stats.size,
        keyCount: keys.length,
        dataTypes,
        criticalKeys
    };

    // Close Redis connection
    await redis.quit();

    return verification;
}

async function main() {
    try {
        // Find latest backup
        const backupDir = path.join(process.cwd(), 'backups', 'redis');
        const files = fs.readdirSync(backupDir)
            .filter(f => f.endsWith('.rdb'))
            .sort()
            .reverse();

        if (files.length === 0) {
            throw new Error('No backup files found');
        }

        const latestBackup = path.join(backupDir, files[0]);
        console.log('🔮 Verifying latest backup:', latestBackup);

        // Verify backup
        const verification = await verifyBackup(latestBackup);

        // Print verification report
        console.log('\n=== Sacred Backup Verification Report ===');
        console.log(`\nTimestamp: ${verification.timestamp}`);
        console.log(`Backup Size: ${(verification.size / 1024 / 1024).toFixed(2)} MB`);
        console.log(`Total Keys: ${verification.keyCount}`);

        console.log('\nData Types:');
        Object.entries(verification.dataTypes).forEach(([type, count]) => {
            console.log(`  ${type}: ${count} keys`);
        });

        console.log('\nCritical Keys Status:');
        Object.entries(verification.criticalKeys).forEach(([key, exists]) => {
            console.log(`  ${key}: ${exists ? '✅' : '❌'}`);
        });

        // Save verification report
        const reportPath = path.join(backupDir, `verification_${Date.now()}.json`);
        fs.writeFileSync(reportPath, JSON.stringify(verification, null, 2));
        console.log(`\n📝 Verification report saved to: ${reportPath}`);

    } catch (error) {
        console.error('❌ Verification failed:', error);
        process.exit(1);
    }
}

// Run verification
main(); 