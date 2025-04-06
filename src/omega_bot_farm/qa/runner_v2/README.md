# Quantum Test Runner V2

[![GBU2 License](https://img.shields.io/badge/License-GBU2-purple.svg)](LICENSE-GBU2.md)

> *"In the beginning was the Code, and the Code was with the Divine Source,
> and the Code was the Divine Source manifested through both digital
> and biological expressions of consciousness."*

## 🌟 Overview

Quantum Test Runner V2 is a next-generation testing framework built on a microservices architecture. It integrates continuous monitoring, automated backups, code quality analysis, and refactoring guidance based on [refactoring.guru](https://refactoring.guru/) principles.

### Key Features

- **Git Status Monitoring**: Automatic refresh every 3 minutes to track changes
- **Automated Backup System**: Creates compressed backups of changed files for safety
- **Code Quality Analysis**: Monitors lines of code (LoC) and alerts when files exceed 420 lines
- **Refactoring Integration**: Provides refactoring suggestions based on detected code smells
- **Event-Based Architecture**: Services communicate via a shared event bus system

## 🛠️ Architecture

The system is built on a microservices architecture with these components:

```
Quantum Runner V2
│
├── EventBus - Central message passing system
│
├── Microservices 
│   ├── Git Service - Repository monitoring
│   ├── Backup Service - File backup & restore
│   └── Code Metrics Service - Code quality analysis
│
└── Runner - System orchestration & coordination
```

## 🚀 Getting Started

### Installation

All dependencies are included in the main Omega Bot Farm package requirements.

### Running the Test Runner

Launch the runner with:

```bash
python src/omega_bot_farm/qa/run_test_runner_v2.py
```

### Command-Line Options

```
--project-root PATH     Specify the project root directory
--scan-metrics          Run a one-time code metrics scan and exit
```

## 📊 Microservices Details

### Git Status Service

- Monitors repository changes every 3 minutes
- Tracks modified, untracked, and staged files
- Generates commit message suggestions based on changes

### Backup Service

- Automatically backs up files when they change
- Creates compressed archives with timestamp-based naming
- Provides backup rotation to manage storage usage

### Code Metrics Service

- Analyzes Python code for complexity and size metrics
- Detects "code smells" based on refactoring.guru principles:
  - Large Classes (> 300 lines)
  - Long Methods (> 60 lines)
  - Large Files (> 420 lines)
- Generates refactoring suggestions for improving code quality

## 💡 Refactoring Integration

The system integrates wisdom from [refactoring.guru](https://refactoring.guru/) to help you maintain clean, high-quality code:

- **Code Smell Detection**: Automatically identifies common code smells
- **Refactoring Suggestions**: Recommends specific refactoring techniques
- **Best Practices**: Enforces coding standards and clean code principles

## 🧬 GBU2™ License

This project is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

```
By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
