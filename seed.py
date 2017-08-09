from person import Person, PeopleRepo
from borrowal import Borrowal, BorrowalRepo

piti = Person(None, 'Piti', True)
pam = Person(None, 'Pam', True)
lookyee = Person(None, 'Lookyee', False)
ply = Person(None, 'Ply', True)
france = Person(None, 'France', True)
nice = Person(None, 'Nice', False)


def seed_people():
    PeopleRepo.add(piti)
    PeopleRepo.add(pam)
    PeopleRepo.add(lookyee)
    PeopleRepo.add(ply)
    PeopleRepo.add(france)
    PeopleRepo.add(nice)


def seed_borrowal():
    BorrowalRepo.create_transaction(piti, pam, 100, 'ramen')
    BorrowalRepo.create_transaction(piti, lookyee, 200, 'fish ball')
    BorrowalRepo.create_transaction(pam, piti, 300, 'BBQ Plaza')
    BorrowalRepo.create_transaction(pam, lookyee, 50, 'Sushi')


def test():
    piti_lend_pam = BorrowalRepo.summarize_debt(piti, pam)
    print piti_lend_pam
    assert(piti_lend_pam == -200)


if __name__ == '__main__':
    PeopleRepo.delete_table()
    BorrowalRepo.delete_table()
    seed_people()
    seed_borrowal()
    test()
