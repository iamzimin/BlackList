from cx_Freeze import setup, Executable

setup(
    name="BlackList",
    version="1.0",
    executables=[Executable("blackList.py", base="Win32GUI")],
)