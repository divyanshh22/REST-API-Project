from django.shortcuts import render


# These views are deliberately thin. They pick a template and hand it over -
# all the real work happens in the API layer under /apis/. Keeping the two apart
# means the JSON endpoints stay reusable even if you later replace these pages
# with a React or mobile app.

def homeView(request):
    return render(request, 'render/home.html')


def aboutView(request):
    return render(request, 'render/about.html')


def addStudentView(request):
    return render(request, 'render/add_students.html')


def updateStudentView(request):
    return render(request, 'render/update_students.html')


def partialUpdateView(request):
    return render(request, 'render/partial_update.html')


def deleteStudentView(request):
    return render(request, 'render/delete_students.html')
