import re


def replaceTrChars(x):
    tr_chars = ['ç', 'Ç', 'Ş', 'ş', 'ü', 'Ü', 'ğ', 'Ğ', 'ı', 'İ', 'ö', 'Ö']
    en_chars = ['c', 'C', 'S', 's', 'u', 'U', 'g', 'G', 'i', 'I', 'o', 'O']
    for i, val in enumerate(tr_chars):
        x = x.replace(val, en_chars[i])
    return x


def urlGenerator(model, title):
    url = replaceTrChars(title.lower())
    url = re.sub('[^a-zA-Z0-9]', ' ', url).strip()
    url = re.sub(' +', '-', url)

    new_url = None
    if model.objects.filter(url=url).first():
        suffix_counter = 2
        new_url = url + "-2"
        while model.objects.filter(url=new_url).first():
            new_url = url + '-' + str(suffix_counter)
            suffix_counter += 1

    if new_url is not None:
        return new_url

    return url
