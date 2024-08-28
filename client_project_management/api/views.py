from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.response import Response

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['projects'] = ProjectSerializer(instance.projects.all(), many=True).data
        return Response(data)

from rest_framework import status
from rest_framework.decorators import action
from .models import Project
from .serializers import ProjectCreateSerializer, ProjectDetailSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectDetailSerializer

    @action(detail=False, methods=['get'])
    def user_projects(self, request):
        projects = Project.objects.filter(users=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='clients/(?P<client_id>\d+)/projects')
    def create_client_project(self, request, client_id=None):
        client = Client.objects.get(pk=client_id)
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=request.user)
            return Response(ProjectDetailSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
