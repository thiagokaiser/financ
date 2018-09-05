from django.contrib.auth.models import User
from financ.models import Importacao

user  = User.objects.get(username='kaiser')

Importacao.objects.create(
	descricao='Hist Mobills',
	dt_import='2018-09-04',
	usuario=user
	)