import lxml as lxml
import sqlite3
import lxml.html
import requests
from banks_info import data


def write_to_db(bank, buy_info, sale_info):
    data_base = sqlite3.connect("USD_to_UAH")
    data_base.execute(
        f"INSERT INTO {'currency_rate'}" "(Bank,buy_rate,sale_rate)" "VALUES (?,?,?)",
        (
            bank,
            buy_info,
            sale_info,
        ),
    )
    data_base.commit()


def get_course(bank_data):
    for bank_name, info in bank_data.items():
        if "open_api" not in bank_name:
            response = requests.get(info["url"]).text
            tree = lxml.html.document_fromstring(response)
            dirty_buy_price = tree.xpath(info["buy_price"])
            dirty_sell_price = tree.xpath(info["sale_price"])
            buy_price = dirty_buy_price[0].text.strip()
            sale_price = dirty_sell_price[0].text.strip()
            write_to_db(bank_name, buy_price, sale_price)
        else:
            open_api_info = requests.get("https://vkurse.dp.ua/course.json")
            price = open_api_info.json()["Dollar"]
            write_to_db(bank_name.split("_")[0], price["sale"], price["buy"])


get_course(data)
