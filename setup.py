import cx_Freeze

executables = [cx_Freeze.Executable("game.py", base="Win32GUI")]

cx_Freeze.setup(
    name="RedHood",
    options={"build_exe": {"packages":["pygame"], "include_files": ["resource"]}},
    executables=executables
)