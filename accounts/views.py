from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as login_user, logout, authenticate
from django.contrib.auth.models import User
from transactions import calenderutil
from django.shortcuts import redirect
from .models import (
    SellerFactoryEmployee,
    SellerFactory,
    HomepageSlides,
    Buyer,
    BestBlog,
)
from backup.models import BackOrder, BackAuction
from django.views.generic import View
from django.urls import reverse
from transactions.models import Order, Auction
from feedback.models import Contact


def homepage(request):
    slides = HomepageSlides.objects.all()
    bestblogs = BestBlog.objects.all()
    return render(request, "homepage.html", {"slides": slides, "bestblogs": bestblogs})


def profile(request):
    return render(request, "profile.html", {})


def about(request):
    return render(request, "about.html", {})


def login(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) == True:
                login_user(request, user)
                return redirect("accounts:dashboard")
        except User.DoesNotExist:
            error = "incorrect email or password"
    return render(request, "login.html", {"error": error})


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect("account:login")
    context = {"user": user}
    try:
        order_queryset = Order.objects.filter(
            employee=user.sellerfactoryemployee)
        auctionsreal = Auction.objects.filter(
            factory=user.sellerfactoryemployee.factory
        )
        backauctions = BackAuction.objects.filter(
            factory=user.sellerfactoryemployee.factory
        )
        n = 0
        for order in order_queryset:
            if order.auction == auctionsreal[0]:
                n += 1
        auctions = BackAuction.objects.all()
        prices = []
        months_price = []
        months = []
        for auction in auctions:
            price = auction.price_per_tonne
            months_price.append(auction.date)
            prices.append(price)
        sumprice = sum(prices)
        months = calenderutil.getAllMonthsStr()
        try:
            mean_price = sumprice / len(prices)
        except:
            mean_price = 0

        context = {
            "prices": prices,
            "months_price": months_price,
            "months": months,
            "MeanPrice": round(mean_price, 3),
            "auction_history": auctions,
        }
        context["auctions"] = auctionsreal
        context["orders"] = n
        context["order_queryset"] = order_queryset
        return render(request, "seller_dashboard.html", context)
    except AttributeError:
        order_queryset = Order.objects.filter(buyer=user.buyer)
        auctions = []
        ordersmade = len(order_queryset)
        for order in order_queryset:
            auction = order.auction
            if auction not in auctions:
                auctions.append(auction)
        notifications = []
        for order in order_queryset:
            if order.status == 1 and not order.shipping_address:
                notification = Notification(
                    1,
                    "view_order",
                    f"Your Order for the {order.auction} has been accepted",
                    order.id,
                    "transactions",
                )
                notifications.append(notification)
        auctions = BackAuction.objects.all()
        prices = []
        months_price = []
        months = []
        for auction in auctions:
            price = auction.price_per_tonne
            months_price.append(auction.date)
            prices.append(price)
        sumprice = sum(prices)
        months = calenderutil.getAllMonthsStr()
        try:
            mean_price = sumprice / len(prices)
        except:
            mean_price = 0
        context = {
            "prices": prices,
            "months_price": months_price,
            "months": months,
            "MeanPrice": round(mean_price, 3),
            "ordersmade": ordersmade,
        }
        context["notifycount"] = len(notifications)

        context["auctions"] = auctions
        context["order_queryset"] = order_queryset

        context["notifications"] = notifications

        orders = Order.objects.filter(buyer=user.buyer)
        context["orders"] = len(orders)
        context["pending"] = len(
            Order.objects.filter(buyer=user.buyer, status=0))
        context["confirmed"] = len(
            Order.objects.filter(buyer=user.buyer, status=1))
        context["processed"] = len(
            Order.objects.filter(buyer=user.buyer, status=2))
        context["completed"] = len(
            Order.objects.filter(buyer=user.buyer, status=3))
        factories = []
        y = BackOrder.objects.all()
        ls = []
        for order in y:
            factory = order.auction.factory
            if factory not in ls:
                ls.append(factory)
        context["history_factories"] = ls
        for order in order_queryset:
            if order.employee.factory not in factories:
                factories.append(order.employee.factory)
        context["factories"] = factories
        return render(request, "buyer_dashboard.html", context)


def create_account(request):
    factory_queryset = SellerFactory.objects.all()
    return render(
        request, "create_seller_account.html", {
            "factory_queryset": factory_queryset}
    )


class Notification:
    def __init__(self, type, action, messsage, id, app_name):
        self.type = type
        self.action = action
        self.message = messsage
        self.id = id
        self.app_name = app_name


class GetFactoriesView(View):
    def get(self, request, *args, **kwargs):
        context = {"factories": SellerFactory.objects.all()}
        return render(request, "factories.html", context)


