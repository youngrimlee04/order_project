from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# onetoone 관계인 user라는 모델에서 해당하는 user 지우면
# partner라는 데이터 어떻게 할꺼냐? cascade는 user 삭제할 때 그걸 따라지운다
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    description=models.TextField() #TextFIeld는 최대 글자수 지정안해도됨
