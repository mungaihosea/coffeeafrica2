from django.urls import path
from .views import (
    homepage,
    profile,
    login,
    create_account,
    dashboard,
    GetFactoriesView,
    accounts,
    create_buyer_account,
    about,
    contact,
    services,
    create_factory_account,
    market,
    help,
)

namespace = "accounts"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("profile/", profile, name="profile"),
    path("login/", login, name="login"),
    path("create_account/", create_account, name="create_account"),
    path("dashboard/", dashboard, name="dashboard"),
    path("factories/", GetFactoriesView.as_view(), name="factories"),
    path("GetSarted/", accounts, name="start"),
    path("Buyer/", create_buyer_account, name="buyer"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("services/", services, name="services"),
    path("Factory/", create_factory_account, name="factory"),
    path("market/", market, name="market"),
    path("help/", help, name="help"),
]
