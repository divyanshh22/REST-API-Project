from rest_framework import serializers
from render.models import Students


# ModelSerializer saves us from spelling out every field by hand. It reads the
# model and works out the field types on its own - IntegerField turns into a
# "must be a number" check, EmailField into email validation, and so on. So the
# validation you saw working in the API is coming for free from the model.
class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Students

        # '__all__' simply means "every field on the model". If you would rather
        # be explicit and see what is exposed, list them out line by line
        # instead - useful once you want to hide a field such as an internal note.
        fields = '__all__'
