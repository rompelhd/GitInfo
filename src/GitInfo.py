import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Banner
print("""
  GGGG  iii tt    IIIII          fff
 GG  GG     tt     III  nn nnn  ff    oooo
GG      iii tttt   III  nnn  nn ffff oo  oo
GG   GG iii tt     III  nn   nn ff   oo  oo
 GGGGGG iii  tttt IIIII nn   nn ff    oooo
                                by rompelhd
""")

def clone_repository(git_url):
    try:
        temp_dir = tempfile.TemporaryDirectory()
        subprocess.run(["git", "clone", "--depth", "1", git_url, temp_dir.name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None

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
        print("No code lines detected.")
        return

    print("\nLanguage Usage:")
    for lang, stats in sorted(language_stats.items(), key=lambda x: x[1]["lines"], reverse=True):
        lines = stats["lines"]
        comments = stats["comments"]
        percentage = (lines / total_lines) * 100
        print(f"{lang}: {lines} lines, {comments} comments ({percentage:.2f}%)")
    print(f"\nTotal lines of code: {total_lines}")

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

        print("Counting lines of code, analyzing languages, and counting comments...")
        language_stats = count_lines_and_comments_by_language(temp_dir.name)
        display_language_statistics(language_stats)
        temp_dir.cleanup()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
