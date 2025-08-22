from django.conf import settings
from django.forms.models import ModelForm
from django.template.context_processors import media

from .models import UserLike, User, Admin, Content
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from DjangoVue.settings import MEDIA_ROOT

# Create your views here.

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self):
        super().__init__()
        for name, field in self.fields.items():
            field.widget.attrs = { "class": 'form-control' }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class RegisterServe(APIView):
    def post(self, request):
        # 提交数据
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            is_exist = User.objects.filter(user_name=request.data['user_name'])
            if is_exist:
                return Response('用户已存在,再想一个吧', status=400)
            serializer.save()
            return Response('注册成功', status=200)
        return Response('用户或密码不能为空', status=400)


class UserServe(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            is_true = User.objects.filter(**request.data)
            if not is_true:
                return Response('用户或密码错误', status=400)
            return Response('登录成功, 欢迎%s'%request.data['user_name'], status=200)
        return Response('用户或密码不能为空', status=400)

    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)


class AdminServe(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            is_true = Admin.objects.filter(**request.data)
            if not is_true:
                return Response('管理员名或密码错误', status=400)
            return Response('登录成功, 欢迎%s'%request.data['admin_name'], status=200)
        return Response('名称或密码不能为空', status=400)


class ContentServe(APIView):
    def get(self, request):
        data = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('发布成功', status=200)
        return Response('发布对象不符合规范', status=400)

    def delete(self, request):
        Content.objects.filter(id=request.data['id']).delete()
        return Response({'message': '删除成功'}, status=200)


class Viewed(APIView):
    def post(self, request):
        views = request.data['views'] + 1
        Content.objects.filter(id=request.data['id']).update(views=views)
        return Response({'message': '预览成功'}, status=200)


class AddFocus(APIView):
    def post(self, request):
        the_user = User.objects.get(user_name=request.data['user']).focus or []
        if the_user:
            if request.data['focus'] in the_user:
                return Response({'message': '你已关注此作者'}, status=400)
        the_user.append(request.data['focus'])
        User.objects.filter(user_name=request.data['user']).update(focus=the_user)
        return Response({'message': '关注成功'}, status=200)


class WhoFocusMe(APIView):
    def post(self, request):
        user_list = User.objects.all()
        the_user = request.data['user_name']
        who_focus = []
        for user in user_list:
            focus_object = {}
            if user.focus:
                if the_user in user.focus:
                    focus_object['user_name'] = user.user_name
                    if user.portrait:
                        focus_object['portrait'] = user.portrait
                    who_focus.append(focus_object)
        return Response({'message': '请求成功', 'data': who_focus}, status=200)


class EditInfo(APIView):
    def post(self, request):
        if 'newname' in request.data:
            User.objects.filter(user_name=request.data['user']).update(user_name=request.data['newname'])
        if 'profile' in request.data:
            User.objects.filter(user_name=request.data['user']).update(profile=request.data['profile'])
        if 'newPwd' in request.data:
            User.objects.filter(user_name=request.data['user']).update(user_password=request.data['newPwd'])
        if 'portrait' in request.data:
            user = User.objects.get(user_name=request.data['user'])
            user.portrait = request.FILES.get('portrait')
            user.save()
        return Response('修改成功', status=200)