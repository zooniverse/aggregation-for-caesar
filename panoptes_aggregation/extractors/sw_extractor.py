def strip_tag(s):
    # remove unicode chars
    return s.encode('ascii', 'ignore').decode('ascii')
