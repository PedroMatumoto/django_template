from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from ..models import Country

register = template.Library()


@register.simple_tag
def flag_icon(country_code, size='24', style='', css_class='', fallback_emoji=True):
    """
    Display a flag icon for the given country code.
    
    Usage:
        {% flag_icon 'BR' %}
        {% flag_icon 'US' size='32' %}
        {% flag_icon 'FR' size='48' style='border-radius: 4px;' %}
        {% flag_icon 'DE' css_class='flag-icon' %}
        {% flag_icon 'XX' fallback_emoji=False %}
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code
        size: Icon size in pixels (default: 24)
        style: Additional CSS styles
        css_class: CSS classes to add to the flag
        fallback_emoji: Whether to show emoji flag as fallback (default: True)
    """
    if not country_code:
        return ''
    
    country_code = country_code.upper()
    
    try:
        country = Country.objects.get(code=country_code, is_active=True)
        flag_code = country.get_flag_code()
        country_name = country.name
    except Country.DoesNotExist:
        flag_code = country_code.lower()
        country_name = country_code
    
    # Get flag settings
    flag_cdn_url = getattr(settings, 'FLAG_CDN_URL', 'https://flagicons.lipis.dev/flags/4x3/{code}.svg')
    flag_use_cdn = getattr(settings, 'FLAG_USE_CDN', True)
    
    # Build CSS classes
    classes = ['flag-icon']
    if css_class:
        classes.extend(css_class.split())
    
    # Build inline styles
    styles = [f'width: {size}px', f'height: {size}px']
    if style:
        styles.append(style)
    
    if flag_use_cdn:
        # Use CDN flag image
        flag_url = flag_cdn_url.format(code=flag_code)
        
        html = format_html(
            '<img class="{classes}" src="{url}" alt="{alt}" title="{title}" style="{styles}" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'inline-block\';">',
            classes=' '.join(classes),
            url=flag_url,
            alt=f'Flag of {country_name}',
            title=f'Flag of {country_name}',
            styles='; '.join(styles)
        )
        
        # Add emoji fallback if enabled
        if fallback_emoji:
            try:
                emoji_flag = Country.objects.get(code=country_code).flag_emoji
            except Country.DoesNotExist:
                # Generate emoji flag for unknown countries
                if len(country_code) == 2:
                    emoji_flag = ''.join(chr(ord(char) + 127397) for char in country_code.upper())
                else:
                    emoji_flag = '🏳️'
            
            html += format_html(
                '<span class="{classes}" style="display: none; {styles}" title="{title}">{emoji}</span>',
                classes=' '.join(classes + ['flag-emoji']),
                styles='; '.join(styles + ['font-size: {0}px'.format(size)]),
                title=f'Flag of {country_name}',
                emoji=emoji_flag
            )
        
        return mark_safe(html)
    else:
        # Use emoji flag only
        if fallback_emoji:
            try:
                emoji_flag = Country.objects.get(code=country_code).flag_emoji
            except Country.DoesNotExist:
                if len(country_code) == 2:
                    emoji_flag = ''.join(chr(ord(char) + 127397) for char in country_code.upper())
                else:
                    emoji_flag = '🏳️'
            
            return format_html(
                '<span class="{classes}" style="{styles}" title="{title}">{emoji}</span>',
                classes=' '.join(classes + ['flag-emoji']),
                styles='; '.join(styles + ['font-size: {0}px'.format(size)]),
                title=f'Flag of {country_name}',
                emoji=emoji_flag
            )
        
        return ''


@register.simple_tag
def country_flag_list(active_only=True, limit=None):
    """
    Get a list of countries with their flags.
    
    Usage:
        {% country_flag_list as countries %}
        {% country_flag_list active_only=False as all_countries %}
        {% country_flag_list limit=10 as top_countries %}
    """
    queryset = Country.objects.all()
    
    if active_only:
        queryset = queryset.filter(is_active=True)
    
    if limit:
        queryset = queryset[:limit]
    
    return queryset


@register.filter
def flag_emoji(country_code):
    """
    Convert country code to flag emoji.
    
    Usage:
        {{ 'BR'|flag_emoji }}
    """
    if not country_code or len(country_code) != 2:
        return '🏳️'
    
    try:
        country = Country.objects.get(code=country_code.upper())
        return country.flag_emoji
    except Country.DoesNotExist:
        # Generate emoji flag for unknown countries
        return ''.join(chr(ord(char) + 127397) for char in country_code.upper())


@register.inclusion_tag('flags/country_selector.html')
def country_selector(selected_code='', name='country', css_class='', required=False):
    """
    Render a country selector dropdown with flags.
    
    Usage:
        {% country_selector %}
        {% country_selector selected_code='BR' name='user_country' %}
        {% country_selector css_class='form-control' required=True %}
    """
    countries = Country.objects.filter(is_active=True).order_by('name')
    
    return {
        'countries': countries,
        'selected_code': selected_code,
        'name': name,
        'css_class': css_class,
        'required': required,
    }