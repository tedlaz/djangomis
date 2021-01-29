from django.test import TestCase
from . import apd_functions as apdf


class ApdfTest(TestCase):
    def test_01(self):
        self.assertEqual(apdf.fill_spaces('TED', 5), 'TED  ')

    def test_02(self):
        self.assertRaises(ValueError, apdf.fill_spaces, 'TEDD', 3)

    def test_03(self):
        self.assertEqual(apdf.fill_spaces('', 5), '     ')
