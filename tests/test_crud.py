from models.db_models import UserDB, AudioCollectionDB



def test_create_user():
    user = UserDB(nickname='user', email='test@test.com', hashed_password='password')
    assert user.nickname == 'user'
    assert user.email == 'test@test.com'
    assert user.hashed_password == 'password'


def test_add_collectable():
    item = AudioCollectionDB(artist='King Crimson', audio_format='Vinyl', album='Red', year=1979, grade='mint')
    assert item.artist == 'King Crimson'
    assert item.audio_format == 'Vinyl'
    assert item.album == 'Red'
    assert item.year == 1979
    assert item.grade == 'mint'
