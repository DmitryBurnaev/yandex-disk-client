

class Disk(object):
    """ Collect metadata information about storage """

    def __init__(self, trash_size, total_space, used_space, system_folders,
                 **kwargs):
        self.trash_size = trash_size
        self.total_space = total_space
        self.used_space = used_space
        self.system_folders = system_folders


class File(object):
    """ Collect  """
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Directory(object):
    """ Access to directory's children """

    def __init__(self, **kwargs):
        self._children = []

        for key in kwargs:
            if key is not '_embedded':
                setattr(self, key, kwargs[key])

        if '_embedded' in kwargs:
            for item in kwargs['_embedded']['items']:
                if item['type'] == 'dir':
                    d = Directory(**item)
                    self._children.append(d)

                if item['type'] == 'file':
                    f = File(**item)
                    self._children.append(f)

    @property
    def children(self):
        return self._children
