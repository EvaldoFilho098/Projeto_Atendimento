from cx_Freeze import setup, Executable
exe = Executable(
    script="Aplicacao.pyw",
    base="Win32GUI",                           # Retirar comentario se for contruir um executavel para windows
    )
setup(
    name = "Cadastro de Atendimentos",
    version = "1.0.0",
    description = "Programinha para cadastrar atendimentos do suporte",
    options = {"build_exe": {
    'include_files': ['Icons/Icon.ico','Icons/Logo_.png','Icons/Logo.png'],
    'include_msvcr': True,
    }},
    executables = [exe]
    )
