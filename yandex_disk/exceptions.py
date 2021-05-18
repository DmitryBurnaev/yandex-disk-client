""" Define custom exception to detect yandex disk error
"""


class YaDiskInvalidStatusException(Exception):

    def __init__(self, code, text):
        self.code = code
        super(YaDiskInvalidStatusException, self).__init__(text)

    def __str__(self):
        base_str = super(YaDiskInvalidStatusException, self).__str__()
        return '{}: {}'.format(self.code, base_str)


class YaDiskInvalidResultException(Exception):

    def __init__(self, url, status):
        self.url = url
        self.status = status
        super(YaDiskInvalidResultException, self).__init__()

    def __str__(self):
        return 'resource: "{}" did not return correct status: {}'.format(
            self.url, self.status
        )
