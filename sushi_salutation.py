#!/usr/bin/env python
# encoding: utf-8

import random
import string
from collections import OrderedDict


__all__ = ['SushiSalutation']

FOOD_FILEN = 'food_types.txt'
RECIP_FILEN = 'recipients.txt'


class NoMatchError(Exception):
    pass


class Items(object):
    def __init__(self, filen):
        self.filen = filen
        self._get_entries()

    def _get_entries(self):
        with open(self.filen, 'r') as handle:
            self.entries = self._clean_lines(handle)
        self.valid_start_chars = set(c[0] for c in self.entries)

    @staticmethod
    def _clean_lines(handle):
        # strip new line characters
        entries = [c.strip() for c in handle.readlines()]
        # remove empty lines
        entries = filter(None, entries)
        return entries

    def select_on_char(self, char):
        assert char in string.ascii_lowercase
        if char not in self.valid_start_chars:
            raise NoMatchError
        return [c for c in self.entries if c.startswith(char)]


class SushiSalutation(object):
    """
    Randomly choose sushi related salutations.

    Attributes
    ----------
    foods : Items
    recips : Items
    saluts : list
        Salutations after `get_saluts` has been run

    Example
    -------
    >>> sushi = SushiSalutation(lines=5)
    >>> sushi.get_saluts()
    """
    foods = Items(filen=FOOD_FILEN)
    recips = Items(filen=RECIP_FILEN)
    valid_chars = list(foods.valid_start_chars.union(recips.valid_start_chars))

    def __init__(self, lines):
        """
        Parameters
        ----------
        lines : number
            Number of salutations to print
        """
        self.lines = lines
        self.saluts = []

    def _get_rand_char(self):
        return random.choice(self.valid_chars)

    def get_saluts(self, letter=None):
        """
        Parameters
        ----------
        letter : string, default None
            Lower-case letter to select combinations. If `None` then
            a random letter is chosen for each combination.
        """
        if self.saluts:
            self.saluts = []
        while len(self.saluts) < self.lines:
            try:
                if letter is None:
                    letter = self._get_rand_char()
                l_foods = self.foods.select_on_char(char=letter)
                l_recip = self.recips.select_on_char(char=letter)
            except NoMatchError:
                pass
            else:
                food = random.choice(l_foods)
                recip = random.choice(l_recip)
                salut = '-'.join([food, recip])
                self.saluts.append(salut)
        return self.saluts

    def calc_combs(self, per_letter=False):
        """
        Parameters
        ----------
        per_letter : bool
            Print combinations per letter?

        Attributes
        ----------
        combos : OrderedDict
        total_combos : number
        """
        combos = OrderedDict()
        for char in self.foods.valid_start_chars:
            if char in self.recips.valid_start_chars:
                char_combo = len(self.foods.select_on_char(char)) * \
                               len(self.recips.select_on_char(char))
                combos[char] = char_combo
        self.combos = combos
        self.total_combos = sum(combos.values())
        if per_letter:
            for char, counts in combos.items():
                print '{0}: {1}'.format(char, counts)
        print 'Total number of combinations: {0}'.format(self.total_combos)


def get_sushi_salutations(lines):
    ss = SushiSalutation(lines=lines)
    return ss.get_saluts()


