import re


# Names is a list of names that are appended to text of pdf. The first name is checked first,
# and used as a default file name if tests fail.
def classify(text, names, binary=True, appendname=False):
    doctext = " ".join(names) + ' ' + text
    months = [('-1V', ['mai', 'juni', 'jun', 'may', 'june', 'spring', 'vår']),
              ('-3H', ['november', 'desember', 'december', 'høst', 'fall', 'dec', 'des', 'nov']),
              ('-2K', ['august', 'aug', 'sommer', 'summer'])]
    years = '(' + '|'.join(map(str, range(1990, 2020))) + ')'
    year = month = solution = None
    done = False
    # Search titles for information
    for iteryear in range(1990, 2020):
        if done:
            break
        for itermonth in months:
            if re.search('(' + '|'.join(itermonth[1]) + ')' + str(iteryear), ' '.join(names), flags=re.IGNORECASE):
                year, month = str(iteryear), itermonth[0]
                done = True
                break
    if re.search('L-', names[0], flags=re.IGNORECASE):
        solution = True
    # Search the document for information.
    if year is None:
        yearcounts = [(count_matches(str(year), doctext), str(year)) for year in range(1990, 2020)]
        year = max(yearcounts, key=lambda yc: yc[0])[1]
    if month is None:
        monthcounts = [(count_matches('(' + '|'.join(month[1]) + ')', doctext), month[0])
                       for month in months]
        month = max(monthcounts, key=lambda mc: mc[0])[1]

    if solution is None:
        solution = bool(re.search('(løsningsforslag|fasit)', doctext, flags=re.IGNORECASE))

    if year is not None:
        if month is not None:
            return year + month + 'L' * solution + (('(' + names[0] + ')') if appendname else "")
        return year + 'U' + 'L' * solution + (('(' + names[0] + ')') if appendname else "")

    print("Couldn't classify {}.".format(names[0]))
    return names[0]


def count_matches(pattern, string):
    return len(re.findall(pattern, string, flags=re.IGNORECASE))


if __name__ == '__main__':
    fp = open('M:/OneDrive - NTNU/Subjects/15 Matte 4K/exams/verext.pdf', 'rb')
    # print(classify_exam(fp, "Test exam", False))
