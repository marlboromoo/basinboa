#!/usr/bin/env python
"""
load object from file
"""
import os
import yaml

class YamlLoader(object):
    """docstring for YamlLoader"""

    FILE_TYPE = 'yaml'

    def __init__(self, data_dir):
        super(YamlLoader, self).__init__()
        self.data_dir = data_dir

    def _load(self, path):
        """docstring for _load"""
        try:
            with open(path, 'r') as f:
                data = yaml.load(f, Loader=yaml.Loader)
                return data
        except Exception:
            return None

    def load(self, name):
        """return data by name"""
        path = os.path.join(self.data_dir, "%s.%s" % (name, self.FILE_TYPE))
        return self._load(path)

    def load_all(self):
        """return all data from data_dir"""
        datas = []
        for fname in os.listdir(self.data_dir):
            path = os.path.join(self.data_dir, fname)
            data = self._load(path)
            datas.append(data) if data else None
        return datas

    def dump_from_object(self, object_):
        """docstring for dump"""
        path = os.path.join(self.data_dir, "%s.yaml" % object_.get_name())
        with open(path, 'w') as f:
            f.write(yaml.dump(object_.dump()))

    def dump(self, object_):
        """dump object to yaml file"""
        return self.dump_from_object(object_)

if __name__ == '__main__':
    yl = YamlLoader('../data/mob/')
    print yl.load_all()
    print yl.load('dog')
