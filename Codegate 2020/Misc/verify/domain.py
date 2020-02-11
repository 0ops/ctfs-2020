from math import inf


class Interval(object):
    def __init__(self, infimum, supremum):
        assert infimum <= supremum
        self.infimum = infimum
        self.supremum = supremum

    def __add__(self, other):
        infimum = self.infimum + other.infimum
        supremum = self.supremum + other.supremum
        return Interval(infimum, supremum)

    def __sub__(self, other):
        infimum = self.infimum - other.supremum
        supremum = self.supremum - other.infimum
        return Interval(infimum, supremum)

    def __mul__(self, other):
        candidate = [self.infimum * other.infimum, self.infimum * other.supremum, self.supremum * other.infimum, self.supremum * other.supremum]
        return Interval(min(candidate), max(candidate))

    def __or__(self, other):
        return Interval(min(self.infimum, other.infimum), max(self.supremum, other.supremum))

    def __repr__(self):
        return '[{}, {}]'.format(self.infimum, self.supremum)

    def widen(self, other):
        w_infimum = self.infimum if self.infimum <= other.infimum else -inf
        w_supremum = self.supremum if other.supremum <= self.supremum else inf
        return Interval(w_infimum, w_supremum)
