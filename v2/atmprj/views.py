from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render

from . import models


#from sessionHelper import checkingSession as ck

def index(request):
	# check session login states
	# and carry name & amount
	# always return index
	if request.session.get('is_login') == True:
		name = request.session.get('user_name')
		amount = request.session.get('user_amount')
	return render(request, 'index.html')


def log_in(request):
	# # check session login states
	# # if already login then redirect to statement
	# if request.session.get('is_login',True):
	# return redirect('/statement/')

	if request.method == "POST":
		user_id = request.POST.get('userName')
		pass_word = request.POST.get('passWord')
		try:
			# find the user
			# get all imforation from the object
			user = models.Accounts.objects.get(identi = user_id)
			if str(user.identi) == user_id and user.pwd == pass_word:
				welcome = 'Hello, ' + str(user.name)
				request.session['is_login'] = True
				request.session['user_id'] = user.identi
				request.session['user_name'] = user.name
				num = user.amount
				request.session['user_amount'] = str(num)
				# save to django user
				django_user = authenticate(request, identi = user_id, pwd = pass_word)
				if django_user is not None:
					login(request, django_user)

				# always return to satement if user login
				return render(request, 'statement.html', {'msg': 'ok'})
			else:
				# password not match id
				return render(request, 'login.html', {'msg': 'wrong'})
		except:
			# no object find
			return render(request, 'login.html', {'msg': 'no user'})

	return render(request, 'login.html')


def register(request):
	# bug todo every refresh will auto add a person


	if request.method == "POST":
		new_username = request.POST.get('registerUsername')
		new_password = request.POST.get('registerPasswords')
		try:
			# register new user into database, and return identi number
			new_user = models.Accounts()
			new_user.name = new_username
			new_user.pwd = new_password
			new_user.save()
			new_id = new_user.identi

			# after reg then login
			return render(request, 'login.html', {'msg': 'Login with your new id:%d' % (new_id)})

		except:
			# reg fault
			return render(request, 'register.html', {'msg': 'catch part'})

	return render(request, 'register.html')


def transfer(request):
	if (request.method == "POST"):
		try:
			user = models.Accounts.objects.get(identi = request.session['user_id'])
		except:
			return render(request, 'login.html', {'msg': 'needs login'})

		operateAmount = request.POST.get('amount')
		operateAcct = request.session.get('user_id')
		otherAccount = request.POST.get('Payee')
		if operateAmount and otherAccount:
			if operateAmount is otherAccount:
				return render(request, 'transfer.html', {'msg': 'can not be yourself'})
		else:
			return render(request, 'transfer.html', {'msg': 'amount,or payer empty'})

		try:
			other_user = models.Accounts.objects.get(identi = otherAccount)
			user_amount = request.session['user_amount']
			dua = Decimal(user_amount)
			doa = abs(Decimal(operateAmount))
			if doa < dua:
				user.amount -= doa
				user.save()
				other_user.amount += doa
				other_user.save()
				return render(request, 'transfer.html', {'msg': 'Transfer Success!'})
			return render(request, 'transfer.html', {'msg': 'Unvalid amount!'})
		except:
			return render(request, 'transfer.html', {'msg': 'User not find!'})

	return render(request, 'transfer.html')


def log_out(request):
	request.session.flush()
	logout(request)
	return redirect('/log_in/')

def statement(request):
	"""
	only deal with GET,
	check the session before display
	return to login page if session of method wrong
	"""

	if request.method=="GET" and not needsLogin(request):
		try:
			user = models.Accounts.objects.get(identi = request.session['user_id'])
			request.session['is_login'] = True
			request.session['user_id'] = user.identi
			request.session['user_name'] = user.name
			num = user.amount
			request.session['user_amount'] = str(num)
			return render(request, 'statement.html',{"msg":"ok"})

		except:
			return render(request, 'login.html',{"msg":"login first"})
	else:
		return render(request, 'login.html',{"msg":"login first"})


def deposit(request):
	"""
	GET: need check session to continue display
	POST: update database and return success message
				if wrong, return Error message
	"""

	if request.method=="GET" and needsLogin(request):
		return render(request,'login.html',{"msg":"Login First!"})

	if (request.method == "POST"):
		try:
			user = models.Accounts.objects.get(identi = request.session['user_id'])
		except:
			return render(request, 'login.html', {'msg': 'needs login'})

		try:
			amount = request.POST.get('amount')
			# todo js check negtive number
			# currently just read as typo and get absolute value
			dua = abs(Decimal(amount))
			user.amount += dua
			user.save()
			return render(request, 'deposit.html', {'msg': 'deposit Success!'})
		except:
			return render(request, 'deposit.html', {'msg': 'Cookie Error'})
	return render(request, 'deposit.html')


def withdraw(request):
	"""
	GET: need check session to continue display
	POST: check session about user information
	otherwise need login
	update database and return success message
				if wrong, return Error message
	"""

	if request.method=="GET" and needsLogin(request):
		return render(request,'login.html',{"msg":"Login First!"})

	if (request.method == "POST"):
		# check login statement
		try:
			user = models.Accounts.objects.get(identi = request.session['user_id'])
		except:
			return render(request, 'login.html', {'msg': 'needs login'})

		try:
			amount = request.POST.get('amount')
			# todo js check negtive number
			# currently just read as typo and get absolute value
			dua = abs(Decimal(amount))
			if (dua <= user.amount):
				user.amount -= dua
				user.save()
				return render(request, 'withdraw.html', {'msg': 'Withdraw Success!'})
			else:
				return render(request, 'withdraw.html', {'msg': 'You don\'t have such money!'})
		except:
			return render(request, 'withdraw.html', {'msg': 'Cookie Error'})

	return render(request, 'withdraw.html')

def closeAccount(request):
	if request.method == "GET":
		needsLogin(request)

	if (request.method == "POST"):
		# check login statement
		try:
			user = models.Accounts.objects.get(identi = request.session['user_id'])
		except:
			return render(request, 'login.html', {'msg': 'needs login'})

		try:

			password = request.POST.get('pwd')
			print(password)
			print(user.identi)
			print(user.pwd)
			# print(password)

			if user.pwd == password:
				models.Accounts.objects.filter(identi = request.session['user_id']).delete()
				log_out(request)
				return render(request, 'login.html', {'msg': 'delete Success!Logout to Login page'})
			else:
				return render(request, 'delete.html', {'msg': 'password wrong '})

		except:
			return render(request, 'delete.html', {'msg': 'cookie error '})
	return render(request, 'delete.html')

def needsLogin(request):
	return False if request.session.get("is_login") else True

