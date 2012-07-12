from django.contrib.auth import authenticate
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, BasicAuthentication
from ads.models import Ad, AdImage
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseBadRequest

#these imports for Base64FileField class
import base64
import os
from tastypie.fields import FileField
from django.core.files.uploadedfile import SimpleUploadedFile

# su dung phuong phap HTTP AUTHENTICATION BASIC

class MyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        #neu chi doc thi khong yeu cau authentication
        if request.method == 'GET':
            return True
        #Cac phuong thuc khac 'GET' thi yeu cau authentication
        if not request.META.get('HTTP_AUTHORIZATION'):
            return False

        try:
            data = request.META['HTTP_AUTHORIZATION']
            user_pass = base64.b64decode(data)
        except:
            return False

        bits = user_pass.split(':', 1)
        if len(bits) != 2:
            return False
        #Su dung ham authenticate cua model Auth de kiem tra username/password
        user = authenticate(username=bits[0], password=bits[1])
        if user is None:
            return False
        request.user = user
        return True


class MyAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True
    """
    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user__username=request.user.username)

        return object_list.none()
    """
class Base64FileField(FileField):
    """
    A django-tastypie field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    Usage:

    class MyResource(ModelResource):
        file_field = Base64FileField("file_field")

        class Meta:
            queryset = ModelWithFileField.objects.all()

    In the case of multipart for submission, it would also pass the filename.
    By using a raw post data stream, we have to pass the filename within our
    file_field structure:

    file_field = {
        "name": "myfile.png",
        "file": "longbas64encodedstring",
        "content_type": "image/png" # on hydrate optional
    }
    """
    def dehydrate(self, bundle):
        if not bundle.data.has_key(self.instance_name) and hasattr(bundle.obj, self.instance_name):
            file_field = getattr(bundle.obj, self.instance_name)
            if file_field:
                try:
                    content_type, encoding = mimetypes.guess_type(file_field.file.name)
                    b64 = open(file_field.file.name, "rb").read().encode("base64")
                    ret = {
                        "name": os.path.basename(file_field.file.name),
                        "file": b64,
                        "content-type": content_type or "application/octet-stream"
                    }
                    return ret
                except:
                    pass
        return None

    def hydrate(self, obj):
        value = super(FileField, self).hydrate(obj)
        if value:
            value = SimpleUploadedFile(value["name"], base64.b64decode(value["file"]), getattr(value, "content_type", "application/octet-stream"))
        return value

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class AdResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = Ad.objects.all()
        resource_name = "ad"

        authentication = MyAuthentication()
        authorization = MyAuthorization()

class AdImageResource(ModelResource):
    file_field = Base64FileField("file_field")
    ad = fields.ForeignKey(AdResource, 'ad')
    class Meta:
        queryset = AdImage.objects.all()
        resource_name = "AdImage"

        authorization = Authorization()


class RegisterResource(ModelResource):
    class Meta:
        allowed_methods = ['post']
        object_class = User
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username']
    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(RegisterResource, self).obj_create(bundle, request, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise HttpResponseBadRequest('That username already exists')
        return bundle