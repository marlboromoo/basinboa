#!/usr/bin/env python
"""
all object should have a uuid except players/rooms.
"""
import uuid

class Uid(object):
    """docstring for Uid"""
    def __init__(self):
        super(Uid, self).__init__()
        self.uuid = uuid.uuid4()
        self.uuid_urn = self.uuid.urn
        
    def dump_uuid(self):
        """docstring for dump_uuid"""
        pass

    def load_uuid(self):
        """docstring for load_uuid"""
        self.uuid = uuid.UUID(self.uuid_urn)
