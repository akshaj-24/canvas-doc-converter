import re
import docx2txt
import json


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
        qtype = "constructed_response_question"

    return choices, correct, qtype

def parse_questions(text):
    pattern = r'(?:^|\n)(\d+[).]\s.*?)(?=\n\d+[).]\s|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    for block in matches:
        print("BLOCK:")
        print(block.strip())
        q_num_match = re.match(r'(\d+)[).]\s*', block)
        q_num = q_num_match.group(1) if q_num_match else "none"
        question_number = "Question " + q_num.zfill(3)
        print(question_number)
        choices, correct, qtype = parse_options(block)
        print("Choices:", choices)
        print("Correct:", correct)
        print("Question Type:", qtype)
        print("-----")


    

test_text = "Exam description\n1. Question one multiple choice question \n*a) Q1optA\nb) Q1optB \nc) Q1optC \nd) Q1optD\n\n2) Question\ntwo\n*A) Q2optA\n*B) Q2optB\n10. Question 10 \na. True\n*b. False"
parse_questions(test_text)
