# drf-coupons
A django-rest-framework application that provides many varieties of coupons 

## Dependencies

This project depends on:
1. `djangorestframework`
2. `django-filter`

## Setup instructions

1. Install `drf-coupons` via pip:
   ```
   $ pip install drf-coupons
   ```

2. Add `'rest_framework'` to `INSTALLED_APPS` in `settings.py`.

3. Add `'coupons'` to `INSTALLED_APPS` in `settings.py`.

4. Migrate database:

   ```
   $ python manage.py migrate
   ```

**Note:** this package was not developed to be compatible side-by-side with `django-coupons`, as they serve very similar needs.

## Usage

1. Specify permissions for interacting with coupon endpoints.

   You can specify a list of groups that can perform specific actions against the coupons, such as restricting who can
   create or list coupons.

   By default all endpoints are open except list.

   `retrieve` does not allow restriction because it doesn't generally need to support such permissions.

   `patch` is not supported as an endpoint and is therefore also not in the `COUPON_PERMISSIONS`.

   ```
   COUPON_PERMISSIONS = {
       'CREATE': ['groupa', 'groupb'],
       'LIST': ['groupa'],
       'DELETE': ['groupb'],
       'UPDATE': ['groupb'],
       'REDEEMED': ['groupc'],
   }
   ```

   You don't need to specify every endpoint in the list and can provide an empty list for an endpoint.

   The groups specified for `REDEEMED` are used in both `GET /coupon/{pk}/redeemed` and `GET /redeemed`.
   
   The groups specified for `DELETE` are used in both `DELETE /coupon/{pk}` and `DELETE /redeemed/{pk}`. 

2. Communicate with coupon endpoints.

   You can place the urls into a subpath, however you like:

   ```
   urlpatterns = [
       # just adding here, but you can put into a subordinate path.
       url(r'^', include('coupons.urls')),
   ]
   ```

   As stated above, by default any user in the system can touch any of the below endpoints, except where specified in bold.

   | Endpoint                    | Details                                                                                 |
   | --------------------------- | --------------------------------------------------------------------------------------- |
   | `GET /coupon`               | List all coupons in the system, **only superuser or in group can see all**.             |
   | `GET /coupon/{pk}`          | Retrieve details about a coupon by database id                                          |
   | `POST /coupon`              | Create a new coupon                                                                     |
   | `PUT /coupon/{pk}`          | Update a coupon                                                                         |
   | `DELETE /coupon/{pk}`       | Delete a coupon                                                                         |
   | `PUT /coupon/{pk}/redeem`   | Redeem a coupon by database id                                                          |
   | `GET /coupon/{pk}/redeemed` | List all times specified coupon was redeemed, **superuser or group member can see all** |
   | `PATCH /coupon/{pk}`        | **Not supported**                                                                       |
   | `GET /redeemed`             | List all redeemed instances, filter-able **only superuser or in group can do see all**  | 

## Querying

`GET /coupon` supports querying by coupon code, and filter by `user`, `bound`, `type` or by ranges of discount via `max_value`, `min_value`

`GET /redeemed` supports filtering by `user`.

## Objects

There are two objects provided:

1. `Coupon` - allows you to specify the properties of the coupon itself.

   | Field     | Type          | Meaning                                                |
   | --------- | ------------- | ------------------------------------------------------ |
   | `code`    | `string`      | the code for the coupon, case insensitive              |
   | `code_l`  | `string`      | automatically set lowercase version of the coupon code |
   | `type`    | `string`      | either `percent` or `value`, how the `value` field should be interpreted |
   | `expires` | `datetime`    | optional field to set when the coupon expires          |
   | `value`   | `decimal`     | the value for the coupon, such as `100` or `0.50`      |
   | `bound`   | `boolean`     | if `true` then the coupon can only be used by the specified user in the `user` field |
   | `user`    | `foreign key` | set when bound to point to the user                    |
   | `repeat`  | `integer`     | if `0` the coupon can be used infinitely, otherwise it specifies how often any system user can use it |

2. `ClaimedCoupon` - allows you to track whenever a user redeems a coupon.

   | Field      | Type          | Meaning                                                |
   | ---------- | ------------- | ------------------------------------------------------ |
   | `redeemed` | `datetime`    | automatically set when a coupon is redeemed            | 
   | `coupon`   | `foreign key` | automatically set to point at the coupon when redeemed |
   | `user`     | `foreign key` | automatically set to point at the coupon when redeemed |

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

## Developing

The unit-tests should automatically be run when you run `python manage.py test` and they are isolated.

If you'd like to contribute, please fork, and develop, branch from the `development` branch to and submit a pull request when ready.
