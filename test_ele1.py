from messenger import User
"""from messenger import Channels
from messenger import Messages
from messenger import LocalStorage
from messenger import RemoteStorage
from messenger import UserInterface
import pytest"""

#test de user d'abord repr marche, puis load dans local storage si fichier json et fit load, remplit bien, get user et add user apres 
def test_repr():
    u = User(70, 'Yamina')
    assert str(u) == 'user(Yamina)'



