import datetime

import factory
import random
from faker import Faker
import itertools
from django.contrib.auth.hashers import make_password

fake = Faker()
Faker.seed(1)

genres = list()
main = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance',
        'Thriller', 'Western', 'Sci-Fi', 'Space Travel', 'Time Travel', 'Cerebral Science',
        'Robot and Monster Films', 'Disaster and Alien Invasion', 'Classic Western',
        'The Revisionist and Anti-Western', 'Contemporary and Neo-Western',
        'Fantasy and Space Western', 'Modern Western', 'Historical Romance', 'Romantic Drama',
        'Romantic Comedy', 'Chick Flick', 'Paranormal Romance', 'Conspiracy Thriller'
        'Crime Thriller', 'Legal Thriller', 'Spy Thriller', 'Supernatural Thriller', 'Animation']
secondary = ['', 'War and Military', 'Spy and Espionage', 'Martial Arts', 'Western Shoot ‘Em Up',
             'Crime', 'Disaster', 'Psychological', 'Techno', 'Slapstick', 'Screwball', 'Parody',
             'Black', 'Zombie', 'Folk', 'Body', 'Found Footage']
factor = ['', 'censored', 'uncensored', 'original', 'colored', 'shorten', 'subbed', 'type 1',
          'type 2', 'type 3', 'type 4', 'rus', 'eng', 'jap', 'ger', 'esp', 'ita', 'ch', 'th',
          'por', 'ukr']
for genre in itertools.product(secondary, main, factor):
    genres.append((' '.join(genre)).strip())


def rand_date(a):
    return fake.date_between(start_date='-60y', end_date='now').strftime('%Y-%m-%d')


def rand_rating(a):
    return random.randrange(100)/10


def movie_path(title):
    return '/movies/%s' % (title)


def person_name(a):
    if random.random() < 0.5:
        return fake.first_name_female() + " " + fake.last_name_female()
    else:
        return fake.first_name_male() + " " + fake.last_name_male()


def filmwork_title(a):
    return fake.text(max_nb_chars=20).capitalize().strip('.')


def filmwork_description(a):
    return fake.paragraph(nb_sentences=2)


def genre(a):
    return random.choice(genres)


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person
        django_get_or_create = ('name',)

    name = factory.LazyAttribute(person_name)


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
        django_get_or_create = ('name',)

    name = factory.LazyAttribute(genre)


class FilmworkFactoryMovies(factory.django.DjangoModelFactory):
    class Meta:
        model = Filmwork
        django_get_or_create = ('title', 'creation_date')

    title = factory.LazyAttribute(filmwork_title)
    description = factory.LazyAttribute(filmwork_description)
    creation_date = factory.LazyAttribute(rand_date)
    rating = factory.LazyAttribute(rand_rating)
    age_rating = factory.Iterator(AgeRating.objects.all())
    type = 'Movie'


class FilmworkFactoryTvSeries(factory.django.DjangoModelFactory):
    class Meta:
        model = Filmwork
        django_get_or_create = ('title',)

    title = factory.LazyAttribute(filmwork_title)
    description = factory.LazyAttribute(filmwork_description)
    creation_date = factory.LazyAttribute(rand_date)
    rating = factory.LazyAttribute(rand_rating)
    age_rating = factory.Iterator(AgeRating.objects.all())
    type = 'Serial'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))
    username = factory.Sequence(lambda n: "user_%d" % n)
    password = make_password('pass123', salt=None, hasher='default')
    date_joined = factory.LazyFunction(datetime.datetime.now)
    is_staff = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class FilmworkGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filmwork
        django_get_or_create = ('title', 'creation_date')
    title = factory.Iterator(Filmwork.objects.all())

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                self.genres.add(genre)


class PersonActorRoleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PersonRole
        django_get_or_create = ('person_id', 'filmwork_id', 'role')

    filmwork = factory.SubFactory(Filmwork)
    person = factory.SubFactory(Person)
    role = factory.LazyAttribute(PersonRole.Roles.ACTOR)


def make_objects():
    PersonFactory.create_batch(size=10000)
    GenreFactory.create_batch(size=12000)
    FilmworkFactoryMovies.create_batch(size=1000000)
    FilmworkFactoryTvSeries.create_batch(size=200000)
    UserFactory.create_batch(size=2000, groups=(Group.objects.filter(name='пользователь')))
    UserFactory.create_batch(size=20, groups=(Group.objects.filter(name='content-manager')))
    FilmworkGenreFactory.create_batch(size=1300000, genres=(random.sample(list(Genre.objects.all()),
                                                                          random.randrange(1, 3))))


make_objects()
