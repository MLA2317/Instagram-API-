# from django.shortcuts import render
# from .serializer import DirectGETMessageSerializer, DirectPostMessageSerializer
# from .models import DirectMessage
# from rest_framework.response import Response
# from rest_framework import status, views, generics
#
#
# class SendMessageView(generics.CreateAPIView):
#     queryset = DirectMessage.objects.all()
#     serializer_class = DirectPostMessageSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         print('ser', serializer)
#         serializer.is_valid(raise_exception=True)
#         #self.perform_create(serializer)
#         serializer.save()
#         # headers = self.get_success_headers(serializer.data)
#         # print('header', headers)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ListReceivedMessageView(generics.ListAPIView):
#     serializer_class = DirectGETMessageSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return DirectMessage.objects.filter(receiver=user)
#
#
# class ListSendMessageView(generics.ListAPIView):
#     serializer_class = DirectGETMessageSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return DirectMessage.objects.filter(sender=user)
#
#
#
# # class SendMessageAPi(views.APIView):
# #     def post(self, request, *args, **kwargs):
# #         sender = request.user
# #         data = request.data.copy()
# #         data['sender'] = sender.id
# #
# #         serializer = DirectMessageSerializer(data=data)
# #
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class RetrieveDirectMessageApi(views.APIView):
# #     def get(self, request, sender_id, *args, **kwargs):
# #         receiver = request.user
# #         message = DirectMessage.objects.filter(sender_id=sender_id, receiver=receiver)
# #         serializer = DirectMessageSerializer(message, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
#
