import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

def clone_repository(git_url):
    try:
        temp_dir = tempfile.TemporaryDirectory()
        subprocess.run(["git", "clone", "--depth", "1", git_url, temp_dir.name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None

def count_lines_in_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)
    except Exception:
        return 0

def count_lines_in_repo(repo_path, extensions=None):
    if extensions is None:
        extensions = [
        # Python
        ".py", ".pyc", ".pyo", ".pyw", ".pyx", ".pxd", ".pxi",

    	# JavaScript
    	".js", ".mjs", ".cjs",

    	# TypeScript
    	".ts", ".tsx",

    	# Java
    	".java", ".class", ".jar", ".jad",

    	# C / C++
    	".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hh", ".hxx",

    	# C#
    	".cs",

    	# HTML / CSS
    	".html", ".htm", ".xhtml", ".jhtml",
    	".css", ".scss", ".sass", ".less",

    	# Markdown
    	".md", ".markdown", ".mkd",

    	# PHP
    	".php", ".phtml", ".php3", ".php4", ".php5", ".php7", ".phps",

    	# Ruby
    	".rb", ".erb", ".rake",

    	# Perl
    	".pl", ".pm", ".pod", ".t", ".psgi",

    	# Bash / Shell
    	".sh", ".bash", ".zsh", ".ksh", ".csh", ".tcsh",

    	# PowerShell
    	".ps1", ".psm1", ".psd1",

    	# Go
    	".go",

    	# Rust
    	".rs",

    	# Kotlin
    	".kt", ".kts",

    	# Swift
    	".swift",

    	# Dart
    	".dart",

    	# SQL
    	".sql",

    	# YAML / JSON
    	".yml", ".yaml", ".json",

    	# XML
    	".xml", ".xsl", ".xsd", ".kml",

    	# Lua
    	".lua",

    	# R
    	".r", ".rdata", ".rds",

    	# MATLAB
    	".m", ".mat", ".fig",

    	# Haskell
    	".hs", ".lhs",

    	# Scala
    	".scala", ".sc",

    	# Lisp / Scheme
    	".lisp", ".lsp", ".cl", ".scm",

    	# Prolog
    	".pl", ".pro", ".p",

    	# Assembly
    	".asm", ".s", ".a",

    	# Fortran
    	".f", ".for", ".f90", ".f95",

    	# COBOL
    	".cob", ".cbl", ".cpy",

    	# Pascal
    	".pas", ".pp", ".inc",

    	# Groovy
    	".groovy", ".gvy", ".gy", ".gsh",

    	# Julia
    	".jl",

    	# Crystal
    	".cr",

    	# Scripting
    	".bat", ".cmd", ".awk", ".sed", ".tcl", ".vbs", ".jscript", ".wsf", ".wsh",

    	# Configuration
    	".make", ".mk", ".cmake", ".ini", ".cfg", ".conf",

    	".ex", ".exs",  # Elixir
    	".ml", ".mli",  # OCaml
    	".adb", ".ads",  # Ada
	]

    total_lines = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    futures.append(executor.submit(count_lines_in_file, file_path))
        total_lines = sum(f.result() for f in futures)
    return total_lines

def main():
    import sys

    if len(sys.argv) > 1:
        git_url = sys.argv[1]
    else:
        git_url = input("URL Repo GitHub: ")

    try:
        print("Cloning the repository, this may take a while...")
        temp_dir = clone_repository(git_url)
        if temp_dir is None:
            return

        print("Counting lines of code")
        total_lines = count_lines_in_repo(temp_dir.name)
        print(f"\nRepository: {git_url}")
        print(f"Lines of code: {total_lines}")
        temp_dir.cleanup()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
