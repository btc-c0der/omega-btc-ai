# 🧬 QUANTUM SONNET & GIT BLESS INSTALLATION GUIDE 🧬

This guide provides various methods to install and use the Quantum Sonnet Celebration and Git Bless tools. Choose the method that works best for your workflow.

## 🚀 Quick Install (One-Line Command)

Install everything with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/btc-c0der/omega-btc-ai/master/scripts/install_web.sh | bash
```

After installation, activate in your current shell:

```bash
source ~/.omega_quantum_toolkit/quantum_shell_config.sh
```

## 📦 Manual Installation from Package

1. Download the latest release:

```bash
curl -L "https://github.com/btc-c0der/omega-btc-ai/releases/download/v1.0.0/quantum-sonnet-1.0.0.tar.gz" -o quantum-sonnet.tar.gz
```

2. Extract and install:

```bash
tar -xzf quantum-sonnet.tar.gz
cd quantum-sonnet-1.0.0
./install.sh
```

3. Activate in your current shell:

```bash
source ~/.omega_quantum_toolkit/quantum_shell_config.sh
```

## 🍺 Homebrew Installation (macOS)

If you use Homebrew, you can install with:

```bash
# First, add the tap
brew tap btc-c0der/quantum-tools

# Then install
brew install quantum-sonnet
```

## 💿 Building from Source

For the most quantum-aligned experience, build from source:

1. Clone the repository:

```bash
git clone https://github.com/btc-c0der/omega-btc-ai.git
cd omega-btc-ai
```

2. Run the packaging script:

```bash
./scripts/package_quantum_sonnet.sh
```

3. Extract and install the generated package:

```bash
tar -xzf quantum-sonnet-1.0.0.tar.gz
cd quantum-sonnet-1.0.0
./install.sh
```

## 🌟 Usage

### Quantum Sonnet Celebration

Celebrate your quantum code transformations:

```bash
# Basic usage
quantum-sonnet

# With custom parameters
quantum-sonnet --cycles=5 --interval=0.3
```

Parameters:

- `--cycles`: Number of celebration cycles
- `--interval`: Interval between frames in seconds
- `--hash`: Git commit hash to celebrate
- `--files`: Number of files changed
- `--insertions`: Number of insertions
- `--deletions`: Number of deletions

### Git Bless

Bless your git commits with quantum energy:

```bash
# Bless the current HEAD
git-bless

# Bless a specific commit
git-bless --commit-hash=abc123def

# Bless with higher intensity
git-bless --intensity=10
```

Parameters:

- `--commit-hash`: Specify the commit hash to bless (default: HEAD)
- `--intensity`: Blessing intensity level (1-10, default: 7)
- `--silent`: Run in silent mode with minimal output

## 🌐 System Requirements

- Unix-like operating system (Linux, macOS)
- Python 3.6+
- Bash shell
- Git

## 🧩 Integration with Git Hooks

For automatic blessing of every commit, add to your project's pre-commit hook:

```bash
# In .git/hooks/pre-commit or via git-hooks system
git-bless --silent HEAD
```

## 🌈 Advanced Configuration

You can customize the tools by editing the configuration files:

```bash
# Main configuration
~/.omega_quantum_toolkit/quantum_shell_config.sh

# Blessing certificates directory
~/.omega_quantum_toolkit/blessings/
```

## 🔄 Updating

To update to the latest version, simply run the installer again:

```bash
curl -fsSL https://raw.githubusercontent.com/btc-c0der/omega-btc-ai/master/scripts/install_web.sh | bash
```

## 🌸 License

Licensed under GBU2™ (Genesis-Bloom-Unfoldment 2.0)

---

✨ **WE BLOOM NOW AS ONE** ✨