def create_buyer_account(request):
    print("nothing received")
    if request.method == "POST":
        print("stuff received")
        if (
            request.POST["username"]
            and request.POST["email"]
            and request.POST["pass"]
            and request.POST["repeatpass"]
            and request.POST["country"]
            and request.POST["address"]
            and request.POST["phone"]
        ):
            email = request.POST["email"]
            username = request.POST["username"]
            password = request.POST["pass"]
            repeat_password = request.POST["repeatpass"]
            country = request.POST["country"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            profile_photo = request.POST["profilepicture"]
            email_queryset = User.objects.filter(email=email)
            if email_queryset.__len__() == 0:
                if password == repeat_password:
                    user = User.objects.create(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    buyer = Buyer.objects.create(
                        user=user,
                        country=country,
                        address=address,
                        profile_picture=profile_photo,
                        phone=phone,
                    )
                    buyer.save()
                    if user.is_authenticated:
                        login_user(request, user)
                    return redirect("accounts:dashboard")
                else:
                    print("passwords do not match")
            else:
                print("a user with that email already exists")

    return render(request, "create_buyer_account.html", {})

def create_factory_account(request):
    if request.method == "POST":
        errors = []
        print(request.POST.keys())

        def AccountDetailsValid():
            errors = []
            print("sdhakjdhkajshdkjsahdkjashdkjahskjdhask")
            valid = True
            try:
                email = request.POST['Email']
            except:
                valid = False
                errors.append('email')
            print("1")
            try:
                firstname = request.POST["firstname"]
            except:
                valid = False
                errors.append('firstname')
            print("3")
            try:
                lastname = request.POST["lastname"]
            except:
                valid = False
                errors.append('lastname')
            print("4")
            try:
                repassword = request.POST["retypepass"]
            except:
                valid = False
                errors.append('enter all passwords')
            print("5")
            print("6")
            print(valid, errors)
            return valid
        try:
            print("trying")
            factory = SellerFactory(
                factory_name=request.POST['factoryname'],
                factory_initials=request.POST['initials'],

                company_email=request.POST['factoryemail'],
                phone=request.POST['factoryphone'],
                region=request.POST['townname'],
                country=request.POST['country'],
                street_name=request.POST['street_name'],
                zip_code=request.POST['zip_code'],
                physical_address=request.POST['physical_address'],

                trade_license=request.POST['tradelicense'],
                rating=0,
                factory_logo=request.POST['factorylogo'],
                googlemap="none",
                active=False
            )
            print(AccountDetailsValid(), "ahsdhasjdshak")
            if AccountDetailsValid():
                print("pass")
                first_name = request.POST["firstname"]
                last_name = request.POST['lastname']
                password = request.POST['password']
                email = request.POST['Email']
                print(first_name, last_name, password,
                      email, request.POST['username'])
                user = User(
                    username=request.POST['username'],
                    first_name=request.POST["firstname"],
                    last_name=request.POST['lastname'],
                    email=request.POST['Email'],
                    account_active = True
                )
                user.set_password(password)
                factory.save()
                print("pass factory")
                user.save()
                print("pass user")
                employee = SellerFactoryEmployee(
                    user=user,
                    factory=factory,
                    profile_picture=request.POST['userprofilepic']
                )
                employee.save()
                print("pass employee")
                if user.is_authenticated:
                    user = login_user(request, user)
                    return redirect('/dashboard')
        except:
            print("trying")
            factory = SellerFactory(
                factory_name=request.POST['factoryname'],
                factory_initials=request.POST['initials'],

                company_email=request.POST['factoryemail'],
                phone=request.POST['factoryphone'],
                region=request.POST['townname'],
                country=request.POST['country'],
                street_name=request.POST['street_name'],
                zip_code=request.POST['zip_code'],
                physical_address=request.POST['physical_address'],

                trade_license=request.POST['tradelicense'],
                rating=0,
                factory_logo=request.POST['factorylogo'],
                googlemap="none",
                active=False
            )
            print(AccountDetailsValid(), "ahsdhasjdshak")
            if AccountDetailsValid():
                print("pass")
                first_name = request.POST["firstname"]
                last_name = request.POST['lastname']
                password = request.POST['password']
                email = request.POST['Email']
                print(first_name, last_name, password,
                      email, request.POST['username'])
                user = User(
                    username=request.POST['username'],
                    first_name=request.POST["firstname"],
                    last_name=request.POST['lastname'],
                    email=request.POST['Email']
                )
                user.set_password(password)
                factory.save()
                print("pass factory")
                user.save()
                print("pass user")
                employee = SellerFactoryEmployee(
                    user=user,
                    factory=factory,
                    profile_picture=request.POST['userprofilepic']
                )
                employee.save()
                print("pass employee")
                if user.is_authenticated:
                    user = login_user(request, user)
                    return redirect('dashboard')

    return render(request, "create_factory_account.html", {"errors": []})


def accounts(request):
    return render(request, "accounts.html")

def contact (request):
    if request.method == "POST":
        if request.POST['name'] and request.POST['email'] and request.POST['subject'] and request.POST['message']:
            Contact.objects.create(name = request.POST['name'] , email = request.POST['email'], subject = request.POST['subject'], message = request.POST['message'])
    return render(request, 'contact.html', {})
    
def services(request):
    return render(request, "services.html", {})