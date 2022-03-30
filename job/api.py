from job.models import Job
from job.serializers import JobSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response


## class based view

class JobListApi(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class JobDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = 'id'
    permission_classes = [DjangoModelPermissions]


'''
## functions based views
@api_view(['GET'])
def job_list_api(request):
    all_jobs = Job.objects.all()
    data = JobSerializer(all_jobs, many=True).data
    return Response({'data': data})


@api_view(['GET'])
def job_detail_api(request, id):
    job_detail = Job.objects.get(id=id)
    data = JobSerializer(job_detail).data
    return Response({'data': data})
'''
