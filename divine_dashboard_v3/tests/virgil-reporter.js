/**
 * "VIRGIL REPORTER" — "OMEGA GRID PORTAL"
 * ======================================
 * 
 * "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST REPORTER
 * CUSTOM JEST REPORTER WITH INDUSTRIAL STYLING
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

/**
 * Custom test results processor with Virgil Abloh / OFF-WHITE™ styling
 * @param {Object} testResults - The Jest test results object
 * @returns {Object} - The processed test results
 */
module.exports = function virgilReporter(testResults) {
    // Create console styling helpers
    const styles = {
        bold: text => `\x1b[1m${text}\x1b[22m`,
        white: text => `\x1b[37m${text}\x1b[39m`,
        black: text => `\x1b[30m${text}\x1b[39m`,
        yellow: text => `\x1b[33m${text}\x1b[39m`,
        green: text => `\x1b[32m${text}\x1b[39m`,
        red: text => `\x1b[31m${text}\x1b[39m`,
        cyan: text => `\x1b[36m${text}\x1b[39m`,
        magenta: text => `\x1b[35m${text}\x1b[39m`,
        bgWhite: text => `\x1b[47m${text}\x1b[49m`,
        bgBlack: text => `\x1b[40m${text}\x1b[49m`,
        bgYellow: text => `\x1b[43m${text}\x1b[49m`
    };

    const format = {
        virgilQuote: text => styles.bold(styles.black(styles.bgWhite(`"${text}"`))),
        virgilHeader: text => styles.yellow(`"${text}"`),
        virgilSuccess: text => styles.green(`"${text}"`),
        virgilError: text => styles.red(`"${text}"`),
        virgilInfo: text => styles.cyan(`"${text}"`)
    };

    // Process results and log in Virgil style
    const numFailedTests = testResults.numFailedTests;
    const numPassedTests = testResults.numPassedTests;
    const numTotalTests = testResults.numTotalTests;

    // Header
    console.log('\n');
    console.log(styles.bold(styles.black(styles.bgYellow('                                                 '))));
    console.log(styles.bold(styles.black(styles.bgYellow('    "OMEGA GRID PORTAL" — "TEST RESULTS"         '))));
    console.log(styles.bold(styles.black(styles.bgYellow('    "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TESTS '))));
    console.log(styles.bold(styles.black(styles.bgYellow('                                                 '))));
    console.log('\n');

    // Summary
    console.log(format.virgilHeader('TEST SUMMARY'));
    console.log(format.virgilInfo(`TOTAL TESTS: ${numTotalTests}`));
    console.log(format.virgilSuccess(`PASSED: ${numPassedTests}`));
    console.log(format.virgilError(`FAILED: ${numFailedTests}`));
    console.log('\n');

    // Test suite details
    if (testResults.testResults) {
        console.log(format.virgilHeader('TEST SUITES'));

        testResults.testResults.forEach(suite => {
            const suiteStatus = suite.status === 'passed' ?
                format.virgilSuccess('PASSED') : format.virgilError('FAILED');

            console.log(`${suiteStatus} — ${format.virgilQuote(suite.name)}`);

            // Show test case results for failed suites
            if (suite.status !== 'passed') {
                suite.testResults.forEach(test => {
                    const testStatus = test.status === 'passed' ?
                        format.virgilSuccess('PASSED') : format.virgilError('FAILED');

                    console.log(`  ${testStatus} — ${format.virgilInfo(test.title)}`);

                    // Show failure messages
                    if (test.status !== 'passed' && test.failureMessages) {
                        test.failureMessages.forEach(msg => {
                            const cleanMsg = msg.replace(/\x1b\[\d+m/g, ''); // Remove ANSI color codes
                            console.log(`    ${format.virgilError('ERROR')}: ${cleanMsg}`);
                        });
                    }
                });
            }
        });
    }

    // Timing information
    console.log('\n');
    console.log(format.virgilHeader('TIMING'));
    console.log(format.virgilInfo(`START TIME: ${new Date(testResults.startTime).toLocaleTimeString()}`));
    console.log(format.virgilInfo(`END TIME: ${new Date(testResults.endTime).toLocaleTimeString()}`));
    console.log(format.virgilInfo(`TOTAL TIME: ${((testResults.endTime - testResults.startTime) / 1000).toFixed(2)}s`));

    // Footer
    console.log('\n');
    console.log(styles.bold(styles.white(styles.bgBlack('                                                   '))));
    console.log(styles.bold(styles.white(styles.bgBlack('    "c/o OMEGA GRID"   "FOR TESTING PURPOSES"      '))));
    console.log(styles.bold(styles.white(styles.bgBlack('                                                   '))));

    // Return original test results for Jest to process
    return testResults;
}; 