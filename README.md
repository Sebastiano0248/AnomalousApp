# AnomalousApp
Graphical application for a more user-friendly experience with AnomalousLib.

> ⚙️ Recommended Python version: Python 3.12.10 or higher.

## Development Setup
### 1. Set Up a Virtual Environment
Creating a virtual environment is not mandatory, but it is highly recommended for a clean installation. To set it up:
```bash
python -m venv venv
```
Then activate it:
- On **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- On **Windows**:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
> **💡 Note:** To deactivate the environment at any time (on both Linux and Windows), use:
> ```bash
> deactivate
> ```

### 2. Install Dependencies
Install the required libraries listed in ```requirements.txt```:
```bash
pip install -r requirements.txt
```
To verify the installation, you can regenerate the ```requirements.txt``` and check for any differences:
- On **Linux/macOS**:
    ```bash
    pip freeze | grep -vE "^-e |@ file://" > requirements.txt
    ```
- On **Windows**:
    ```powershell
    pip freeze | Select-String -NotMatch '^-e |@ file://' > requirements.txt
    ```
> **💡 Note:** This filtering step avoids including the local installation of the library itself.

If no changes appear in the file, the setup is correct.

## Repository Structure
```nginx
AnomalousApp
│   # App configuration
├───cache
│   # Stored datasets
├───data                 
│   ├───generated
│   └───raw
│   # Trained models
├───models
│   # Output results
├───results
│   ├───analysis
│   ├───predictions
│   └───reports
│   # GUI source code
└───ui
    │   # Utility classes
    ├───handlers
    │   # Menu subclasses
    ├───specific_menu
    │   # Paths, defaults, etc.
    ├───constants.py
    │   # Abstract menu class
    └───Menu.py
```

# How to run the App
Para correr la App con Python se puede hacer directamente ejecutando ./AnomalousApp.py:
```bash ./AnomalousApp.py
pyrhon 
```