import tkinter as tk
from tkinter import filedialog, messagebox
from converter import convert

root = tk.Tk()
root.title("Doc Converter for Canvas")

tk.Label(root, text="Select a .doc or .docx file to convert:").pack(pady=10)
fileVar =  tk.StringVar()
fileEntry = tk.Entry(root, textvariable=fileVar, width=50)
fileEntry.pack(pady=5)

def browseFile():
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.doc;*.docx")])
    if file_path:
        fileVar.set(file_path)

browseButton = tk.Button(root, text="Browse", command=browseFile)
browseButton.pack(pady=5)

tk.Label(root, text="Nursing Quiz (Green Bg)").pack(pady=10)

optionVar = tk.StringVar(value="Yes")
tk.Radiobutton(root, text="Yes", variable=optionVar, value="true").pack(anchor='w')
tk.Radiobutton(root, text="No", variable=optionVar, value="false").pack(anchor='w')

def start():
    file_path = fileVar.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    selected_option = optionVar.get()
    messagebox.showinfo("Info", f"Converting {file_path} to JSON.")
    result = convert(file_path, selected_option)
    messagebox.showinfo("Success", f"Process Complete")

startButton = tk.Button(root, text="Start Conversion", command=start)
startButton.pack(pady=10)

root.mainloop()