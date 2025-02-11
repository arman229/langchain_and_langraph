# UV Project Create and Setup VS Code

    uv version

    uv help

    uv init first_uv_project

This command sets up a project structured for packaging, placing your code inside a src directory, aligning with best practices for Python project structures.

    cd first_uv_project

    code .

Use code . on terminal or open the directory first_uv_project in VSCode

Now Create Virtual environment:

    uv venv

Activate virtual environment:


    In Windows 
    .\.venv\Scripts\activate

   or

- Open VS Code.
- Press Ctrl+Shift+P (or Cmd+Shift+P on macOS) to open the Command Palette.
- Type Python: Select Interpreter and select the interpreter located in .venv\Scripts\python.exe (Windows) or .venv/bin/python (macOS/Linux).      

Select Recommended Python Interpreter (./.venv/bin/python) created by virtual envirnoment in VSCode

    uv run hello.py




    


