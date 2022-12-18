from ariadne.contrib.federation import FederatedObjectType
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, MutationType, make_executable_schema, QueryType,ScalarType
from src.resolvers import logs_resolvers
from ariadne.contrib.federation import make_federated_schema
from prisma import Prisma

prisma = Prisma()

schema = load_schema_from_path('schema.graphql')

query = QueryType()
mutation = MutationType()
user= FederatedObjectType("User")
log = FederatedObjectType("Log")
datetime = ScalarType("DateTime")

query.set_field("userTimeLogs", logs_resolvers.resolve_user_time_logs)
mutation.set_field("addTimeInLogs", logs_resolvers.resolve_add_time_in_logs)
mutation.set_field("addTimeOutLogs", logs_resolvers.resolve_add_time_out_logs)

@log.field("user")
def resolve_log(obj, info):
    return {user.field('id'): log.field('user_id')}

@datetime.serializer
def serialize_datetime(value):
    return value.isoformat()

schema = make_federated_schema(schema, query, mutation,log)
app = GraphQL(schema, debug=True)
 