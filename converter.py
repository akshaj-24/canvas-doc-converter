import json
import os
import subprocess
import sys
import re
import tkinter as tk
from tkinter import messagebox
import docx2txt

def open_and_highlight_file(filepath):
    if sys.platform == "win32":
        subprocess.run(['explorer', '/select,', os.path.normpath(filepath)])
    elif sys.platform == "darwin":
        subprocess.run(["open", "-R", filepath])
    else:
        folder = os.path.dirname(filepath)
        subprocess.run(["xdg-open", folder])

def error_question_num(block):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Error parsing question number in block: {block[:30]}")
    root.destroy()
    return "unknown"

def parse_questions(text):
    questions = []
    question_blocks = re.split(r'\n\d+[).]\s', text)

    for block in question_blocks[1:]:
        print(block)
        q_num_match = re.match(r'(\d+)[).]\s*', block)
        q_num = q_num_match.group(1) if q_num_match else error_question_num(block)
        question_number = "Question " + q_num.zfill(3)

def convert_to_txt(docx):
    text = docx2txt.process(docx)
    return text


def parse_options(block):
    option_pattern = r'(\*?)([a-zA-Z])[).]\s*(.*?)(?= *\*?[a-zA-Z][).]\s|\n*\d+[).]\s|\Z)'
    options = re.findall(option_pattern, block, re.DOTALL)
    
    choices = []
    correct = []
    for index, (corr, label, text) in enumerate(options):
        choices.append(text.strip())
        if corr == "*":
            correct.append(index)

    # Determine question type
    if len(choices) == 2 and all(choice.lower() in ("true", "false") for choice in choices):
        qtype = "true_false_question"
    elif len(correct) == 1:
        qtype = "multiple_choice_question"
    elif len(correct) > 1:
        qtype = "multiple_answers_question"
    else:
        qtype = "NA PLEASE FILL IN"

    return choices, correct, qtype

def parse_questions(text, nurs):
    pattern = r'(?:^|\n)(\d+[).]\s.*?)(?=\n\d+[).]\s|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    questions_list = []

    for block in matches:
        print("BLOCK:")
        print(block.strip())
        q_num_match = re.match(r'(\d+)[).]\s*', block)
        q_num = q_num_match.group(1) if q_num_match else "none"
        question_number = "Question " + q_num.zfill(3)
        print(question_number)
        choices, correct, qtype = parse_options(block)
        question = {
            "questionNumber": question_number,
            "questionText": block.strip(),
            "answerChoices": choices,
            "correctAnswers": correct,
            "questionType": qtype,
            "nurs": nurs
        }
        questions_list.append(question)
        return questions_list

def convert(doc_path, nurs):
    text = convert_to_txt(doc_path)
    questions = parse_questions(text, nurs)
    with open(json_path := doc_path.replace('.docx', '_build.json'), 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    open_and_highlight_file(json_path)
    return {"status": "success", "file": doc_path, "option": nurs}
