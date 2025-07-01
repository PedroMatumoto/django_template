# Django Flag System Documentation

## Overview

This Django flag system provides comprehensive functionality for displaying country flags in your Django applications. It supports both CDN-based flag images and emoji fallbacks, with a flexible template tag system and admin interface for managing countries.

## Features

- **Country Model**: Store countries with ISO codes, names, and flag codes
- **Template Tags**: Easy-to-use template tags for displaying flags
- **CDN Integration**: Support for external flag icon CDNs with fallback
- **Emoji Fallback**: Unicode flag emojis when CDN is unavailable
- **Admin Interface**: Django admin integration for managing countries
- **Management Command**: Command to populate initial country data
- **Responsive Design**: CSS for responsive flag display
- **API Endpoints**: JSON API for country data

## Installation

1. Add `'flags'` to your `INSTALLED_APPS` in `settings.py`
2. Run migrations: `python manage.py migrate`
3. Populate countries: `python manage.py populate_countries`
4. Include URLs in your main `urls.py`: `path('flags/', include('flags.urls'))`

## Settings

Add these optional settings to your `settings.py`:

```python
# Flag System Configuration
FLAG_USE_CDN = True  # Use CDN for flag images
FLAG_CDN_URL = 'https://flagicons.lipis.dev/flags/4x3/{code}.svg'  # CDN URL pattern
FLAG_DEFAULT_SIZE = '24'  # Default flag size in pixels
FLAG_CACHE_TIMEOUT = 3600  # Cache timeout in seconds
```

## Template Tags

### Loading the Template Tags

```django
{% load flag_tags %}
```

### flag_icon

Display a flag icon for a country:

```django
{% flag_icon 'BR' %}
{% flag_icon 'US' size='32' %}
{% flag_icon 'FR' size='48' style='border-radius: 4px;' %}
{% flag_icon 'DE' css_class='flag-icon-bordered' %}
{% flag_icon 'XX' fallback_emoji=False %}
```

Parameters:
- `country_code`: ISO 3166-1 alpha-2 country code (required)
- `size`: Icon size in pixels (default: 24)
- `style`: Additional CSS styles
- `css_class`: CSS classes to add
- `fallback_emoji`: Whether to show emoji as fallback (default: True)

### flag_emoji Filter

Convert country code to flag emoji:

```django
{{ 'BR'|flag_emoji }}  → 🇧🇷
{{ 'US'|flag_emoji }}  → 🇺🇸
```

### country_flag_list

Get a list of countries:

```django
{% country_flag_list as countries %}
{% country_flag_list active_only=False as all_countries %}
{% country_flag_list limit=10 as top_countries %}

{% for country in countries %}
    {% flag_icon country.code %} {{ country.name }}
{% endfor %}
```

### country_selector

Display a country dropdown selector:

```django
{% country_selector %}
{% country_selector selected_code='BR' name='user_country' %}
{% country_selector css_class='form-control' required=True %}
```

## Model API

### Country Model

```python
from flags.models import Country

# Get a country
country = Country.objects.get(code='BR')

# Country properties
country.code          # 'BR'
country.name          # 'Brazil'
country.flag_code     # 'br'
country.is_active     # True
country.flag_emoji    # '🇧🇷'

# Methods
country.get_flag_code()  # Returns flag_code or defaults to code.lower()
str(country)             # 'Brazil (BR)'
```

## Management Commands

### populate_countries

Populate the database with common countries:

```bash
# Add countries
python manage.py populate_countries

# Clear existing and add countries
python manage.py populate_countries --clear
```

## API Endpoints

### Countries API

Get all active countries as JSON:

```
GET /flags/api/countries/
```

Returns:
```json
[
    {"code": "BR", "name": "Brazil", "flag_code": "br"},
    {"code": "US", "name": "United States", "flag_code": "us"},
    ...
]
```

## CSS Classes

The system includes several CSS classes for styling flags:

- `.flag-icon`: Base flag icon class
- `.flag-emoji`: Emoji flag class
- `.flag-small`: 16px flags
- `.flag-medium`: 24px flags
- `.flag-large`: 32px flags
- `.flag-xlarge`: 48px flags
- `.flag-rounded`: Rounded flags
- `.flag-bordered`: Flags with border
- `.flag-shadow`: Flags with shadow
- `.flag-grayscale`: Grayscale flags

## Usage Examples

### Basic Flag Display

```django
{% load flag_tags %}

<!-- Simple flag -->
{% flag_icon 'BR' %} Brazil

<!-- Large flag with custom style -->
{% flag_icon 'US' size='48' style='border-radius: 8px;' %} United States

<!-- Multiple sizes -->
{% flag_icon 'FR' size='16' %} Small
{% flag_icon 'FR' size='24' %} Medium
{% flag_icon 'FR' size='32' %} Large
```

### Country List

```django
{% load flag_tags %}

<h2>Countries</h2>
{% country_flag_list as countries %}
<ul>
    {% for country in countries %}
        <li>
            {% flag_icon country.code %} 
            <a href="{% url 'flags:country_detail' country.code %}">
                {{ country.name }}
            </a>
        </li>
    {% endfor %}
</ul>
```

### Form with Country Selector

```django
{% load flag_tags %}

<form method="post">
    {% csrf_token %}
    <label for="country">Select Country:</label>
    {% country_selector name='country' css_class='form-control' required=True %}
    <button type="submit">Submit</button>
</form>
```

### Handling Unknown Countries

```django
<!-- With emoji fallback (default) -->
{% flag_icon 'XX' %}  <!-- Shows 🏳️ if country not found -->

<!-- Without fallback -->
{% flag_icon 'XX' fallback_emoji=False %}  <!-- Shows nothing if CDN fails -->
```

## Admin Interface

The flag system includes a Django admin interface for managing countries:

1. Go to `/admin/flags/country/`
2. Add, edit, or delete countries
3. View flag emojis in the list view
4. Filter by active status
5. Search by name, code, or flag code

## Troubleshooting

### Flags Not Displaying

1. Check internet connection for CDN flags
2. Verify `FLAG_USE_CDN` setting
3. Check browser console for errors
4. Ensure country exists in database

### Template Tag Errors

1. Make sure `{% load flag_tags %}` is at the top
2. Check country code format (2 uppercase letters)
3. Verify the flags app is in `INSTALLED_APPS`

### Emoji Not Showing

1. Check browser/OS emoji support
2. Verify Unicode flag emoji support
3. Use CDN flags as alternative

## Performance Considerations

- CDN flags are cached by browsers
- Database queries are optimized with indexing
- Use `limit` parameter for large country lists
- Consider caching for high-traffic sites

## Security

- Country codes are validated (2 uppercase letters)
- HTML output is properly escaped
- CDN URLs are configurable
- No user input directly in database queries