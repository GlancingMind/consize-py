class Dictionary(list):
    def __init__(self):
        super().__init__()
        self._data = []

    def __setitem__(self, key, value):
        # Check if the key already exists and update the value if it does
        for i, (k, v) in enumerate(self._data):
            if k == key:
                self._data[i] = (key, value)
                return
        # Otherwise, add a new key-value pair
        self._data.append((key, value))

    def __getitem__(self, key):
        # Search for the key and return its value if found
        for k, v in self._data:
            if k == key:
                return v
        # Raise KeyError if the key is not found
        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key):
        # Search for the key and remove the corresponding key-value pair if found
        for i, (k, v) in enumerate(self._data):
            if k == key:
                del self._data[i]
                return
        # Raise KeyError if the key is not found
        raise KeyError(f"Key '{key}' not found")

    def __contains__(self, key):
        # Check if the key exists in the list
        return any(k == key for k, v in self._data)

    def __len__(self):
        # Return the number of key-value pairs
        return len(self._data)

    def __iter__(self):
        # Iterate over the keys in the dictionary
        for k, v in self._data:
            yield k

    def items(self):
        # Return a list of tuples (key, value)
        return self._data

    def keys(self):
        # Return a list of keys
        return [k for k, v in self._data]

    def values(self):
        # Return a list of values
        return [v for k, v in self._data]

    def __repr__(self):
        dr = ""
        for t in self._data:
            k, v = t
            dr += k
            if not k.startswith("@"):
                dr += v

        return "{ "+dr+" }"

    def copy(self):
        new_dict = Dictionary()
        new_dict._data = self._data.copy()
        return new_dict

    def __eq__(self, other):
        if isinstance(other, list):
            return other == self._data
        if isinstance(other, Dictionary):
            return self._data == other._data
        return False

    def __bool__(self):
        return bool(self._data)

    def toList(self):
        l = []
        for t in self._data:
            k,v = t
            l.append(k)
            if not k.startswith("@"):
                l.append(v)

        return l
