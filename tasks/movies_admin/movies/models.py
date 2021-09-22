from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Genre(TimeStampedModel):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class AgeRating(TimeStampedModel):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('age rating')
        verbose_name_plural = _('Age ratings')

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = [
            models.Index(fields=('name',))
        ]

    def __str__(self):
        return self.name


class Filmwork(TimeStampedModel):
    class TVType(models.TextChoices):
        MOVIE = 'Movie', _('Movie')
        SERIAL = 'Serial', _('Serial')

    type = models.CharField(
        max_length=6,
        choices=TVType.choices
    )
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255, null=False, blank=False)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'))
    file_path = models.FileField(_('file location'), upload_to='film_works/', blank=True)
    rating = models.DecimalField(_('rating'),
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
                                 blank=False, decimal_places=1, max_digits=3, null=True)
    age_rating = models.ForeignKey(
        AgeRating,
        verbose_name=_("age rating"),
        related_name='film_age_rating',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        max_length=20
    )
    genres = models.ManyToManyField(Genre, blank=True)

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        constraints = [
            models.UniqueConstraint(fields=['title', 'creation_date'], name='unique title name')
        ]
        indexes = [
            models.Index(fields=('title', 'creation_date')),
        ]

    def __str__(self):
        return self.title


class PersonRole(TimeStampedModel):
    class Roles(models.TextChoices):
        DIRECTOR = 'Director', _('Director')
        ACTOR = 'Actor', _('Actor')
        WRITER = 'Writer', _('Writer')

    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='film_relation',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        max_length=20
    )
    filmwork = models.ForeignKey(
        Filmwork,
        verbose_name=_('movie'),
        related_name='film_relation',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        max_length=20
    )

    role = models.CharField(
        max_length=8,
        choices=Roles.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['filmwork', 'person', 'role'], name='unique person role for movie')
        ]
        indexes = [
            models.Index(fields=('filmwork',)),
            models.Index(fields=('person',)),
        ]
        verbose_name = _('relation')
        verbose_name_plural = _('relations')
