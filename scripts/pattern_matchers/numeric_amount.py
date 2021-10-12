from spacy import Language
from spacy.tokens import Doc

from scripts.pattern_matchers.util import LongestOnlyMatcher, __create_combination, __join_elements, \
    add_and_merge_matches

NUMBER_SHAPES = ['d', 'dd', 'ddd', 'dddd', 'd.ddd', 'ddddd', 'dd.ddd', 'dddddd', 'ddd.ddd', 'd.ddd.ddd', 'ddddddd',
                 'dd.ddd.ddd', 'dddddddd']
NUMBERS_AFTER_COMMA = ['dd', '-', '=']
DUTCH_CURRENCY_FORMAT = "{},{}"
NUMERIC_AMOUNT_LABEL = "BEDRAG"


def create_numeric_amount_matcher(vocab) -> LongestOnlyMatcher:
    matcher = LongestOnlyMatcher(vocab)
    create_amount_combinations = __create_combination(NUMBER_SHAPES, NUMBERS_AFTER_COMMA)
    amount_shapes = __join_elements(DUTCH_CURRENCY_FORMAT, create_amount_combinations)
    amount_pattern = [{"LOWER": {"IN": ["€", "eur"]}}, {'SHAPE': {"IN": amount_shapes}}]

    matcher.add('numeric_amount_pattern', [amount_pattern])
    return matcher


@Language.component("numeric_amount")
def numeric_amount(doc: Doc):
    label = NUMERIC_AMOUNT_LABEL
    numeric_amount_matcher = create_numeric_amount_matcher(doc.vocab)
    matches = numeric_amount_matcher(doc)
    add_and_merge_matches(label, doc, matches)
    return doc
