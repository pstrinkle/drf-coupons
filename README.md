# drf-coupons
A django-rest-framework application that provides many varieties of coupons 

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
