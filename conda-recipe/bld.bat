if "%PYTHON%"=="" (set PYTHON=python)
"%PYTHON%" setup.py clean --all
if errorlevel 1 exit 1

"%PYTHON%" setup.py install
if errorlevel 1 exit 1
