class Client:
    def __init__(self, client_id, client_name):
        self._client_id = client_id
        self._client_name = client_name

    @property
    def client_name(self):
        return self._client_name

    @property
    def client_id(self):
        return self._client_id

    @client_name.setter
    def client_name(self, new_name):
        self._client_name = new_name

    @client_id.setter
    def client_id(self, new_id):
        self._client_id = new_id

    def __eq__(self, other):
        if isinstance(other, Client) is False:
            return False
        return self._client_id == other._client_id

    def __str__(self):
        return str(self._client_id) + ', ' + str(self._client_name)
