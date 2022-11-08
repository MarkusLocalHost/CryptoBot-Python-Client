import json
import logging

import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_response import json_response

from data import config
from utils.func.index_rating import make_request_index_rating_by_page
from utils.misc.requests_type import make_request_post, make_request_get
from utils.token.token import generate_token
from utils.web_app.check_webapp_signature import check_webapp_signature

routes = web.RouteTableDef()


# рейтинг криптовалют и просмотр конкретной криптовалюты
@routes.get("/index_rating/data/")
@aiohttp_jinja2.template("pages/index_rating/index_rating.html")
async def index_rating(request: web.Request):
    params = request.rel_url.query

    if "currency" in params.keys():
        context = {'currencies': params["currency"]}
        response = aiohttp_jinja2.render_template('pages/currency/detail_info.html',
                                                  request,
                                                  context)
        return response

    global_page = params["page"]
    current_currency = "usd"

    data_request = await make_request_index_rating_by_page(123, global_page, current_currency)

    return {"currencies": data_request["result"]}


# просмотр конкретной криптовалюты
@routes.get("/currency/{currency_name}")
@aiohttp_jinja2.template("pages/currency/detail_info.html")
async def currency_detail_info(request: web.Request):
    return


# просмотр конкретной криптовалюты
@routes.get("/portfolio")
@aiohttp_jinja2.template("pages/portfolio/portfolio.html")
async def portfolio_info(request: web.Request):
    return


# проверка хеша
@routes.post("/demo/checkData")
async def check_data_handler(request: web.Request):
    data = await request.post()
    if check_webapp_signature(config.BOT_TOKEN, data["_auth"]):
        return json_response({"ok": True})
    return json_response({"ok": False, "err": "Unauthorized"}, status=401)


# просмотр списка криптовалют при поиске
@routes.get("/try_find/{search_string}")
@aiohttp_jinja2.template("pages/search/view_currencies.html")
async def view_currencies(request: web.Request):
    search_string = request.match_info["search_string"]
    params = request.rel_url.query

    if "state" in params.keys():
        context = {'currency': params["state"]}
        response = aiohttp_jinja2.render_template('pages/currency/create_observer.html',
                                                  request,
                                                  context)

        return response
    elif "currency" in params.keys():
        context = {'currencies': params["currency"]}
        response = aiohttp_jinja2.render_template('pages/currency/detail_info.html',
                                                  request,
                                                  context)
        return response

    data = {
        "telegramUserID": 123,
        "currency_name": search_string,
        "currency_slug": ""
    }
    endpoint = f"http://127.0.0.1:8080/api/search/try_find_currency"
    headers = {
        "Content-Type": "application/json"
    }
    r = await make_request_post(endpoint, headers, json.dumps(data))

    return {"currencies": r.json()["result"]["coins"]}


# # просмотр списка криптовалют при поиске
# @routes.get("/search/form/{currency}")
# @aiohttp_jinja2.template("pages/search/form.html")
# async def view_currencies(request: web.Request):
#     currency = request.match_info["currency"]
#
#     data = {
#         "telegramUserID": 123,
#         "currency_slug": currency.lower()
#     }
#     token = await generate_token(data)
#     endpoint = f"http://127.0.0.1:8080/api/info/currency/data/short_version"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#     r = await make_request_get(endpoint, headers)
#     print(r.json())
#
#     return
