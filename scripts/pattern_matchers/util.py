import itertools
from dataclasses import dataclass
from typing import List, Tuple

from spacy.matcher import Matcher
from spacy.tokens import Span, Token


def overlaps(first: Span, second: Span):
    #  Range == empty if not overlapping
    #  The overlapping part is defined by the range described by the largest start and smallest end.
    #  For spans, end is not inclusive, which is also the case for ranges.
    #  A inversed range (ie. range(4,0)) is empty, so this always works
    return bool(range(max(first.start, second.start), min(first.end, second.end)))


def match_len(match):
    return match[2] - match[1]


def longest_matches_only(matches: list):
    disjoint = []
    matches.sort(key=match_len, reverse=True)
    for match in matches:
        overlapping = list(filter(lambda d: d[1] <= match[1] < d[2] or d[1] <= match[2] < d[2], disjoint))
        if not overlapping:
            disjoint.append(match)
        else:
            overlap = overlapping[0]
            if (match[2] - match[1]) > (overlap[2] - overlap[1]):
                disjoint.remove(overlap)
                disjoint.append(match)

    return disjoint


# De LongestOnlyMatcher hebben wij gecreeërd voor gevallen waarin we de langst mogelijk match willen gebruiken.
# Bijvoorbeeld: Een gewone matcher op de token text {a, ab, abc} die toegepast wordt op "abc def", returnt drie matches.
# De LongestOnlyMatcher geeft slechts de langste match terug (abc).
# Dit is nuttig voor bijvoorbeeld persoonsnamen (We willen Jan Johannes Klaassen, niet een gedeelte hiervan),
# of data (liever 22 november 2020 dan alleen 22 november)
class LongestOnlyMatcher(Matcher):
    def __call__(self, doc) -> List[Tuple[int, int, int]]:
        return longest_matches_only(super().__call__(doc))


def merge_spans(doc, spans):
    with doc.retokenize() as tokenizer:
        for span in spans:
            tokenizer.merge(span)


def __create_combination(*lists):
    return list(itertools.product(*lists))


def __assure_tuple(x):
    return x if type(x) is tuple else (x,)


def __join_elements(template: str, *combinations):
    result = list(map(lambda c: template.format(*__assure_tuple(c)), *combinations))
    return result


def add_and_merge_matches(label, doc, matches, overwrite_existing=False):
    spans = ()
    for match in matches:
        _, start, end = match
        span = Span(doc, start, end, label=label) if label else Span(doc, start, end)
        if overwrite_existing:
            if label:
                doc.ents = [ent for ent in list(doc.ents) if not overlaps(span, ent)]
            spans += (span,)
        else:
            if span and not any(overlaps(span, ent) for ent in spans) and not any(
                    overlaps(span, ent) for ent in doc.ents):
                spans += (span,)
    if label:
        doc.ents += spans
    merge_spans(doc, spans)


def create_selector(token: Token):
    return Selector(src_start=token.idx, src_end=token.idx + len(token), src_text=token.text)


@dataclass
class Selector:
    src_start: int or None
    src_end: int or None
    src_text: str or None