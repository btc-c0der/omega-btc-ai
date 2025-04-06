# Quantum Dashboard Tools

This directory contains utility tools for managing the Quantum Dashboard and related components.

## 🧹 Clean Quantum Logs (clean_quantum_logs.sh)

The `clean_quantum_logs.sh` script helps maintain repo hygiene by cleaning up Quantum Dashboard JSON logs and report files that can quickly grow in size but aren't needed for version control.

### Usage

```bash
# Run from project root
./src/omega_bot_farm/qa/tools/clean_quantum_logs.sh
```

### What It Does

The script:

1. Identifies and counts all JSON log files and report files
2. Asks for confirmation before deleting
3. Removes:
   - All JSON logs in the tests/reports directory
   - Test run reports (test_run_*.json)
   - Quantum test reports and their HTML/XML counterparts
   - Dated report directories
   - Temporary JSON files
   - Dashboard asset JSON files

### Gitignore Integration

These files are also added to the project's `.gitignore` file with patterns like:

```
# Quantum Dashboard logs and reports
src/omega_bot_farm/qa/tests/reports/*.json
src/omega_bot_farm/qa/tests/reports/*/
src/omega_bot_farm/qa/tests/reports/quantum_test_report_*.json
src/omega_bot_farm/qa/tests/reports/test_run_*.json
src/omega_bot_farm/qa/tests/reports/*_20*.json
src/omega_bot_farm/qa/tests/reports/latest.json
src/omega_bot_farm/qa/data/*.json
src/omega_bot_farm/qa/data/quantum_*.json
src/omega_bot_farm/qa/quantum_dashboard/assets/*.json
src/omega_bot_farm/qa/tmp/quantum_*.json

# Quantum test output files
src/omega_bot_farm/qa/tests/reports/*.html
src/omega_bot_farm/qa/tests/reports/*.xml
```

## 🔄 Best Practices

1. Run the clean script before committing changes
2. Run it periodically to prevent disk space issues
3. If you need to preserve specific logs, move them to a directory not covered by the cleaning patterns

## 🔒 Security Note

Be careful when using the script in a production environment, as it will permanently delete files. Always ensure your important data is backed up before running cleanup operations.

---

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬

This toolset is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸
