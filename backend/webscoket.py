# from graphql_ws.websockets_lib import WsLibSubscriptionServer
# from . import schema

# app = Sanic(__name__)

# subscription_server = WsLibSubscriptionServer(schema)

# @app.websocket('/subscriptions', subprotocols=['graphql-ws'])
# async def subscriptions(request, ws):
#     await subscription_server.handle(ws)
#     return ws


# app.run(host="0.0.0.0", port=8000)