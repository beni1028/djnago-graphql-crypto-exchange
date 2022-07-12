import graphene
from .queries import Query
from .mutations import Mutation
from .subscriptions import Subscription

# schema = graphene.Schema(query=Query, mutation=Mutation) #, subscription=Subscription)
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
