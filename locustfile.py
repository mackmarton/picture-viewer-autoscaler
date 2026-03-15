from locust import HttpUser, task, between
import uuid
import re
import os


class PhotoAlbumUser(HttpUser):
    wait_time = between(1, 5)

    def extract_csrf(self, html_text):
        match = re.search(r'name="_csrf"\s+value="([^"]+)"', html_text)
        if match:
            return match.group(1)
        return ""

    def on_start(self):
        # CSRF token kinyerése
        response = self.client.get("/")
        csrf_token = self.extract_csrf(response.text)

        # bejelentkezési adatok tokennel együtt
        self.client.post("/api/auth/login", data={
            "username": "testuser",
            "password": "password",
            "_csrf": csrf_token
        })
        self.uploaded_photo_names = []

    @task(3)
    def view_photo_list(self):
        self.client.get("/")

    @task(1)
    def upload_photo(self):
        response = self.client.get("/")
        csrf_token = self.extract_csrf(response.text)

        photo_name = 'test' + str(uuid.uuid4())

        if os.path.exists("test.jpg"):
            with open("test.jpg", "rb") as image_file:
                files = {
                    'file': ('test.jpg', image_file, 'image/jpeg')
                }
                data = {
                    'name': photo_name,
                    '_csrf': csrf_token
                }
                upload_response = self.client.post("/api/pictures", data=data, files=files)
                if upload_response.status_code == 201:
                    self.uploaded_photo_names.append(photo_name)

    @task(1)
    def delete_photo(self):
        if not self.uploaded_photo_names:
            return

        photo_name = self.uploaded_photo_names.pop(0)

        api_response = self.client.get("/api/pictures/name", params={"name": photo_name})

        if api_response.status_code == 200:
            try:
                picture_data = api_response.json()
                photo_id = picture_data.get("id")

                if photo_id:
                    page_response = self.client.get("/")
                    csrf_token = self.extract_csrf(page_response.text)

                    self.client.delete(f"/api/pictures/{photo_id}", data={"_csrf": csrf_token})
            except ValueError:
                pass