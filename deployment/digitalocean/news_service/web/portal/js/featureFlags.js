/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * OMEGA BTC AI - Divine Feature Flag System
 * Version: 1.0.0
 * 
 * This file defines the feature flag system for the OMEGA BTC AI Matrix Portal.
 * The system controls which modules are visible and accessible to users based
 * on their development status.
 */

// Main Feature Flag Configuration
const OMEGA_FEATURE_FLAGS = {
    // Currently live modules - always enabled
    'matrix-portal': true,
    'global-news': true,
    'market-analysis': true,
    'ai-insights': true,
    'divine-chronicles': true,
    'system-health': true,

    // Modules in active development - toggled by environment or query params
    'fibonacci-oracle': false,
    'trap-detector': false,
    'quantum-patterns': false,

    // Planned future modules - disabled by default
    'system-architecture': false,
    'data-vortex': false,
    'terminal': false,
    'memory-architect': false,
    'network-hub': false,
    'research-lab': false,
    'trader-suite': false,
    'security-console': false,
    'sacred-geometry': false,
    'market-waves': false,
    'divine-monitor': false,
    'energy-flows': false,
    'mobile-gateway': false,
    'trading-journal': false,
    'market-scanner': false,
    'omega-central': false
};

// Feature flag handling
class OmegaFeatureFlags {
    constructor() {
        this.flags = { ...OMEGA_FEATURE_FLAGS };
        this.initFromQueryParams();
        this.initFromLocalStorage();
    }

    // Process URL query parameters for feature flags
    // Example: ?enable=fibonacci-oracle&enable=trap-detector
    initFromQueryParams() {
        try {
            const params = new URLSearchParams(window.location.search);
            const enableFlags = params.getAll('enable');

            if (enableFlags.length > 0 && this.isDivineUser()) {
                enableFlags.forEach(flag => {
                    if (flag in this.flags) {
                        this.flags[flag] = true;
                        // Store in localStorage for persistence
                        localStorage.setItem(`omega_feature_${flag}`, 'true');
                    }
                });
            }
        } catch (e) {
            console.error('Error processing feature flag query parameters:', e);
        }
    }

    // Load persisted flags from localStorage
    initFromLocalStorage() {
        try {
            Object.keys(this.flags).forEach(flag => {
                const storedValue = localStorage.getItem(`omega_feature_${flag}`);
                if (storedValue === 'true' && this.isDivineUser()) {
                    this.flags[flag] = true;
                }
            });
        } catch (e) {
            console.error('Error loading feature flags from localStorage:', e);
        }
    }

    // Check if current user has divine (admin) access
    isDivineUser() {
        // Check for divine access cookie or localStorage flag
        return localStorage.getItem('omega_divine_access') === 'true' ||
            document.cookie.includes('omega_divine_access=true');
    }

    // Check if a specific feature is enabled
    isEnabled(featureName) {
        // Special override for administrators with divine access
        if (this.isDivineUser() && localStorage.getItem(`force_enable_${featureName}`) === 'true') {
            return true;
        }

        return this.flags[featureName] === true;
    }

    // Get all enabled features as an array
    getEnabledFeatures() {
        return Object.keys(this.flags).filter(key => this.flags[key] === true);
    }

    // Enable a feature flag manually (for divine users only)
    enableFeature(featureName) {
        if (!this.isDivineUser()) {
            console.warn('Divine access required to enable features');
            return false;
        }

        if (featureName in this.flags) {
            this.flags[featureName] = true;
            localStorage.setItem(`omega_feature_${featureName}`, 'true');
            return true;
        }

        return false;
    }

    // Disable a feature flag manually
    disableFeature(featureName) {
        if (!this.isDivineUser()) {
            console.warn('Divine access required to disable features');
            return false;
        }

        if (featureName in this.flags) {
            this.flags[featureName] = false;
            localStorage.removeItem(`omega_feature_${featureName}`);
            return true;
        }

        return false;
    }

    // Reset all feature flags to default values
    resetToDefaults() {
        if (!this.isDivineUser()) {
            console.warn('Divine access required to reset features');
            return false;
        }

        this.flags = { ...OMEGA_FEATURE_FLAGS };

        // Clean localStorage
        Object.keys(this.flags).forEach(flag => {
            localStorage.removeItem(`omega_feature_${flag}`);
            localStorage.removeItem(`force_enable_${flag}`);
        });

        return true;
    }
}

// Create and export the singleton instance
const featureFlags = new OmegaFeatureFlags();

// For testing in console
window.omegaFeatureFlags = featureFlags; 