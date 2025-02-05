This API forms the main backend interface for the clients.
It handles literally all the non-admin requests except user-account related operations such as account creation, update and deletion which are handled by Django.

### Django Endpoints

These endpoints are handled by Django


| Index | Endpoint                                                      | Purpose          |
|-------|---------------------------------------------------------------|------------------|
|  0    | [`/d/admin`](/d/admin)                                            | Administration   |
|  1    | [`/d/user/create`](/d/user/create)                                | Account Creation |
|  2    | [`/d/user/login?token=<api-key>`](/d/user/login?token=<api-key)   | Account Login    |
|  3    | [`/d/user/update/<id>`](/d/user/update/<id>)                      | Account Update   |
|  4    | [`/d/user/delete/<id>`](/d/user/delete/<id>)                      | Account Deletion |
|  5    | [`/d/user/logout`](/d/user/logout)                                | Account Logout   |