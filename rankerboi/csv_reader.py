import csv
import keyword

_kwords = keyword.kwlist

class CSVReader(object):

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
        self._find_code_column()
        self._header = data[0]
        self.data = data[1:]
        self.name_col = 0 # fair assumption

    @property
    def header(self):
        return self._header[:]

    def _find_code_column(self):
        n = min(10, len(self.data))
        data = self.data
        m = len(data[0])
        counts = []
        for c in range(m):
            count = 0.
            for i in range(n):
                for k in _kwords:
                    count += data[i][c].count(k)
            counts.append(count)
        self.code_col = max(list(range(m)), key=counts.__getitem__)
