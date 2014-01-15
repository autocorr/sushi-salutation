#!/usr/bin/env python
# encoding: utf-8

import random
import string


__all__ = ['SushiSalutation']

FOOD_FILEN = 'food_types.txt'
RECIP_FILEN = 'recipients.txt'


class NoMatchError(Exception):
    def __init__(self):
        pass


class Items(object):
    def __init__(self, filen):
        self.filen = filen
        self._get_entries()

    def _get_entries(self):
        with open(self.filen, 'r') as handle:
            self.entries = self._clean_lines(handle)
        self.valid_start_letters = set(s[0] for s in self.entries)

    @staticmethod
    def _clean_lines(handle):
        # strip new line characters
        entries = [s.strip() for s in handle.readlines()]
        # remove empty lines
        entries = filter(None, entries)
        return entries

    def select_on_letter(self, letter):
        assert letter in string.ascii_lowercase
        if letter not in self.valid_start_letters:
            raise NoMatchError
        return [s for s in self.entries if s.startswith(letter)]


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

    def __init__(self, lines):
        """
        Parameters
        ----------
        lines : number
            Number of salutations to print
        """
        self.lines = lines
        self.saluts = []

    @staticmethod
    def _get_rand_letter():
        return random.choice(string.ascii_lowercase)

    def get_saluts(self):
        if self.saluts:
            self.saluts = []
        while len(self.saluts) < self.lines:
            try:
                letter = self._get_rand_letter()
                l_foods = self.foods.select_on_letter(letter=letter)
                l_recip = self.recips.select_on_letter(letter=letter)
            except NoMatchError:
                pass
            else:
                food = random.choice(l_foods)
                recip = random.choice(l_recip)
                salut = '-'.join([food, recip])
                self.saluts.append(salut)
        return self.saluts


def get_sushi_salutations(lines):
    ss = SushiSalutation(lines=lines)
    return ss.get_saluts()


