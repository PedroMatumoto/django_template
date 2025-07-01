from django.test import TestCase, Client
from django.urls import reverse
from .models import Country


class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            code='BR',
            name='Brazil',
            flag_code='br'
        )

    def test_country_creation(self):
        """Test that country is created correctly."""
        self.assertEqual(self.country.code, 'BR')
        self.assertEqual(self.country.name, 'Brazil')
        self.assertEqual(self.country.flag_code, 'br')
        self.assertTrue(self.country.is_active)

    def test_get_flag_code(self):
        """Test get_flag_code method."""
        # With explicit flag_code
        self.assertEqual(self.country.get_flag_code(), 'br')
        
        # Without flag_code (should default to country code lowercase)
        country_no_flag = Country.objects.create(code='US', name='United States')
        self.assertEqual(country_no_flag.get_flag_code(), 'us')

    def test_flag_emoji(self):
        """Test flag emoji property."""
        emoji = self.country.flag_emoji
        self.assertIsInstance(emoji, str)
        self.assertEqual(len(emoji), 2)  # Flag emoji should be 2 characters

    def test_string_representation(self):
        """Test string representation of country."""
        self.assertEqual(str(self.country), 'Brazil (BR)')


class FlagViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.country = Country.objects.create(
            code='BR',
            name='Brazil',
            flag_code='br'
        )

    def test_examples_view(self):
        """Test examples view loads correctly."""
        response = self.client.get(reverse('flags:examples'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Flag System Examples')

    def test_countries_api(self):
        """Test countries API endpoint."""
        response = self.client.get(reverse('flags:countries_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_country_detail_view(self):
        """Test country detail view."""
        response = self.client.get(reverse('flags:country_detail', args=['BR']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brazil')

    def test_country_detail_not_found(self):
        """Test country detail view for non-existent country."""
        response = self.client.get(reverse('flags:country_detail', args=['XX']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Country Not Found')


class FlagTemplateTagsTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            code='BR',
            name='Brazil',
            flag_code='br'
        )

    def test_flag_icon_template_tag(self):
        """Test flag_icon template tag functionality."""
        from django.template import Context, Template
        
        # Test basic flag icon
        template = Template('{% load flag_tags %}{% flag_icon "BR" %}')
        rendered = template.render(Context({}))
        self.assertIn('img', rendered)
        self.assertIn('Flag of Brazil', rendered)

    def test_flag_emoji_filter(self):
        """Test flag_emoji template filter."""
        from django.template import Context, Template
        
        template = Template('{% load flag_tags %}{{ "BR"|flag_emoji }}')
        rendered = template.render(Context({}))
        self.assertIsInstance(rendered, str)
        self.assertTrue(len(rendered) >= 1)  # Should contain emoji or fallback
