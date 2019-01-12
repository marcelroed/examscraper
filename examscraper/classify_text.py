import re


def generate_name(naming, text, names):
    """
        Generates a name string from naming rules, document text and existing names
    """
    name = ''
    for fragname, fragment in naming.items():
        fragtype = fragment['type']
        if fragtype in methods.keys():
            name += methods[fragtype](fragment, text, names)
        else:
            raise ValueError("No such type for naming fragment")


"""class Classifier:
    def __init__(self, document):
        self.document = document
"""


def _classify_class(fragment, text, names):
    classes = fragment['classes']
    # Build strings to search
    namestring = ' '.join(names)
    if fragment.get('prioritizeNames', False):
        # Search names for tags. No action if there are multiple matches.
        # Add additional identifiers to classes
        name_classes = fragment.get('nameAdditions', {})
        all_classes = classes
        for classname, identifiers in name_classes.items():
            all_classes[classname] = identifiers
        # Find identifiers in names
        name_counts = []
        for classname, identifiers in all_classes.items():
            matchcount = count_matches('(' + '|'.join(identifiers) + ')', namestring)
            if matchcount:
                name_counts.append([classname, matchcount])
        if len(name_counts) == 1:
            return name_counts[0][0]
    # If the name results in no matches, match in entire text.
    complete_text = namestring + ' ' + text
    counts = {}
    for classname, identifiers in classes.items():
        pattern = '(' + '|'.join(identifiers) + ')'
        counts[classname] = count_matches(pattern, complete_text)
    # Most occurring word
    max_count = max(counts.items(), key=lambda i: i[1])
    if len(list(filter(lambda x: x == max_count[1], counts.values()))) > 1 or max_count[1] == 0:
        # Return default value if there is ambiguity (more than one maximum)
        return fragment.get('default', '')
    # Else return largest
    return max_count[0]


def _classify_range(fragment, text, names):
    pass


def count_matches(pattern, string):
    return len(re.findall(pattern, string, flags=re.IGNORECASE))


methods = {
    'class': _classify_class,
    'range': _classify_range
}
