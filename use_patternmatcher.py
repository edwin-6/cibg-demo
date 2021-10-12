import spacy
from spacy import displacy
from spacy.tokens import Doc

from scripts.pattern_matchers.numeric_amount import NUMERIC_AMOUNT_LABEL
from scripts.pattern_matchers.util import create_selector


# Handmatige, eenmalige stap: 'python -m spacy download nl_core_news_md'
nlp = spacy.load("nl_core_news_md")

nlp.add_pipe("numeric_amount", before="ner")
nlp.add_pipe("merge_entities", last=True)
print([pipe for pipe in nlp.pipe_names])


def find_all_numeric_amount_tokens(doc: Doc):
    return [token for token in doc if token.ent_type_ == NUMERIC_AMOUNT_LABEL]


def find_potential_salaries(doc: Doc):
    potential_salaries = []
    bedrag_tokens = find_all_numeric_amount_tokens(doc)

    for bedrag in bedrag_tokens:
        for token in bedrag.ancestors:
            if token.lemma_ in ["ontvangen", "verkrijgen", "krijgen"]:
                salary_entity = create_selector(bedrag)
                potential_beneficiary = [child.text for child in token.children if child.dep_ == "nsubj"]
                potential_salaries.append({"Beneficiary": potential_beneficiary, "Salary": salary_entity})

    return potential_salaries

nog_niet_werkend_bedrag_patroon = "Henny wilt €34.567."
test_zinnen = "Mr. Gerard Theodorus Geraerts ontving in 2020 €136.059,- voor zijn diensten." \
              "De heer Johannes Gerardus kreeg als beloning €34.567,- voor zijn diensten. " \
              "Jan Pastoor verdient 89.012,- voor zijn diensten. " \
              "Mw. Klaassen heeft een salaris ontvangen van EUR 50.000,00 en daarnaast een onregelmatigheidstoeslag ter hoogte van EUR 2500,- ."

doc = nlp(test_zinnen)

print(f"Gevonden bedragen: {[t.text for t in find_all_numeric_amount_tokens(doc)]}")
for salary in find_potential_salaries(doc):
    print(salary)

# We can visualize the dependency tree and the found entities with spacy
options = {"compact": False}
displacy.serve(list(doc.sents), style="dep", options=options, port=8081, host="localhost")
# displacy.serve(doc, style="ent", options=options, port=8081, host="localhost")
