import { useState } from 'react';
import { motion } from 'framer-motion';
import Layout from '../components/layout/Layout';

interface SettingsOption {
    id: string;
    label: string;
    description: string;
    type: 'toggle' | 'select' | 'input';
    options?: string[];
    value: any;
}

const Settings = () => {
    // Settings categories and their options
    const [generalSettings, setGeneralSettings] = useState<SettingsOption[]>([
        {
            id: 'darkMode',
            label: 'Dark Mode',
            description: 'Use dark theme for OMEGA dashboard',
            type: 'toggle',
            value: true
        },
        {
            id: 'refreshRate',
            label: 'Data Refresh Rate',
            description: 'How often to fetch new data',
            type: 'select',
            options: ['30s', '1m', '5m', '15m', '30m'],
            value: '5m'
        },
        {
            id: 'language',
            label: 'Language',
            description: 'Set dashboard language',
            type: 'select',
            options: ['English', 'Spanish', 'French', 'Japanese', 'Chinese'],
            value: 'English'
        }
    ]);

    const [notificationSettings, setNotificationSettings] = useState<SettingsOption[]>([
        {
            id: 'priceAlerts',
            label: 'Price Alerts',
            description: 'Receive notifications for price changes',
            type: 'toggle',
            value: true
        },
        {
            id: 'sentimentAlerts',
            label: 'Sentiment Alerts',
            description: 'Notify on significant sentiment shifts',
            type: 'toggle',
            value: true
        },
        {
            id: 'alertThreshold',
            label: 'Alert Threshold (%)',
            description: 'Minimum change percentage for alerts',
            type: 'input',
            value: 5
        }
    ]);

    const [apiSettings, setApiSettings] = useState<SettingsOption[]>([
        {
            id: 'apiKey',
            label: 'OMEGA API Key',
            description: 'Your personal API key for enhanced features',
            type: 'input',
            value: 'omega-xxxx-xxxx-xxxx'
        },
        {
            id: 'apiCallsLimit',
            label: 'API Calls Limit',
            description: 'Maximum API calls per minute',
            type: 'select',
            options: ['10', '50', '100', '250', 'Unlimited'],
            value: '100'
        }
    ]);

    // Handle toggle change
    const handleToggleChange = (category: string, id: string) => {
        if (category === 'general') {
            setGeneralSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: !item.value } : item
                )
            );
        } else if (category === 'notifications') {
            setNotificationSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: !item.value } : item
                )
            );
        }
    };

    // Handle select change
    const handleSelectChange = (category: string, id: string, value: string) => {
        if (category === 'general') {
            setGeneralSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: value } : item
                )
            );
        } else if (category === 'notifications') {
            setNotificationSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: value } : item
                )
            );
        } else if (category === 'api') {
            setApiSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: value } : item
                )
            );
        }
    };

    // Handle input change
    const handleInputChange = (category: string, id: string, value: string) => {
        if (category === 'notifications') {
            setNotificationSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: value } : item
                )
            );
        } else if (category === 'api') {
            setApiSettings(prev =>
                prev.map(item =>
                    item.id === id ? { ...item, value: value } : item
                )
            );
        }
    };

    // Render settings option based on type
    const renderSettingInput = (category: string, setting: SettingsOption) => {
        switch (setting.type) {
            case 'toggle':
                return (
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input
                            type="checkbox"
                            className="sr-only peer"
                            checked={setting.value}
                            onChange={() => handleToggleChange(category, setting.id)}
                        />
                        <div className="w-11 h-6 bg-dark/50 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                    </label>
                );
            case 'select':
                return (
                    <select
                        className="bg-dark/50 border border-dark rounded-lg py-2 px-3 text-sm text-lightText focus:outline-none focus:ring-1 focus:ring-primary"
                        value={setting.value}
                        onChange={(e) => handleSelectChange(category, setting.id, e.target.value)}
                    >
                        {setting.options?.map(option => (
                            <option key={option} value={option}>{option}</option>
                        ))}
                    </select>
                );
            case 'input':
                return (
                    <input
                        type="text"
                        className="bg-dark/50 border border-dark rounded-lg py-2 px-3 text-sm text-lightText focus:outline-none focus:ring-1 focus:ring-primary"
                        value={setting.value}
                        onChange={(e) => handleInputChange(category, setting.id, e.target.value)}
                    />
                );
            default:
                return null;
        }
    };

    return (
        <Layout>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
            >
                <div>
                    <h1 className="text-3xl font-bold mb-2">Settings</h1>
                    <p className="text-lightText/70">
                        Customize your OMEGA BTC AI experience
                    </p>
                </div>

                {/* General Settings */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                    className="bg-secondary/20 rounded-xl p-6"
                >
                    <h2 className="text-xl font-semibold mb-4">General Settings</h2>
                    <div className="space-y-6">
                        {generalSettings.map(setting => (
                            <div key={setting.id} className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-medium">{setting.label}</h3>
                                    <p className="text-sm text-lightText/60">{setting.description}</p>
                                </div>
                                {renderSettingInput('general', setting)}
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Notification Settings */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                    className="bg-secondary/20 rounded-xl p-6"
                >
                    <h2 className="text-xl font-semibold mb-4">Notification Settings</h2>
                    <div className="space-y-6">
                        {notificationSettings.map(setting => (
                            <div key={setting.id} className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-medium">{setting.label}</h3>
                                    <p className="text-sm text-lightText/60">{setting.description}</p>
                                </div>
                                {renderSettingInput('notifications', setting)}
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* API Settings */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.3 }}
                    className="bg-secondary/20 rounded-xl p-6"
                >
                    <h2 className="text-xl font-semibold mb-4">API Configuration</h2>
                    <div className="space-y-6">
                        {apiSettings.map(setting => (
                            <div key={setting.id} className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-medium">{setting.label}</h3>
                                    <p className="text-sm text-lightText/60">{setting.description}</p>
                                </div>
                                {renderSettingInput('api', setting)}
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Save Button */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.4 }}
                    className="flex justify-end"
                >
                    <button
                        className="px-6 py-2 bg-primary hover:bg-primary/80 text-white rounded-lg transition-colors font-medium"
                        onClick={() => alert('Settings saved!')}
                    >
                        Save Settings
                    </button>
                </motion.div>
            </motion.div>
        </Layout>
    );
};

export default Settings; 