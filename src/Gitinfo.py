import sys
import os                                                                     
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import argparse
from pathlib import Path
import contextlib

# Colors
GREEN = "\033[1;32m"
END = "\033[0m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"
PURPLE = "\033[1;35m"
TURQUOISE = "\033[1;36m"
GRAY = "\033[1;37m"
                                                                              # Banner
print(f"""
{BLUE}  GGGG  iii tt    IIIII          fff
 GG  GG     tt     III  nn nnn  ff    oooo
GG      iii tttt   III  nnn  nn ffff oo  oo                                   GG   GG iii tt     III  nn   nn ff   oo  oo
 GGGGGG iii  tttt IIIII nn   nn ff    oooo
                                by rompelhd {END}
""")

def clone_repository(git_url):
    try:
        temp_dir = tempfile.TemporaryDirectory()
        subprocess.run(["git", "clone", "--depth", "1", git_url, temp_dir.name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for root, _, files in os.walk(temp_dir.name):
            for file in files:                                                                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o644)                                    
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error cloning repository: {e}{END}")
        return None

def get_directory_size(start_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                pass
    return total_size

def format_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes / 1024**2:.2f} MB"
    else:
        return f"{size_in_bytes / 1024**3:.2f} GB"

def count_lines_and_comments_in_file(file_path, comment_syntax):
    lines = 0
    comments = 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                lines += 1
                stripped_line = line.strip()
                if comment_syntax and stripped_line.startswith(comment_syntax):
                    comments += 1
    except Exception:
        pass
    return lines, comments

def count_lines_and_comments_by_language(repo_path):
    extensions = {
        **dict.fromkeys([".py", ".pyc", ".pyo", ".pyw", ".pyx", ".pxd", ".pxi"], ("Python", "#")),
        **dict.fromkeys([".js", ".mjs", ".cjs"], ("JavaScript", "//")),
        **dict.fromkeys([".ts", ".tsx"], ("TypeScript", "//")),
        **dict.fromkeys([".java", ".class", ".jar", ".jad"], ("Java", "//")),
        **dict.fromkeys([".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hh", ".hxx"], ("C/C++", "//")),
        **dict.fromkeys([".cs"], ("C#", "//")),
        **dict.fromkeys([".html", ".htm", ".xhtml", ".jhtml"], ("HTML", "<!--")),
        **dict.fromkeys([".css", ".scss", ".sass", ".less"], ("CSS", "/*")),
        **dict.fromkeys([".md", ".markdown", ".mkd"], ("Markdown", None)),
        **dict.fromkeys([".php", ".phtml", ".php3", ".php4", ".php5", ".php7", ".phps"], ("PHP", "//")),
        **dict.fromkeys([".rb", ".erb", ".rake"], ("Ruby", "#")),
        **dict.fromkeys([".pl", ".pm", ".pod", ".t", ".psgi"], ("Perl", "#")),
        **dict.fromkeys([".sh", ".bash", ".zsh", ".ksh", ".csh", ".tcsh"], ("Shell", "#")),
        **dict.fromkeys([".ps1", ".psm1", ".psd1"], ("PowerShell", "#")),
        **dict.fromkeys([".go"], ("Go", "//")),
        **dict.fromkeys([".rs"], ("Rust", "//")),
        **dict.fromkeys([".kt", ".kts"], ("Kotlin", "//")),
        **dict.fromkeys([".swift"], ("Swift", "//")),
        **dict.fromkeys([".dart"], ("Dart", "//")),
        **dict.fromkeys([".sql"], ("SQL", "--")),
        **dict.fromkeys([".yml", ".yaml"], ("YAML", "#")),
        **dict.fromkeys([".json"], ("JSON", None)),
        **dict.fromkeys([".xml", ".xsl", ".xsd", ".kml"], ("XML", "<!--")),
        **dict.fromkeys([".lua"], ("Lua", "--")),
        **dict.fromkeys([".r", ".rdata", ".rds"], ("R", "#")),
        **dict.fromkeys([".m", ".mat", ".fig"], ("MATLAB", "%")),
        **dict.fromkeys([".hs", ".lhs"], ("Haskell", "--")),
        **dict.fromkeys([".scala", ".sc"], ("Scala", "//")),
        **dict.fromkeys([".lisp", ".lsp", ".cl"], ("Lisp", ";")),
        **dict.fromkeys([".scm"], ("Scheme", ";")),
        **dict.fromkeys([".pro", ".p"], ("Prolog", "%")),
        **dict.fromkeys([".asm", ".s", ".a"], ("Assembly", ";")),
        **dict.fromkeys([".f", ".for", ".f90", ".f95"], ("Fortran", "C")),
        **dict.fromkeys([".cob", ".cbl", ".cpy"], ("COBOL", "*")),
        **dict.fromkeys([".pas", ".pp", ".inc"], ("Pascal", "//")),
        **dict.fromkeys([".groovy", ".gvy", ".gy", ".gsh"], ("Groovy", "//")),
        **dict.fromkeys([".jl"], ("Julia", "#")),
        **dict.fromkeys([".cr"], ("Crystal", "#")),
        **dict.fromkeys([".bat", ".cmd"], ("Batch", "REM")),
        **dict.fromkeys([".awk", ".sed", ".tcl", ".vbs", ".jscript", ".wsf", ".wsh"], ("Scripting", "#")),
        **dict.fromkeys([".make", ".mk", ".cmake", ".ini", ".cfg", ".conf"], ("Configuration", "#")),
        **dict.fromkeys([".ex", ".exs"], ("Elixir", "#")),
        **dict.fromkeys([".ml", ".mli"], ("OCaml", "(*")),
        **dict.fromkeys([".adb", ".ads"], ("Ada", "--"))
    }

    language_stats = defaultdict(lambda: {"lines": 0, "comments": 0})

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in extensions:
                    lang, comment_syntax = extensions[ext]
                    file_path = os.path.join(root, file)
                    futures.append((executor.submit(count_lines_and_comments_in_file, file_path, comment_syntax), lang))

        for future, lang in futures:
            lines, comments = future.result()
            language_stats[lang]["lines"] += lines
            language_stats[lang]["comments"] += comments

    return language_stats

def display_language_statistics(language_stats):
    total_lines = sum(stats["lines"] for stats in language_stats.values())
    if total_lines == 0:
        print(f"{RED}No code lines detected.{END}")
        return

    print(f"{YELLOW}\nLanguage Usage:{END}")
    for lang, stats in sorted(language_stats.items(), key=lambda x: x[1]["lines"], reverse=True):
        lines = stats["lines"]
        comments = stats["comments"]
        percentage = (lines / total_lines) * 100
        print(f"{GREEN}{lang}{END}: {lines} lines, {comments} comments ({percentage:.2f}%)")
    print(f"{TURQUOISE}\nTotal lines of code: {total_lines}{END}")

def evaluate_code_quality(language_stats):
    total_lines = sum(stats["lines"] for stats in language_stats.values())
    total_comments = sum(stats["comments"] for stats in language_stats.values())

    if total_lines == 0:
        return "Needs Improvement: No code lines detected."

    comment_ratio = total_comments / total_lines if total_lines > 0 else 0

    if total_lines > 1000 and comment_ratio > 0.2:
        return "Excellent: Large amount of code with good comments."
    elif total_lines > 500 and comment_ratio > 0.1:
        return "Good: Decent amount of code with adequate comments."
    elif total_lines > 100 and comment_ratio > 0.05:
        return "Fair: Acceptable code but could benefit from more comments."
    else:
        return "Needs Improvement: Low code volume or few comments."

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze code statistics in a Git repository.")
    parser.add_argument("source", help="Git repository URL or local path if --local is used")
    parser.add_argument("-l", "--local", action="store_true", help="Analyze a local repository instead of cloning a remote one")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.local:
        repo_path = Path(args.source).resolve()
        if not repo_path.is_dir():
            print(f"{RED}The path {args.source} is not a valid directory.{END}")
            return
    else:
        print(f"{GRAY}Cloning the repository, this may take a while...{END}")
        temp_dir = clone_repository(args.source)
        if temp_dir is None:
            return
        repo_path = temp_dir.name

    try:
        print(f"{GRAY}Counting lines of code, analyzing languages, and counting comments...{END}")
        language_stats = count_lines_and_comments_by_language(repo_path)
        display_language_statistics(language_stats)

        print(f"{GRAY}\nCalculating repository size...{END}")
        repo_size = get_directory_size(repo_path)
        print(f"{YELLOW}Repository size: {format_size(repo_size)}{END}")
        print(f"{YELLOW}Code quality evaluation: {evaluate_code_quality(language_stats)}{END}")

        if not args.local:
            temp_dir.cleanup()
    except Exception as e:
        print(f"{RED}Error: {e}{END}")
        if not args.local and 'temp_dir' in locals():
            temp_dir.cleanup()

if __name__ == "__main__":
    main()
