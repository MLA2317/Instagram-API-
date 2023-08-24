# from django.shortcuts import render
# from .serializer import SaveSerializer
# from .models import Save
# from rest_framework import generics, status
# from rest_framework.response import Response
#
#
# class SaveListCreate(generics.ListCreateAPIView):
#     queryset = Save.objects.all()
#     serializer_class = SaveSerializer
#
#     def get_queryset(self):
#         return Save.objects.filter(account_id=self.request.user.id)
#
#
#
