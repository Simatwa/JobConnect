This API forms the main backend interface for the clients.
It handles literally all the non-admin requests except user-account related operations such as account creation, update and deletion which are handled by Django.

### Django Endpoints

These endpoints are handled by Django


| Index | Endpoint                                                      | Purpose          |
|-------|---------------------------------------------------------------|------------------|
|  0    | [`/admin`](/admin)                                            | Administration   |
|  1    | [`/user/create`](/user/create)                                | Account Creation |
|  2    | [`/user/login?token=<api-key>`](/user/login?token=<api-key)   | Account Login    |
|  3    | [`/user/update/<id>`](/user/update/<id>)                      | Account Update   |
|  4    | [`/user/delete/<id>`](/user/delete/<id>)                      | Account Deletion |
|  5    | [`/user/logout`](/user/logout)                                | Account Logout   |