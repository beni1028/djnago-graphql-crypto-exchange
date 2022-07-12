from django.shortcuts import redirect, render, HttpResponsePermanentRedirect
from graphql_auth.models import UserModel
from django.contrib.auth.models import User
from .models import UserProfile
from graphql_jwt.backends import JSONWebTokenBackend 
# from graphene_django import 
# Create your views here.



# def verify(request,token):
    
#     u = UserModel.objects.last()
#     # create_profile(u)
#     print(u,'herererer')
#     print(u.email,'herererer')

#     print(u.status.verified)
#     if not u.status.verified:
#         u.status.verified = True
#         u.save()
#         u.token = token
#     # print(u.userprofile.age,'line 18')

#     context={
#         'user':u
#     }

#     # print(dir(u))
#     # print(u._meta.fields)
#     # print(u.values)
    
#     return HttpResponse('Hello '+str(u.username), context)



['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_legacy_get_session_auth_hash', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'refresh_from_db', 'refresh_tokens', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'status', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'userprofile', 'validate_unique']