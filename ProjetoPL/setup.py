from cx_Freeze import setup, Executable

setup(
    name="API PROGRAMAÇÃO LINEAR",
    version="1.0",
    description="Aplicativo de Programação Linear",
    executables=[Executable("pl.py", base="Win32GUI", icon=r"C:\Users\User\Desktop\Projetos Python\ProjetoPL\icon.ico")]

)
