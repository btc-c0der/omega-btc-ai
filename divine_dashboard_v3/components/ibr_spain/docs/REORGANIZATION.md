# IBR España Component Reorganization

## Overview

The IBR España Instagram Manager component files have been reorganized for better maintainability and code organization. This document outlines the changes made to the directory structure and explains how to run the various scripts in their new locations.

## Directory Structure

The IBR España component now follows this directory structure:

```
divine_dashboard_v3/
└── components/
    └── ibr_spain/
        ├── docs/                   # Documentation files
        │   ├── BUG_FIX_LOG_IBR_SPAIN.md
        │   └── REORGANIZATION.md
        ├── standalone/             # Standalone version
        │   ├── ibr_standalone.py
        │   ├── run_ibr_standalone.sh
        │   └── run_ibr_with_server.sh
        ├── tests/                  # Test files
        │   ├── test_ibr_fetching.py
        │   ├── run_ibr_tests.sh
        │   ├── IBR_SPAIN_TEST_README.md
        │   └── other test files...
        ├── micro_modules/          # Smaller feature modules
        ├── ibr_dashboard.py        # Main component implementation
        ├── __init__.py             # Package initialization
        └── README.md               # Component documentation
```

## Files Moved

The following files were relocated:

1. `divine_dashboard_v3/ibr_standalone.py` → `components/ibr_spain/standalone/ibr_standalone.py`
2. `divine_dashboard_v3/run_ibr_standalone.sh` → `components/ibr_spain/standalone/run_ibr_standalone.sh`
3. `divine_dashboard_v3/run_ibr_with_server.sh` → `components/ibr_spain/standalone/run_ibr_with_server.sh`
4. `divine_dashboard_v3/test_ibr_fetching.py` → `components/ibr_spain/tests/test_ibr_fetching.py`
5. `divine_dashboard_v3/run_ibr_tests.sh` → `components/ibr_spain/tests/run_ibr_tests.sh`
6. `divine_dashboard_v3/IBR_SPAIN_TEST_README.md` → `components/ibr_spain/tests/IBR_SPAIN_TEST_README.md`
7. `divine_dashboard_v3/BUG_FIX_LOG_IBR_SPAIN.md` → `components/ibr_spain/docs/BUG_FIX_LOG_IBR_SPAIN.md`

## Script Updates

All scripts have been updated to work with the new directory structure:

1. Path references have been updated in all scripts to maintain compatibility
2. Import statements have been fixed to reflect the new module locations
3. Virtual environment references now point to the main project venv

## Running the Scripts

### Standalone Dashboard

To run the standalone dashboard:

```bash
cd divine_dashboard_v3/components/ibr_spain/standalone
./run_ibr_standalone.sh
```

### Server Integration

To run the IBR España component integrated with the main server:

```bash
cd divine_dashboard_v3/components/ibr_spain/standalone
./run_ibr_with_server.sh
```

### Tests

To run the tests:

```bash
cd divine_dashboard_v3/components/ibr_spain/tests
./run_ibr_tests.sh
```

## Benefits of Reorganization

1. **Better Code Organization**: Related files are now grouped together
2. **Improved Maintainability**: Easier to find and update specific components
3. **Modularity**: The component is now more self-contained and can be developed independently
4. **Separation of Concerns**: Tests, documentation, and implementation code are properly separated
5. **Reusability**: Components can be more easily reused in other parts of the project

## Note on Dependencies

All scripts now reference the main project's virtual environment (`divine_dashboard_v3/venv/`) to ensure consistent dependencies across all components.

---

*Reorganization completed: April 11, 2025*
