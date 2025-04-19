
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Repository Consolidation Guide

## Overview

This document outlines the process for consolidating multiple repository versions of the OMEGA-BTC-AI project.

The two repository locations that need to be consolidated are:
- `/Users/fsiqueira/Desktop/Code/omega_btc_ai` (referred to as "Code folder")
- `/Users/fsiqueira/Desktop/GitHub/omega-btc-ai` (referred to as "GitHub folder")

## Steps Already Completed

1. ✅ Merged version of `btc_live_feed.py` created that combines functionality from both repositories
2. ✅ Created archiving script (`scripts/archive_code_folder.sh`) to safely archive the Code folder

## Remaining Files to Check

The following files may need manual inspection to confirm they are properly synchronized:

1. Market Maker Trap Detector files:
   - mm_trap_processor.py
   - mm_trap_consumer.py
   - mm_websocket_server.py
   - trap_producer.py
   - fibonacci_detector.py
   - high_frequency_detector.py
   - grafana_reporter.py

2. Test files:
   - test_redis_trap_monitor.py
   - test_btc_live_feed.py

## Consolidation Process

Follow these steps to complete the consolidation:

1. **For each important file:**
   - Compare the versions in both repositories using: 
     ```bash
     diff -u /Users/fsiqueira/Desktop/Code/omega_btc_ai/path/to/file /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/path/to/file
     ```
   - If there are critical differences, create a merged version similar to what was done with `btc_live_feed.py`

2. **Run all tests** to ensure functionality is preserved:
   ```bash
   cd /Users/fsiqueira/Desktop/GitHub/omega-btc-ai
   python -m pytest
   ```

3. **Commit all changes** to the GitHub repository:
   ```bash
   cd /Users/fsiqueira/Desktop/GitHub/omega-btc-ai
   git add .
   git commit -m "Consolidate code from both repositories"
   git push
   ```

4. **Archive the Code folder** using the provided script:
   ```bash
   cd /Users/fsiqueira/Desktop/GitHub/omega-btc-ai
   ./scripts/archive_code_folder.sh
   ```

## Verification Checklist

Before archiving, manually verify:

- [ ] All important files from Code folder are present in GitHub folder
- [ ] All tests pass in the GitHub repository
- [ ] Any custom modifications made in the Code folder have been preserved
- [ ] Redis trap functionality works correctly in both versions
- [ ] Repository structure is clean and consistent

## After Consolidation

After consolidating:

1. Use only the GitHub repository for all future development
2. If needed, reference the archived Code folder for any missed functionality
3. Consider running both versions side by side briefly to ensure all functionality works the same

## Troubleshooting

If you encounter issues during consolidation:

1. Check the diff output to identify key differences
2. Run specific tests for the affected functionality
3. Use temporary prints and logging to debug behavior differences
4. Restore from backup if needed (created by the archive script)

## Contact

For any questions regarding this consolidation process, contact the OMEGA-BTC-AI development team.

---

*JAH BLESS THE DIVINE CODE CONSOLIDATION!* 🌿✨ 