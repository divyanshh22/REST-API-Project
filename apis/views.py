from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from render.models import Students
from .serializers import StudentSerializers


# The @api_view decorator does two jobs here. It turns a plain function into a
# real DRF endpoint, and it also acts as a bouncer - any method we did not list
# gets a 405 back instead of quietly running the wrong code.
@api_view(['GET', 'POST'])
def studentListView(request):
    # GET and POST deliberately share this single URL. That is the usual REST
    # layout, so the frontend only has to remember "/apis/" and not remember a
    # second "/apis/create/" path as well.
    if request.method == 'POST':
        # data=request.data hands the incoming JSON to the serializer so it can
        # be checked. Nothing touches the database until is_valid() passes.
        serializer = StudentSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # 201 ("Created") is the honest status code when a new row appears,
            # not 200. We send the saved record back so the caller gets the id
            # that the database just generated.
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 400 means the client sent something we cannot accept. serializer.errors
        # looks like {"student_email": ["Enter a valid email address."]}, and the
        # frontend drops each message under its matching input field.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # The read side is three lines: grab the rows, convert them, return them.
    serializer = StudentSerializers(Students.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def studentDetailView(request, pk):
    # get_object_or_404 saves us writing a try/except. If no row has this id we
    # get a clean 404 ("no such student") rather than an ugly crash.
    student = get_object_or_404(Students, pk=pk)
    serializer = StudentSerializers(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def studentUpdateView(request, pk):
    student = get_object_or_404(Students, pk=pk)

    # No partial=True here, and that is the whole point of PUT. Every field is
    # treated as required, so a client that forgets the email gets a 400 rather
    # than silently wiping the value.
    serializer = StudentSerializers(student, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def studentPartialUpdateView(request, pk):
    student = get_object_or_404(Students, pk=pk)

    # partial=True is the only difference from the PUT above. It tells the
    # serializer to only demand the keys that were actually sent, so the client
    # can change one field and leave everything else untouched.
    serializer = StudentSerializers(student, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def studentDeleteView(request, pk):
    student = get_object_or_404(Students, pk=pk)
    student.delete()

    # 204 means "done, and there is nothing to send back". The record is gone,
    # so returning its old contents would only be confusing.
    return Response(status=status.HTTP_204_NO_CONTENT)
