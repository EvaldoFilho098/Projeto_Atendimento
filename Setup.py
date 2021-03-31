from cx_Freeze import setup, Executable
exe = Executable(
    script="Aplicacao.pyw",
    base="Win32GUI",                           # Retirar comentario se for contruir um executavel para windows
    )
setup(
    name = "Cadastro de Atendimentos",
    version = "0.0.2",
    description = "Programinha para cadastrar atendimentos do suporte",
    executables = [exe]
    )