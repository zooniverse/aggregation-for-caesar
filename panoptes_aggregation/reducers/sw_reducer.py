import collatex as col


def tokenize(self, contents):
    '''tokenize only on space so angle bracket tags are not split'''
    return contents.split()


# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize
