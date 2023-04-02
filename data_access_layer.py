from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


query_example = gql("""
    query {
        users {
            id
            twitter_id
            twitter_username
        }
    }
""")

# Configure the GraphQL client
transport = RequestsHTTPTransport(url="http://localhost:9000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Send a query
result = client.execute(query_example)
print(result)