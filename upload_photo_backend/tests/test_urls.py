from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import ImageUploadView, ListImageView


class TestUrls(SimpleTestCase):

    def test_url_upload_photo(self):
        url = reverse("main:upload-photo")
        self.assertEqual(resolve(url).func.view_class, ImageUploadView)

    def test_url_list_photo(self):
        url = reverse("main:list-photo")
        self.assertEqual(resolve(url).func.view_class, ListImageView)
