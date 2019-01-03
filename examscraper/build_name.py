import pdfkeywords, classify

def get_name(naming_rules, text_repr, classifier):
    for rule_name, rule in naming_rules.items():
