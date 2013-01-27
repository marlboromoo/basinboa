#!/usr/bin/env python
"""
text encoder
"""
ENCODE = 'big5'

def texts_encoder(texts):
    """docstring for texts_encoder"""
    try:
        texts_ = texts.encode(ENCODE)
    except Exception:
        texts_ = text_filtering_encoder(texts)
    return texts_

def text_filtering_encoder(texts):
    """docstring for text_filtering_encoder"""
    texts_ = ''
    for text in texts:
        try:
            text_ = text.encode(ENCODE)
        except Exception:
            text_ = '--'
        texts_ += text_
    return texts_

        

