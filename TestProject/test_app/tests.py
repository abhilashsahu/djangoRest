"""
Test script for the projects endpoints and their features
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class TestProjectModel(APITestCase):
    """ Class responsible for testing project API endpoints """

    def setUp(self):
        self.url = reverse('projects')
        self.project_data = {
            "id": 5000,
            "project_name": "Solar Water pump",
            "project_number": "789",
            "acquisition_date": "2023-01-01",
            "number_3l_code": "DNR",
            "project_deal_type_id": "Asset",
            "project_group_id": "RW 1",
            "project_status_id": "1 Operating",
            "company_id": 123
        }
        # self.dummy_user = User.objects.create_user("dummy_user")

    def test_create_new_project(self):
        """ Test case to call the API get project"""
        api_response = self.client.post(self.url, self.project_data)
        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED, "Project Create")

    def test_get_created_project(self):
        api_response = self.client.get(self.url)
        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
