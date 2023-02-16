import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import numpy as np
import jinja2

from mnst import get_configs as config
from mnst.sendmail import sendmail

excel_file = "/app/output/monthly_statistics.xlsx"


def main():
    clients_list = config.get_projects()
    db_list = config.get_config()

    # date setting (from now)
    date = datetime.now()
    date2 = date - timedelta(30)

    # Users section
    count_users = get_users(db_list, date)
    count_users2 = get_users(db_list, date2)
    # users - deltas
    u_a = np.array(count_users)
    u_b = np.array(count_users2)
    delta_users: int = u_a - u_b
    delta_users_percent: int = 100 * (u_a - u_b) / u_a

    # Visits section:
    count_visits = get_visits(date, db_list)
    count_visits2 = get_visits(date2, db_list)
    # visits - deltas:
    v_a = np.array(count_visits)
    v_b = np.array(count_visits2)
    delta_visits: int = v_a - v_b
    delta_visits_percent: int = 100 * (v_a - v_b) / v_a

    # Photos section:
    count_photos = get_photos(date, db_list)
    count_photos2 = get_photos(date2, db_list)
    # photos - deltas:
    p_a = np.array(count_photos)
    p_b = np.array(count_photos2)
    delta_photos: int = p_a - p_b
    delta_photos_percent: int = 100 * (p_a - p_b) / p_a


    # creating dataframe + excel
    dataframe(clients_list, count_users, count_visits, count_photos,
              delta_visits, delta_photos, delta_users, delta_users_percent, delta_visits_percent, delta_photos_percent)
    sendmail(excel_file)
    #sendmail("output/monthly_statistics.xlsx")

def dataframe(client, count_users, count_visits, count_photos, delta_visits, delta_photos, delta_users,
              delta_users_p, delta_visits_p, delta_photos_p):
    df = pd.DataFrame({
        "Client": client,
        "Users": count_users,
        "Users Delta": delta_users,
        "Users Delta, %": delta_users_p,
        "Visits": count_visits,
        "Visits Delta": delta_visits,
        "Visits Delta, %": delta_visits_p,
        "Photos": count_photos,
        "Photos Delta": delta_photos,
        "Photos Delta, %": delta_photos_p
    })
    def color_negative_red(val):
        color = 'red' if val < 0 else 'black'
        return f'color: {color}'

    df.loc["Total", "Users"] = df.Users.sum()
    df.loc["Total", "Visits"] = df.Visits.sum()
    df.loc["Total", "Photos"] = df.Photos.sum()

    pd.set_option('display.max_colwidth', 40)
    s = df.style.applymap(color_negative_red, subset=["Users Delta", "Users Delta, %",
                                                   "Visits Delta", "Visits Delta, %",
                                                   "Photos Delta", "Photos Delta, %"])
    s.to_excel(excel_file)


def get_users(db_list, date):
    users_results = []
    for db in db_list:
        con = MongoClient(db)
        database = con.list_database_names()
        get_db = database[0]
        db = con[f'{get_db}']
        date1 = date
        date2 = date1 - timedelta(days=30)
        collection = db.visit
        result = collection.find({"dt_start": {"$gte": date2, "$lt": date1}}).distinct("user_id")
        result = len(result)
        users_results.append(result)
    print("collecting users")
    return users_results

def get_visits(date, db_list):
    visits_results = []
    print("collecting visits")
    for db in db_list:
        con = MongoClient(db)
        database = con.list_database_names()
        get_db = database[0]
        db = con[f'{get_db}']
        collection = db.visit
        date2 = date - timedelta(days=30)
        result = collection.count_documents({"dt_start": {"$gte": date2, "$lt": date}})
        visits_results.append(result)
    return visits_results

def get_photos(date, db_list):
    photos_results = []
    print("collecting photos")
    for db in db_list:
        con = MongoClient(db)
        database = con.list_database_names()
        get_db = database[0]
        db = con[f'{get_db}']
        collection = db.photo
        date1 = date
        date2 = date1 - timedelta(days=30)
        result = collection.count_documents({"dt_create": {"$gte": date2, "$lt": date1}})
        photos_results.append(result)
    return photos_results
