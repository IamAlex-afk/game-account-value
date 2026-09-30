"""Local number style for a translated string (counts and percents only).

Thousands in plain counts -> non-breaking space (1,147 -> 1 147); decimal percents -> comma (17.8% -> 17,8%).
Money stays as written in the source ($59.99, R$4,000, Rp80,000, €117), same convention as the
existing ru pages. Used for locales whose norm is space + decimal comma (uz, kk, ky, tk, ...).
"""
import re

CUR = re.compile(r"[$€£¥₩₫]|R\$|Rp")

def local_numbers(s: str) -> str:
    def thou(m):
        start = m.start()
        token_start = max(s.rfind(" ", 0, start), s.rfind("(", 0, start), s.rfind(" ", 0, start)) + 1
        if CUR.search(s[token_start:start]):
            return m.group(0)
        return m.group(0).replace(",", " ")
    s = re.sub(r"(?<![\d.,])\d{1,3}(?:,\d{3})+(?![\d,]*\.\d)", thou, s)
    s = re.sub(r"(?<![\d.])(\d+)\.(\d+)(?=\s?%)", r"\1,\2", s)
    return s

if __name__ == "__main__":
    for t in ["1,147 tadan 57 tasi", "$750–1,500", "~28,059,680 R$", "R$4,000 (~$755)", "17.8% ga", "Rp80,000 dan", "$9,171,511.80.", "(4,463 ta eʼlon)", "~61%+", "12,000 kubok, $3"]:
        print(t, "->", local_numbers(t))
