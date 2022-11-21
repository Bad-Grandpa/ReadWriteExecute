from random import sample, choice

from ..models import FlashCard

def add_two_random_fcs(include_pk):
    '''
    Function expects pk that needs to be included.
    It chooses randomly three FlashCards - if the one with the required pk isn't
    among them, it adds it at random position.
    '''
    pks = list(FlashCard.objects.values_list('pk', flat=True))
    random_pks = sample(pks, 3)

    if not include_pk in random_pks:
        random_pks[choice(range(3))] = include_pk

    return tuple(random_pks)
