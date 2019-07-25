**How to setup this project**
----------

This short doc assumes you have docker installed on your computer.
If you do not have, [Install](https://docs.docker.com/get-started/) here.
The project runs on Postgres only because of the multi-tenancy strategy.

**Compulsory environmental variables**
* HASURA_SAAS_DATABASE: *This is the postgres database name you want to you, assumes you have the database created.  It defaults to 'hasura_saas'.*
* HASURA_SAAS_USER: *This is the postgres user name.  It defaults to 'postgres'.*
* HASURA_SAAS_PASSWORD: *This is the postgres user password.  It defaults to 'postgres'.*
* MAIN_DOMAIN_URL: *This is required to register the public schema on first run. It defaults to 'localhost'.*
* HASURA_SAAS_AUTH_WEBHOOK: *webhook URL for hasura to perform authentication on requests, this URL should just carry the auth server path,
like this ``/api/v1/users/webhook/auth/`` without the domain*.


**Steps to run**
-----
* **Run django migrations:** ``python manage.py migrate_schemas --shared``. This creates the database relations and the schemas for the tenants.
* **Run django project:** ``python manage.py runserver``

* You can also register an account on the django app at endpoint `/api/v1/users/` on any of the domains, endpoint collects payload
```json
    {
        "username": "test",
        "first_name": "Test",
        "last_name": "Test",
        "is_tenant": true,
        "password": "mostsecure",
        "email": "test@localhost.com",
        "is_superuser": true
    }
```
The `is_tenant` attribute is only effective when you are sending the API request to
the main domain. When this is true, it creates a sub-domain for the user being created.
* To get JWT for authentication, POST `{email: <email_address>, password: <password>}` to `/api/v1/users/token/`
* By default, graphql API is accessible at `http://<domain>:8080/v1alpha1/graphql` and fully protected
by webhook authorization, whenever you want to access data in the graphql API, add `X-HASURA-TARGET-SCHEMA` as an header to your request alongide your token, this helps the django application
authenticate the requesting user in the correct domain because by default, all authorization requests from
hasura are sent to the main domain, then the main domain handles appropriately. This header `X-HASURA-TARGET-SCHEMA` defaults to `public`.
* The hasura console is available at
`http://<domain>:8080`. You can change this in the `docker-run.sh` file.


**Sample Procedure of a request to the graphQL API**
--
Assuming our django server runs at `localhost:8000` and hasura runs at `localhost:8080`
* Sign Up:
Send request to `localhost:8000/api/v1/users/`, payload: 
```json
    {
        "username": "admin",
        "first_name": "Administrator",
        "last_name": "LastName",
        "is_tenant": true,
        "password": "mostsecure",
        "email": "admin@localhost.com",
        "is_superuser": true
    }
```
This signs me up to the main domain `localhost:8000` and creates a subdomain for me that resolves to
`admin.localhost:8000`.
* To get our token: we send a post request to `localhost:8000/api/v1/users/token/` with payload
```json
{
  "password": "mostsecure",
  "email": "admin@localhost.com",
}
```
We get a response looking like this:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU1MjQzNzMyNiwianRpIjoiMDg3MWY2MjhjYTlhNGM2NWJlNzk1YmU0ZTYwNzAyN2MiLCJ1c2VyX2lkIjoyfQ.QT_roC2-APBfKA4rauNT38u4MwL76X4C05hBPm6hRrc",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUyMzUwOTI2LCJqdGkiOiI3YzJjYWFmMWQ4OWE0NjQ3OGZlZWZlODljNTg1YjFkMSIsInVzZXJfaWQiOjJ9.faA5LWqb9TSSAoke7pyz9IGg_RZSTYusoWxfXWXaqak"
}
```

* Finally, when we try to send requests to our graph API at `localhost:8080/v1alpha/graphql/`. We add headers:
```
X-HASURA-TARGET-SCHEMA=public
Authorization=Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUyMzUwOTI2LCJqdGkiOiI3YzJjYWFmMWQ4OWE0NjQ3OGZlZWZlODljNTg1YjFkMSIsInVzZXJfaWQiOjJ9.faA5LWqb9TSSAoke7pyz9IGg_RZSTYusoWxfXWXaqak 
```

Request Data:
```graphql
query {
  users_user {
    id
    first_name
  }
}
```

Response:
```json
{
  "data": {
    "users_user": [
      {
        "id": 2,
        "first_name": "Test"
      }
    ]
  }
}
```
When we remove the Authorization header:
```json
{
  "errors": [
    {
      "extensions": {
        "path": "$",
        "code": "access-denied"
      },
      "message": "Authentication hook unauthorized this request"
    }
  ]
}
```

**Auto tracking postgres table for new sub-domains**
--
If you wish to track specific table automatically. You can define a subclass under 
such model named 'Hasura' and set track attribute to True such as example below.

```python
class User(Model):
    ...
    
    class Hasura:
        track = True

```

This model named 'User' is automatically tracked for new domains.
NOTE: It requires you settings `HASURA_URL` attribute in the project settings.
Sample:
`file: settings.py`
```python
...

HASURA_URL = '45.93.135.102:8000'

...
```

**Other useful commands*
--
- Create superuser ``./manage.py createsuperuser --username=admin --schema=customer1``. **customer1** here is the schema name.
- Run migrations in parallel when there are many tenants: ``python manage.py migrate_schemas --executor=parallel``
- When you want to execute a normal django command, but targeted at a specific schema, use the `tenant_command`. E.g To load data for *customer1* schema. 
``./manage.py tenant_command loaddata --schema=customer1``.
- List tenants: 
    ```bash
    for t in $(./manage.py list_tenants | cut -f1);
    do
        ./manage.py tenant_command dumpdata --schema=$t --indent=2 auth.user > ${t}_users.json;
    done    
    ```
- Perform tenant post save actions:
    ```python
    from tenant_schemas.signals import post_schema_sync
    from tenant_schemas.models import TenantMixin
    
    def foo_bar(sender, tenant, **kwargs):
        ...
        #This function will run after the tenant is saved, its schema created and synced.
        ...
    
    post_schema_sync.connect(foo_bar, sender=TenantMixin)
    ```
We'd find more [here](https://django-tenant-schemas.readthedocs.io/en/latest/use.html)

