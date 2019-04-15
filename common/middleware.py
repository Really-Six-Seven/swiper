from django.utils.deprecation import MiddlewareMixin
from user.models import User
from lib.render_json import render_json
from common import errors

class AuthMiddleware(MiddlewareMixin):
    URL_WHITE_LIST=['/user/api/submit_phone',
                    '/user/api/submit_vcode',
                    ]

    def process_request(self,request):

        if request.path in self.URL_WHITE_LIST:
            return
        uid=request.session.get('uid')
        if not uid:
            return render_json("user not login",errors.USER_NOT_LOGIN)
        try:
            user=User.objects.get(id=uid)
            request.user=user
        except User.DoesNotExist:
            return render_json('no this user',errors.NO_THIS_USER)
