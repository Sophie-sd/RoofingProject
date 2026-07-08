from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from core.models import EstimateRequest


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

    def test_portfolio_featured_cities_appear_first(self):
        response = self.client.get(reverse('core:portfolio'))
        content = response.content.decode()
        karpaty_pos = content.find('/portfolio/karpaty/')
        mizhrichchya_pos = content.find('/portfolio/mizhrichchya/')
        novi_pos = content.find('/portfolio/novi-petrivtsi/')
        bilogorodka_pos = content.find('/portfolio/bilogorodka/')
        self.assertNotEqual(karpaty_pos, -1)
        self.assertNotEqual(mizhrichchya_pos, -1)
        self.assertNotEqual(novi_pos, -1)
        self.assertNotEqual(bilogorodka_pos, -1)
        self.assertLess(karpaty_pos, mizhrichchya_pos)
        self.assertLess(mizhrichchya_pos, novi_pos)
        self.assertLess(novi_pos, bilogorodka_pos)

    def test_portfolio_project_returns_200(self):
        response = self.client.get(
            reverse('core:portfolio_project', kwargs={'city': 'karpaty'}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Карпати')

    def test_portfolio_project_unknown_city_returns_404(self):
        response = self.client.get(
            reverse('core:portfolio_project', kwargs={'city': 'unknown'}),
        )
        self.assertEqual(response.status_code, 404)

    def test_home_portfolio_preview_uses_home_images(self):
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, '/static/images/portfolio/home-preview/')
        self.assertContains(response, reverse('core:portfolio_project', kwargs={'city': 'karpaty'}))

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

    @patch('core.services.leads.send_lead_notification', return_value=True)
    def test_estimate_request_form_valid_redirects(self, _mock_tg):
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
        lead = EstimateRequest.objects.get()
        self.assertEqual(lead.settlement, 'Біла Церква')
        self.assertEqual(lead.phone, '+380441234567')
        self.assertEqual(lead.source, 'home')
        self.assertFalse(lead.is_processed)
        _mock_tg.assert_called_once()

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
            {'city': 'karpaty'},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse('core:portfolio_project', kwargs={'city': 'karpaty'}),
        )

    def test_faq_toggle_returns_partial(self):
        response = self.client.get(
            reverse('core:htmx_faq_toggle', kwargs={'pk': 1}),
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'site-faq-item is-open')
