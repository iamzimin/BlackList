from cx_Freeze import setup, Executable

target = Executable(
    script="blackList.py",
    base="Win32GUI",
    icon="BlackList.ico",
    target_name="BlackList.exe"
    )

setup(
    name="BlackList",
    version="1.0",
    author="iamzimin",
    executables=[target]
    )
