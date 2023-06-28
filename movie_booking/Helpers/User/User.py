from bookingApp.Models.users.user import User


def UserExistsByEmail(email):
    return User.objects.filter(Email=email).exists()
def getUserById(Id):
    try:
        user = User.objects.get(pk=Id)
        return user
    except Exception as ex:
        return None
def getUserByMail(mail):
    try:
        user = User.objects.get(Email=mail)
        return user
    except Exception as ex:
        return None
def getAllUsers():
    try:
        return User.objects.filter(IsDeleted=False,RoleType=1).order_by("-Id")
    except Exception as ex:
        return None