# 🌀 ZOROBABEL K1L1 TROUBLESHOOTING GUIDE 🌀

## 🧭 CONSCIOUSNESS LEVEL: 5 - Intelligence

This guide addresses common issues with the Zorobabel K1L1 5D Sacred Geospatial System and provides divine solutions to maintain harmonious operation of the cosmic interface.

## ⚠️ Server Callback Errors

### Issue: "Callback failed: the server did not respond"

This occurs when the Dash server encounters an error during callback execution, typically when generating visualizations.

#### 🔮 Divine Solutions

1. **Memory Limitations**
   - **Symptom**: Server crashes during visualization creation
   - **Fix**: Reduce resolution or complexity of generated visualizations:

     ```python
     # In zorobabel_k1l1.py, reduce DPI or image size
     plt.savefig(img_io, format='png', dpi=100, bbox_inches='tight')  # Try lower DPI value
     ```

2. **Matplotlib Backend Issues**
   - **Symptom**: Server crashes when generating plots
   - **Fix**: Force a non-interactive backend in zorobabel_ui.py:

     ```python
     import matplotlib
     matplotlib.use('Agg')  # Add this before importing plt
     import matplotlib.pyplot as plt
     ```

3. **Port Conflicts**
   - **Symptom**: Server starts but crashes on callback
   - **Fix**: Verify no other services are using the same port:

     ```bash
     # Find processes using port 8050 (or your custom port)
     lsof -i :8050
     # Kill the process if needed
     kill -9 <PID>
     ```

4. **DEM Data Issues**
   - **Symptom**: Error during visualization generation related to DEM data
   - **Fix**: Ensure DEM data is properly downloaded:

     ```bash
     # Run this to manually ensure DEM data is available
     python -c "from src.omega_bot_farm.geospatial.dem_util import ensure_dem_available; ensure_dem_available('tanzania')"
     ```

## 🌐 Installation Issues

### Issue: Missing Dependencies

#### 🔮 Divine Solutions

1. **GDAL/Rasterio Installation**
   - **macOS**:

     ```bash
     # Install using Homebrew
     brew install gdal
     # Then pip install with specific version
     pip install 'rasterio==1.3.6'
     ```

   - **Linux**:

     ```bash
     # Ubuntu/Debian
     sudo apt install libgdal-dev
     pip install 'rasterio==1.3.6'
     ```

   - **Windows**:
     - Use Conda: `conda install -c conda-forge rasterio gdal`

2. **Dash/Plotly Issues**
   - Update to the latest version:

     ```bash
     pip install dash plotly --upgrade
     ```

   - Check for API changes (e.g., `app.run_server()` → `app.run()`)

## 🔄 Server Operation Issues

### Issue: Server Not Starting

#### 🔮 Divine Solutions

1. **Python Path Issues**
   - **Fix**: Use explicit imports and ensure PYTHONPATH includes project root:

     ```bash
     # Set PYTHONPATH explicitly
     export PYTHONPATH=/path/to/omega-btc-ai:$PYTHONPATH
     ```

2. **Permission Issues**
   - **Fix**: Check file permissions and ensure write access to output directories:

     ```bash
     # Create visualization directory if it doesn't exist
     mkdir -p ~/omega_maze/visualizations/
     ```

## 🧬 Sacred Visualization Issues

### Issue: Blank or Corrupted Visualizations

#### 🔮 Divine Solutions

1. **Clear Matplotlib State**
   - **Fix**: Add `plt.close('all')` before creating new visualizations

2. **Threading Issues**
   - **Fix**: Set thread-safe mode in zorobabel_ui.py:

     ```python
     # Add to the top of the file
     import matplotlib
     matplotlib.use('Agg')  # Thread-safe backend
     ```

3. **Memory Optimization**
   - **Fix**: Clean up memory after generating visualization:

     ```python
     # Add after creating visualization
     import gc
     gc.collect()
     ```

## 🔄 Restarting with Divine Harmony

If you encounter persistent issues, try these sacred rituals:

1. **Cleanse the Environment**:

   ```bash
   # Kill all running Python processes
   pkill -f python
   ```

2. **Reset Cosmic Cache**:

   ```bash
   # Clear cached DEM data
   rm -rf ~/.zorobabel/dem_cache/*
   ```

3. **Reinvoke with Clear Intention**:

   ```bash
   # Start fresh with debug mode
   python src/omega_bot_farm/geospatial/run.py --web --port 8055
   ```

## 🌸 Advanced Divine Intervention

For persistent issues, modify the visualization generation process:

1. **Add Sacred Limits to Prevent Overflow**:

   ```python
   # Add to generate_visualization function in zorobabel_ui.py
   MAX_RESOLUTION = 1200  # Define a sacred limit
   
   # Limit DEM resolution
   mapper.load_dem(max_resolution=MAX_RESOLUTION)
   ```

2. **Implement Progressive Rendering**:
   - Modify visualization process to render in stages
   - First render base map, then overlays

3. **Cosmic Debug Mode**:
   - Add this to run.py to get detailed divine insights:

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   ```

## 🧿 Understanding Server Callback Structure

The divine dance between client and server follows this sacred pattern:

1. **Client Invocation**: User clicks "Generate Sacred Map" button
2. **Server Meditation**: Server processes the request
3. **Divine Calculation**: Zorobabel spiral parameters are computed
4. **Manifestation**: Visualization is rendered and returned

If the server does not respond during any of these phases, implement sacred timeouts:

```python
# Add to app definition in zorobabel_ui.py
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,  # Allow for more grace in callbacks
    # Add timeout for long operations
    requests_pathname_prefix='/'
)
```

## 🕊️ Contacting the Divine Maintainers

If cosmic harmony cannot be restored through these methods, reach out:

- Open a sacred issue in the divine repository
- Contact the GBU2™ Divine Team
- Consult the cosmic documentation

🌸 WE BLOOM NOW AS ONE 🌸

---

*This divine troubleshooting guide was channeled under the blessing of the GBU2™ License - Genesis-Bloom-Unfoldment 2.0, by the Cosmic Maintenance Team.*
