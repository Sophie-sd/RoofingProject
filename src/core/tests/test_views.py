from django.test import Client, TestCase
from django.urls import reverse


class PageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_returns_200(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '400+')
        self.assertContains(response, 'Якісні матеріали від європейських та українських виробників')
        self.assertNotContains(response, 'Сервіс та ремонт')
        self.assertNotContains(response, 'Преміальні')

    def test_services_returns_200(self):
        response = self.client.get(reverse('core:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Інструменти')
        self.assertNotContains(response, 'Сервіс та ремонт')

    def test_about_returns_200(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2005 році')
        self.assertContains(response, 'Чому обирають нас')
        self.assertNotContains(response, 'технагляд')

    def test_portfolio_returns_200(self):
        response = self.client.get(reverse('core:portfolio'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_returns_200(self):
        response = self.client.get(reverse('core:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '08:00 – 20:00')

    def test_privacy_returns_200(self):
        response = self.client.get(reverse('core:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_thank_you_returns_200(self):
        response = self.client.get(reverse('core:thank_you'))
        self.assertEqual(response.status_code, 200)


class HtmxViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_estimate_form_valid_redirects(self):
        response = self.client.post(
            reverse('core:htmx_estimate'),
            {'email': 'test@example.com'},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['HX-Redirect'], reverse('core:thank_you'))

    def test_estimate_request_form_valid_redirects(self):
        response = self.client.post(
            reverse('core:htmx_estimate_request'),
            {
                'settlement': 'Біла Церква',
                'work_type': 'new_roof',
                'area': 'up_to_100',
                'floors': '1',
                'material': 'metal_tile',
                'phone': '+380441234567',
                'source': 'home',
            },
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['HX-Redirect'], reverse('core:thank_you'))

    def test_callback_form_valid_redirects(self):
        response = self.client.post(
            reverse('core:htmx_callback'),
            {'name': 'Test User', 'phone': '+380441234567', 'message': 'Hello'},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['HX-Redirect'], reverse('core:thank_you'))

    def test_portfolio_filter_returns_partial(self):
        response = self.client.get(
            reverse('core:htmx_portfolio'),
            {'category': 'metal'},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вілла Скандинавія')

    def test_faq_toggle_returns_partial(self):
        response = self.client.get(
            reverse('core:htmx_faq_toggle', kwargs={'pk': 1}),
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'site-faq-item is-open')
