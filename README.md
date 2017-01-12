# drf-coupons
A django-rest-framework application that provides many varieties of coupons 

## Setup instructions

1. Install `drf-coupons` via pip:
   ```
   $ pip install drf-coupons
   ```

2. Add `'coupons'` to `INSTALLED_APPS` in `settings.py`.

3. Migrate database:

   ```
   $ python manage.py migrate
   ```

4. Specify permissions for interacting with coupon endpoints.

   You can specify a list of groups that can perform specific actions against the coupons, such as restricting who can
   create or list coupons.

   By default all endpoints are open.

   ```
   COUPON_PERMISSIONS = {
       'CREATE': ['groupa', 'groupb'],
       'LIST': ['groupa'],
       'DELETE': ['groupb'],
       'RETRIEVE': ['groupa'],
       'UPDATE': ['groupb'],
   }
   ```

   You don't need to specify every endpoint in the list and can provide an empty list.

5. Communicate with coupon endpoints.

   You can place the urls into a subpath, however you like:

   ```
   urlpatterns = [
       # just adding here, but you can put into a subordinate path.
       url(r'^', include('coupons.urls')),
   ]
   ```

   | Endpoint                  | Details                                        |
   | ------------------------- | ---------------------------------------------- |
   | `GET /coupon`             | List all coupons                               |
   | `GET /coupon/{pk}`        | Retrieve details about a coupon by database id |
   | `POST /coupon`            | Create a new coupon                            |
   | `PUT /coupon/{pk}`        | Update a coupon                                |
   | `DELETE /coupon/{pk}`     | Delete a coupon                                |
   | `PUT /coupon/{pk}/redeem` | Redeem a coupon by database id                 |
   | `PATCH /coupon/{pk}`      | Not supported                                  |

## Coupon Types

It supports the following variations of coupons:

1. Coupons can be a value, or a percentage.
2. They can be bound to a specific user in the system.
3. They can be single-use:
   1. per user (a pre-specified user can use it once), `case I`
   2. globally (any user in the system can use it, but only once) `case II`
4. They can be infinite:
   1. per a specific user (a pre-specified user can use it repeatedly infinitely) `case III`
   2. infinite globally (any user can use it repeatedly infinitely) `case IV`
5. They can be used a specific number of times:
   1. per user (a pre-specified user can use it a specific number of times) `case V`
   2. globally (any user can use it a specific number of times) `case VI`
6. (They can be used by a specific list of users?) ... maybe later.

You create coupons in the system that are then claimed by users.
