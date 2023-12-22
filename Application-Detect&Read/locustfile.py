from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  

    @task
    def kyc_request(self):
        endpoint = "/kyc_v2"  
        files = {'recto_image': ('293.jpg', open('C:/Users/rimba/Desktop/293.jpg', 'rb'))}
        response = self.client.post(endpoint, files=files)
        assert response.status_code == 200








