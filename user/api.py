from lib.sms import send_sms
from lib.http import render_json
from common import errors
from django.core.cache import cache
from common import keys
from user.models import User


def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return render_json('request method error', errors.REQUEST_ERROR)

    phone = request.POST.get('phone')
    result,msg = send_sms(phone)

    return render_json(msg)


def submit_vcode(request):
    """通过验证码登录注册"""

    #判断是否是post请求
    if not request.method == "POST":
        return render_json('request method error', errors.REQUEST_ERROR)

    phone = request.POST.get('phone')
    # 取到发到手机的验证码
    vcode = request.POST.get('vcode')
    # 取到缓存中的验证码
    cache_vcode = cache.get(keys.VCODE_KEY % phone)

    #对比验证码是否一致
    if vcode == cache_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone, nickname=phone)
        # 两个返回值，一个是返回该用户，一个是创建则ture反之，
        request.session['uid'] = user.id
        return render_json(user.to_string())
    else:
        return render_json('verify code error',errors.VCODE_ERROR)

def get_profile(request):
    """获取个人资料"""
    pass


def set_profile(request):
    """修改个人资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass

