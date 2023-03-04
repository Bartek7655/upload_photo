import io

from django.test import TestCase, Client
from django.urls import reverse
from PIL import Image as ImagePIL

from main.models import User, TypeAccount, BinaryImage


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.enterprise = TypeAccount.objects.get(id=3)
        self.user = User.objects.create_user(
            username="user",
            password="password",
            email="email@email.com",
            type_account=self.enterprise
        )
        self.upload_image_url = reverse("main:upload-photo")
        self.list_image_url = reverse("main:list-photo")

    @staticmethod
    def create_photo_file():
        file = io.BytesIO()
        photo = ImagePIL.new("RGB", size=(100, 100), color=(155, 0, 0))
        photo.save(file, 'jpeg')
        file.name = "test.jpeg"
        file.seek(0)
        return file

    def create_extra_user(self):
        user = User.objects.create_user(
            username='user1',
            password='password',
            email='email1@email@com',
            type_account=self.enterprise
        )
        return user

    def create_photo(self, user, expiring_time=0):
        self.client.login(username=user.username, password="password")
        photo = self.create_photo_file()

        data = {"photo": photo}
        if expiring_time:
            data["expiring_time"] = expiring_time

        response = self.client.post(
            self.upload_image_url,
            data
        )
        self.client.logout()
        return response

    def test_image_upload_view_success(self):
        response = self.create_photo(self.user)

        self.assertEqual(response.status_code, 201)

    def test_image_upload_view_inclusive_binary_link_success(self):
        response = self.create_photo(self.user, 300)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BinaryImage.objects.count(), 1)

    def test_image_upload_view_inclusive_binary_link_fail(self):
        response = self.create_photo(self.user, 299)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(BinaryImage.objects.count(), 0)

    def test_list_image_view_success(self):
        extra_user = self.create_extra_user()
        self.create_photo(extra_user)
        self.create_photo(self.user)
        self.create_photo(self.user)

        self.client.login(username="user", password="password")
        response = self.client.get(self.list_image_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
