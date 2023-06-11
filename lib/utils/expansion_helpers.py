from .expansion_flags import F
from .poker_iterator import PokerIterator

SUIT_LIST = list('hdcs')

class ExpansionHelpers:

    # strip flags and return cards only
    def getRawHand(self, combo: str) -> str:
        return combo[0:2]

    # '22-77' -> ['22', '77']
    def getRawHandAndCeiling(self, combo: str) -> list[str]:
        return [self.getRawHand(c) for c in combo.split('-')]

    # get suit from eg 'AJhh'
    def getComboSuit(self, combo: str) -> str:
        return combo[2]

    def allGreaterCombinations(self, raw_hand: str, ceiling=None, filters={}) -> list[str]:
        [a, b] = list(raw_hand)

        c = PokerIterator(a)
        d = PokerIterator(b)
        card_only_perms = []

        (c_top, d_top) = PokerIterator.getTops(ceiling)

        while c.current() is not c_top and d.current() is not d_top:
            card_only_perms.append(c + d)
            c.next(); d.next()

        expansion = []
        for p in card_only_perms:
            expansion += self.combinations(p, **filters)

    def combinations(self, raw_hand: str, offsuit=False, suited=False, suit=None) -> list[str]:

        [top, bottom] = list(raw_hand)
        result = self.prune([top + x + bottom + y for x in SUIT_LIST for y in SUIT_LIST])

        if offsuit:
            return self.offsuit(result)
        elif suited:
            return self.suited(result, suit)
        else:
            return result

    def getFilters(self, flag, suit=None):
        result = {}
        if flag == F.OFFSUIT:
            result['offsuit'] = True
        elif flag == F.SUITED:
            result['suited'] = True
            result['suit'] = suit
        return result

    def offsuit(self, combs):
        result = []
        for c in combs:
            [a, b] = list(c)
            s1, s2 = a[1], b[1]
            if s1 != s2:
                result.append(c)
        return result

    def suited(self, combs, suit=None):
        result = []
        for c in combs:
            [a, b] = list(c)
            s1, s2 = a[1], b[1]
            if suit is not None:
                if s1 == suit and s2 == suit:
                    result.append(c)
            else:
                if s1 == s2:
                    result.append(c)
        return result

    def prune(self, perms):
        deduped = self.dedupe(perms)
        cleaned = self.clean(deduped)
        return cleaned

    def dedupe(self, perms):
        results = []
        seen = {}
        for p in perms:
            p_mirror = p[2:] + p[0:2]
            if p_mirror not in seen and p not in seen:
                results.append(p)
                seen[p] = True
                seen[p_mirror] = True
        return results

    def clean(self, deduped):
        result = []
        for v in deduped:
            if v[0:2] != v[2:]:
                result.append(v)
        return result

    def format(self, combos: list[str]) -> str:
        return ','.join(combos)