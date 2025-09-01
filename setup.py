from cx_Freeze import setup, Executable
import os

path = "asset"
asset_list = os.listdir(path)
asset_list_completa = [os.path.join(path, asset) for asset in asset_list]

executables = [Executable("main.py", base="Win32GUI")]

files = {
    "include_files": asset_list_completa,
    "packages": ["pygame", "os", "sys", "random"]
}

setup(
    name="Primeiro Jogo",
    version="1.0",
    description="Space Arcade app",
    options={"build_exe": files},
    executables=executables,
)