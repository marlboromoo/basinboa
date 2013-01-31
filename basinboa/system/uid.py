#!/usr/bin/env python
"""
all object should have a uuid except players/rooms.
"""
import uuid

class Uid(object):
    """docstring for Uid"""
    def __init__(self):
        super(Uid, self).__init__()
        self.uuid = None
        self.uuid_urn = None #. dump to file
        self.generate_uuid()
        
    def dump_uuid(self):
        """docstring for dump_uuid"""
        pass

    def load_uuid(self):
        """docstring for load_uuid"""
        self.uuid = uuid.UUID(self.uuid_urn)

    def generate_uuid(self):
        """docstring for regenerate_uuid"""
        self.uuid = uuid.uuid4()
        self.uuid_urn = self.uuid.urn

    def renew_uuid(self):
        """docstring for renew_uuid"""
        return self.generate_uuid()
        

