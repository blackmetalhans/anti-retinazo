@echo off
cd /d "%~dp0"
python -c "import sys; sys.path.insert(0, '.'); from gamma_engine import GammaEngine; GammaEngine().apply_warmth(0); print('Pantalla restaurada a 6500K neutral.')"
exit /b 0
