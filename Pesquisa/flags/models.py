from django.db import models
from django.core.validators import RegexValidator


class Country(models.Model):
    """
    Model to store country information with flag support.
    """
    code = models.CharField(
        max_length=2,
        unique=True,
        validators=[RegexValidator(regex=r'^[A-Z]{2}$', message='Country code must be 2 uppercase letters')],
        help_text='ISO 3166-1 alpha-2 country code (e.g., BR, US, FR)'
    )
    name = models.CharField(
        max_length=100,
        help_text='Full country name'
    )
    flag_code = models.CharField(
        max_length=10,
        blank=True,
        help_text='Flag icon code, defaults to country code if empty'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this country should be displayed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_flag_code(self):
        """
        Return the flag code, defaulting to country code if not set.
        """
        return self.flag_code or self.code.lower()

    @property
    def flag_emoji(self):
        """
        Convert country code to flag emoji using Unicode regional indicators.
        """
        if len(self.code) == 2:
            return ''.join(chr(ord(char) + 127397) for char in self.code.upper())
        return '🏳️'  # Default flag if conversion fails
