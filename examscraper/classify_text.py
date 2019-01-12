import copy
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
    return name


def _classify_class(fragment, text, names):
    # TODO: Use _unique and _strict_max, like in _classify_range
    # TODO: Add targeting of specific names
    classes = fragment['classes']
    # Build strings to search
    namestring = ' '.join(names)
    if fragment.get('prioritizeNames', False):
        # Search names for tags. No action if there are multiple matches.
        # Add additional identifiers to classes
        name_classes = fragment.get('nameAdditions', {})
        all_classes = copy.deepcopy(classes)
        for classname, identifiers in name_classes.items():
            if all_classes.get(classname, None) is None:
                all_classes[classname] = identifiers
            else:
                all_classes[classname] += identifiers
        # Find identifiers in names
        name_counts = []
        for classname, identifiers in all_classes.items():
            matchcount = _count_matches('(' + '|'.join(identifiers) + ')', namestring)
            if matchcount:
                name_counts.append([classname, matchcount])
        if len(name_counts) == 1:
            return name_counts[0][0]
    # If the name results in no matches, match in entire text.
    complete_text = namestring + ' ' + text
    counts = {}
    for classname, identifiers in classes.items():
        pattern = '(' + '|'.join(identifiers) + ')'
        counts[classname] = _count_matches(pattern, complete_text)
    # Most occurring word
    max_count = max(counts.items(), key=lambda i: i[1])
    if len(list(filter(lambda x: x == max_count[1], counts.values()))) > 1 or max_count[1] == 0:
        # Return default value if there is ambiguity (more than one maximum)
        return fragment.get('default', '')
    # Else return
    return max_count[0]


def _classify_range(fragment, text, names):
    namestring = ' '.join(names)

    # Get min and max values in range. Non-inclusive.
    rmin = fragment.get('min')
    rmax = fragment.get('max', rmin)
    # Check names first
    if fragment.get('prioritizeNames', False):
        name_counts = [(str(num), _count_matches(str(num), namestring))
                       for num in range(rmin, rmax)]
        max_count = _strict_max(name_counts, lambda x: x[1])
        if max_count is not None and max_count[1] != 0:
            return max_count[0]

    complete_text = namestring + ' ' + text
    # Count occurrences of each number
    counts = [(str(num), _count_matches(str(num), complete_text)) for num in range(rmin, rmax)]
    # Maximum number of occurrences
    max_count = _strict_max(counts, lambda x: x[1])
    # If there are more than one with the same count
    if max_count is None or max_count[1] == 0:
        return fragment.get('default', '')
    return max_count[0]


def _count_matches(pattern, string):
    return len(re.findall(pattern, string, flags=re.IGNORECASE))


def _unique(iterable, element):
    """
    Returns false if the element occurs more than once.
    :param iterable: Iterable with elements
    :param element: Element to equal
    :return: Whether or not the element is unique in the sequence.
    """
    found = False
    for val in iterable:
        if val == element:
            if found:
                return False
            found = True
    return True


def _strict_max(iterable, key):
    """
    Returns the strict max (unique max) of an iterable. Returns None if it doesn't exist.
    :param iterable:
    :param key:
    :return: Maximum element. Returns None if it isn't unique.
    """
    max_val = max(iterable, key=key)
    if not _unique(map(key, iterable), key(max_val)):
        return None
    return max_val


methods = {
    'class': _classify_class,
    'range': _classify_range
}
