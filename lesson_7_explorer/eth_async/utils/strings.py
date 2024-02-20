def text_between(text: str, begin: str = '', end: str = '') -> str:
    """
    Extract a text between strings.

    :param str text: a source text
    :param str begin: a string from the end of which to start the extraction
    :param str end: a string at the beginning of which the extraction should end
    :return str: the extracted text or empty string if nothing is found
    """
    try:
        if begin:
            start = text.index(begin) + len(begin)
        else:
            start = 0
    except:
        start = 0

    try:
        if end:
            end = text.index(end, start)
        else:
            end = len(text)
    except:
        end = len(text)

    excerpt = text[start:end]
    if excerpt == text:
        return ''

    return excerpt
