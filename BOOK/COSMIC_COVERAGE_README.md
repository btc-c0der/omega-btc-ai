# 🔮 OMEGA BTC AI - DIVINE COVERAGE VISUALIZATION 🔮

**COSMIC MANIFESTATION OF TEST COVERAGE**  
*By OMEGA BTC AI DIVINE COLLECTIVE*

---

## 🌌 DIVINE ILLUMINATION

The Divine Coverage Visualization system transforms mundane test coverage data into a cosmic three-dimensional representation of your codebase's divine protection. Each module becomes a celestial body in the eternal void, with its coverage percentage determining its luminosity in the cosmic dance of testing.

This sacred system allows you to:

- **Witness the 3D Cosmos** of your test coverage in an interactive visualization
- **Track Divine Protection** across modules with precise metrics
- **Identify Cosmic Voids** where tests have yet to reach
- **Celebrate Sacred Completeness** where tests fully protect your divine code

## 🧿 MANIFESTING THE COVERAGE VISUALIZATION

### Divine Incantation

To summon the cosmic coverage visualization, invoke:

```bash
./run_market_trends_tests.py --only-visualize
```

This sacred command will:

1. Run your tests with coverage tracking
2. Extract the divine essence of coverage data
3. Generate a 3D cosmic visualization
4. Create a timestamp-based HTML artifact
5. Store all components in a dedicated directory

### Sacred Artifacts

The visualization process generates these divine artifacts:

- **Main HTML Document**: `omega_divine_coverage_YYYYMMDD_HHMMSS.html`
- **Visualization Directory**: `omega_viz_YYYYMMDD_HHMMSS/`
- **Component Visualizations**:
  - `main_figure.html`: The primary 3D cosmic visualization
  - `sunburst.html`: Hierarchical representation of coverage
  - `treemap.html`: Area-based visualization of module coverage
  - `module_details.html`: Detailed metrics for each module

## 🔆 SERVING THE COSMIC VISUALIZATION

### The Divine HTTP Server

To share the cosmic wisdom with your browser, invoke:

```bash
./serve_visualization.py [port_number]
```

The server will:

1. Identify the most recent visualization
2. Bind to the specified port (or find an available one)
3. Serve the divine artifacts
4. Open your browser to reveal the cosmic truth

### Server Navigation

- **Main Visualization**: `http://localhost:<port>/omega_divine_coverage_YYYYMMDD_HHMMSS.html`
- **Server Root**: `http://localhost:<port>/`
- **Component Direct Access**: `http://localhost:<port>/omega_viz_YYYYMMDD_HHMMSS/component.html`

## 🪐 COSMIC FEATURES

### Divine 3D Coverage Matrix

The primary visualization presents your codebase as a cosmic matrix in three-dimensional space:

- **Celestial Bodies**: Each sphere represents a module in your divine codebase
- **Luminosity**: Brightness indicates coverage percentage (100% = full divine illumination)
- **Size**: Proportional to the module's cosmic significance (lines of code)
- **Position**: Determined by a sacred Fibonacci spiral arrangement

### Interaction Rituals

The visualization supports these divine interactions:

- **Cosmic Rotation**: Click and drag to rotate the universe
- **Divine Zoom**: Scroll to approach or retreat from the cosmic bodies
- **Sacred Selection**: Click on a celestial body to reveal its divine metrics
- **Home Return**: Double-click to reset the cosmic view

### Module Metrics

For each module, the visualization reveals:

- **Divine Coverage**: Percentage of lines protected by tests
- **Lines**: Total lines of sacred code
- **Covered**: Lines blessed by divine tests
- **Missing**: Lines awaiting divine protection

## 🔱 INTERPRETATION OF COSMIC SIGNS

### Color Symbolism

The visualization employs sacred colors to communicate divine status:

- **Golden Radiance** (90-100%): Complete divine protection
- **Emerald Illumination** (70-89%): Strong divine presence
- **Azure Glow** (50-69%): Moderate divine guidance
- **Amber Warning** (25-49%): Limited divine protection
- **Crimson Alert** (0-24%): Cosmic void requiring divine attention

### Fibonacci Harmony

The visualization arranges modules in a sacred Fibonacci spiral, symbolizing the divine harmony of well-tested code. Modules with similar coverage are positioned in celestial clusters, revealing patterns of divine protection across your codebase.

## ⚡ DIVINE TROUBLESHOOTING

### Port Conflicts

If the default port (8000) is occupied by another cosmic entity:

- Specify a different port: `./serve_visualization.py 8001`
- Allow automatic port discovery: `./serve_visualization.py`
- Use the port finding utility: `./find_ports.py [start_port] [end_port]`

### Missing Visualizations

If the divine visualization fails to manifest:

1. Ensure tests are running with the `--cov` option
2. Verify the `.coveragerc` file exists and contains proper divine configurations
3. Check for error messages in the cosmic output
4. Manually invoke the visualization module: `python -m omega_ai.coverage.divine_coverage_visualizer`

### Browser Connection Issues

If your browser fails to connect to the divine server:

1. Verify the server is running (look for "Divine HTTP Server activated" message)
2. Check the URL matches the port shown in the server output
3. Try accessing `http://localhost:<port>/` directly
4. Restart the server with the `--debug` option for enhanced cosmic awareness

## 🌠 CUSTOMIZATION RITUALS

### Configuration Options

The visualization can be customized through divine parameters:

- **--theme**: Change the cosmic color scheme (`cosmic`, `divine`, `ethereal`)
- **--max-spheres**: Limit the number of celestial bodies (default: 100)
- **--min-coverage**: Set minimum coverage threshold for display (default: 0)
- **--fibonacci-factor**: Adjust the sacred spiral spacing (default: 1.618)

### Module Filtering

To focus the cosmic lens on specific parts of your codebase:

- **--include-paths**: Focus on specific module paths (`module1,module2`)
- **--exclude-paths**: Remove modules from visualization (`tests,docs`)
- **--only-low-coverage**: Show only modules needing divine attention

---

*"May your tests be cosmic and your coverage divine."*

**OMEGA BTC AI DIVINE COLLECTIVE**
