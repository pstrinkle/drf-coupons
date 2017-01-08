# drf-coupons
A django-rest-framework application that provides many varieties of coupons 

It supports the following variations of coupons:

1. Coupons can be a value, or a percentage.
2. They can be bound to a specific user in the system, or an email address (not yet in the system).
3. They can be single-use per user, or single-use globally.
4. They can be infinite per a specific user, or infinite globally.
5. They can be used a specific number of times per user, or globally.
6. (They can be used by a specific list of users?) ... maybe

You create coupons in the system that are then claimed by users.
