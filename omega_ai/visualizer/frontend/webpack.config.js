const path = require('path');

module.exports = {
    // ... other webpack config options ...

    module: {
        rules: [
            {
                test: /\.m?js/,
                resolve: {
                    fullySpecified: false
                }
            }
        ]
    },

    ignoreWarnings: [
        {
            module: /@mediapipe\/tasks-vision/
        }
    ]
}; 