<div align="center">
  <img src="RRADME.assets/banner.png" alt="Vehicle Side Slip Dashboard Banner" width="100%">
  <h1 align="center">Vehicle Side Slip Dashboard</h1>
</div>

This project is a web application built with Streamlit that visualizes vehicle dynamics, specifically focusing on side slip data. It provides interactive controls and visualizations to help users understand vehicle behavior under various conditions.

## Setup Instructions

Follow these steps to set up the project environment:

1. **Create a new conda environment:**
   ```bash
   conda create -n tmp python=3.10 -y
   ```

2. **Activate the conda environment:**
   ```bash
   conda activate tmp
   ```

3. **Install `uv` first:**
   ```bash
   pip install uv
   ```

4. **Install the required packages:**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Navigate to the source directory:**
   ```bash
   cd src/
   ```

6. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Development Instructions (Code Linting)

   ```bash
   ruff check
   ruff format
   ```


## Notes
- Ensure you have `conda` and `pip` installed on your system.
- Adjust the Python version in step 1 if necessary.