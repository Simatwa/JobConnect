from django.contrib.auth.hashers import make_password

p1 = make_password("hello")

p2 = make_password(p1)

print(
    len(p1),
    len(p2)
)