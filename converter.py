import os
import subprocess
import sys

def open_and_highlight_file(filepath):
    if sys.platform == "win32":
        subprocess.run(['explorer', '/select,', os.path.normpath(filepath)])
    elif sys.platform == "darwin":
        subprocess.run(["open", "-R", filepath])
    else:
        folder = os.path.dirname(filepath)
        subprocess.run(["xdg-open", folder])

def convert(doc_path, nurs):
    # Placeholder for conversion logic
    print(f"Converting {doc_path} with option {nurs}")
    # Here you would add the actual conversion code



    open_and_highlight_file(doc_path) #switch to open_and_highlight_file with the output file path
    return {"status": "success", "file": doc_path, "option": nurs}