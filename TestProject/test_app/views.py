
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache

from .models import Project
from .serializers import ProjectSerializer


class ProjectAPIView(APIView):
    """ Class to handle .../projects/ endpoint GET and POST requests """

    @staticmethod
    def get(request):
        """ Returns all the projects from Model """

        all_projects = cache.get('projects', None)  # Get projects from cache
        if all_projects is None:
            projects = Project.objects.filter(is_deleted=False)
            serializer = ProjectSerializer(projects, many=True)
            all_projects = serializer.data
            cache.set('projects', all_projects)  # Set projects to cache
        return Response(all_projects)

    @staticmethod
    def post(request):
        """ Method to create new project in the DB  """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('projects')  # Delete projects cache
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailsView(APIView):
    """ Class to handle .../project/<id> endpoint POST and DELETE requests"""

    @staticmethod
    def get_object(project_id):
        """ Method to return project record from the Model """
        return Project.objects.get(id=project_id, is_deleted=False)

    def get(self, request, project_id):
        """ Method to return project details from the DB """
        try:
            project = self.get_object(project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, project_id):
        """ Method to update project record in the DB """
        try:
            project = self.get_object(project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('projects')  # Delete projects cache
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        """ Method to delete project from the DB """
        try:
            project = self.get_object(project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project.soft_delete()
        cache.delete('projects')  # Delete projects cache
        return Response(status=status.HTTP_204_NO_CONTENT)
