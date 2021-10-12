import warnings
from pathlib import Path

import spacy
import typer
from spacy.tokens import DocBin


def parse_tuple(string):
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        return
    except:
        return


def convert_jsonl(lang: str, input_path: Path, output_path: Path):
    train_data = []
    with open(input_path, encoding='utf-8', mode='r') as input_file:
        for line in input_file:
            elements = parse_tuple(line)
            el1 = elements[0]
            el2 = eval(elements[1])
            train_data.append((el1, el2))

    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in train_data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(convert_jsonl)
