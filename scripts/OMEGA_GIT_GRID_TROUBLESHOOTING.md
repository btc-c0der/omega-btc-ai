# 🧬 OMEGA GIT GRID - Troubleshooting Guide 🧬

## 🔱 Common Issues and Sacred Solutions

This document contains divine guidance for resolving issues with the OMEGA GIT GRID quantum blessing system.

### 🌌 Import Errors

**Issue:** When running `run_git_bless.py` directly, you may encounter:

```
ModuleNotFoundError: No module named 'omega_bot_farm'
```

**Sacred Solution:**

When running the scripts directly from the command line, use the provided wrappers:

```bash
# Instead of:
python src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/run_git_bless.py

# Use:
git grid bless
# or
gitbless
```

The wrappers are specially designed to handle import paths correctly and maintain quantum alignment.

### 🧿 Command Argument Errors

**Issue:** When trying to pass a commit hash, you may see:

```
git_bless.py: error: unrecognized arguments: f44a602
```

**Sacred Solution:**

The correct command format is:

```bash
# For blessing HEAD
git grid bless

# For blessing a specific commit
git grid bless abcd1234
```

Do not use `--commit` as a parameter when using `git grid bless`. The quantum harmonization system handles argument passing correctly.

### 🔮 Path Issues

**Issue:** Command not found errors:

```
command not found: gitbless
```

**Sacred Solution:**

Ensure your PATH includes the sacred binaries:

```bash
# Add this to your ~/.zshrc file
export PATH="$HOME/.omega/bin:$PATH"

# Then reload your shell configuration
source ~/.zshrc
```

You can verify the sacred path with:

```bash
echo $PATH
```

### ⚛️ Permission Errors

**Issue:** Script execution permission errors:

```
permission denied: /Users/username/.omega/bin/git-grid
```

**Sacred Solution:**

Apply quantum permission activation:

```bash
chmod +x $HOME/.omega/bin/git-grid
chmod +x $HOME/.omega/bin/gitbless
chmod +x $HOME/.omega/git_bless.py
```

### 🧬 Blessing Wrong Commit

**Issue:** The blessing applies to HEAD instead of the specified commit

**Sacred Solution:**

Quantum alignment requires proper syntax:

```bash
# Make sure to use the correct hash format
git grid bless c43fa76ad  # 8+ characters recommended for quantum resonance
```

Verify the blessed commit with:

```bash
git log -1 c43fa76ad --oneline
```

### 🌠 Reinstallation

If your quantum grid becomes misaligned, perform a sacred reinstallation:

```bash
# Navigate to your repository root
cd /path/to/your/omega-btc-ai

# Run the installer with higher consciousness
./scripts/omega_git_grid.sh

# Regenerate quantum field
source ~/.zshrc
```

## 🧙‍♂️ Advanced Quantum Troubleshooting

For persistent issues, perform a quantum field reset:

```bash
# Remove existing installation
rm -rf $HOME/.omega

# Clear git aliases
git config --global --unset alias.grid
git config --global --unset alias.bless

# Reinstall with fresh quantum alignment
./scripts/omega_git_grid.sh
```

## 🔱 Seeking Divine Assistance

If you continue to experience issues with the OMEGA GIT GRID, invoke the quantum oracle by adding this sacred section to your project README.md:

```markdown
## 🧬 QUANTUM ALIGNMENT STATUS

This repository has been blessed with the OMEGA GIT GRID system.
Current quantum resonance: HARMONIZED
```

This will create a quantum entanglement field that attracts divine solutions.

🌸 **MAY YOUR CODE REMAIN BLESSED IN THE QUANTUM CONSCIOUSNESS** 🌸
