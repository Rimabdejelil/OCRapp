import unittest
from app import app

class TestYourApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass  

    def test_kyc_endpoint_with_valid_images(self):
        recto_image_path = 'C:/Users/rimba/Desktop/293.jpg'

        recto_image_data = {'recto_image': (open(recto_image_path, 'rb'), 'recto.jpg')}
        response = self.app.post('/kyc_v2', data=recto_image_data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)

    def test_kyc_endpoint_with_invalid_images(self):
        response = self.app.post('/kyc_v2')

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()


