from pathlib import Path


def write_binary(location, filename, data, overwrite=False):
    slug = ''
    if not overwrite:
        while True:
            file_path = Path(construct_name(location, filename, slug))
            if file_path.exists():
                if slug == '':
                    slug = '1'
                else:
                    slug = str(int(slug) + 1)
            else:
                break
    file = open(construct_name(location, filename, slug), 'wb')
    file.write(data)
    file.close()


def construct_name(location, filename, slug):
    return location + '.'.join(filename.split('.')[:-1]) + slug + '.' + filename.split('.')[-1]
