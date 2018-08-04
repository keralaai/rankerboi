class AntiPlag(object):

    def __init__(self, threshold=0.9):
        self.threshold = threshold

    def _levenshtein_distance(self, code1, code2):
        if len(code1) > len(code2):
            code1, code2 = code2, code1
        distances = list(range(len(code1) + 1))
        for i2, c2 in enumerate(code2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(code1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def _similarity(self, code1, code2):
        if code1.replace(' ', '').lower() == code2.replace(' ', '').lower():
            return 1.0
        avg_code_len = 0.5 * (len(code1) + len(code2))
        ld = float(self._levenshtein_distance(code1, code2)) / avg_code_len
        return 1. - ld
        
        
    def __call__(self, codes):
        buckets = []
        sim = self._similarity
        t = self.threshold
        for i, c in enumerate(codes):
            added = False
            for b in buckets:
                for j in b:
                    c2 = codes[j]
                    if sim(c, c2) > t:
                        b.append(i)
                        added = True
                        continue
            if not added:
                new_bucket = [i]
                buckets.append(new_bucket)
        return [b for b in buckets if len(b) > 1]
