#!/usr/bin/env python
"""
text encoder
"""
from basinboa import status

def texts_encoder(texts):
    """docstring for texts_encoder"""
    try:
        texts_ = texts.encode(status.LANG.get_encode())
    except Exception:
        texts_ = text_filtering_encoder(texts)
    return texts_

def text_filtering_encoder(texts):
    """docstring for text_filtering_encoder"""
    texts_ = ''
    for text in texts:
        try:
            text_ = text.encode(status.LANG.get_encode())
        except Exception:
            text_ = '-'
        texts_ += text_
    return texts_

        

