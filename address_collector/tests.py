from django.test import TestCase
from django.test import Client
from django.test import override_settings


class AddressTestCase(TestCase):

    @override_settings(GOOGLE_FUSION_TABLE_ID='14GFO4o2zzdhGg0NR-rGtliVAQoHD9IdHrjWa3P2O')
    def setUp(self):
        self.client = Client()
        self.resp = self.client.post('/api/v1/addresses/', {
            "address": "220KV Grid Station NTDCL Nishatabad Faisalabad, Nishatabad Bridge, Faisalabad, Pakistan",
            "latitude": "31.449899868379656",
            "longitude": "73.1195068359375"
        })

    @override_settings(GOOGLE_FUSION_TABLE_ID='14GFO4o2zzdhGg0NR-rGtliVAQoHD9IdHrjWa3P2O')
    def test_create_address(self):
        """Address, Latitude and Longitude are saved to DB and FusionTable"""
        self.assertEquals(201, self.resp.status_code)
        self.assertEquals('application/json', self.resp.get('Content-Type'))
        self.assertIn('"latitude":31.449899868379656', str(self.resp.content))
        self.assertIn('"latitude":31.449899868379656', str(self.resp.content))

    @override_settings(GOOGLE_FUSION_TABLE_ID='14GFO4o2zzdhGg0NR-rGtliVAQoHD9IdHrjWa3P2O')
    def test_get_addresses(self):
        """List of addresses are retireved from database"""
        self.client.post('/api/v1/addresses/', {
            "address": "Lahore, Nishatabad Bridge, Town, Pakistan",
            "latitude": "22.449894379656",
            "longitude": "73.1195068359375"
        })
        response = self.client.get('/api/v1/addresses/')
        json = response.json()
        self.assertEquals(200, response.status_code)
        self.assertEquals('application/json', response.get('Content-Type'))
        self.assertEquals(len(json), 2)

    @override_settings(GOOGLE_FUSION_TABLE_ID='14GFO4o2zzdhGg0NR-rGtliVAQoHD9IdHrjWa3P2O')
    def test_delete_addresses(self):
        """Database and fusiontable are cleared"""
        response = self.client.delete('/api/v1/addresses/')
        json = response.json()
        self.assertEquals(205, response.status_code)
        self.assertEquals('application/json', response.get('Content-Type'))
        self.assertEquals(len(json), 0)

    @override_settings(GOOGLE_FUSION_TABLE_ID='14GFO4o2zzdhGg0NR-rGtliVAQoHD9IdHrjWa3P2O')
    def tearDown(self):
        self.client.delete('/api/v1/addresses/')
