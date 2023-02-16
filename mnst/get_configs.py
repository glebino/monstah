from glob import glob
import yaml


def get_projects():
    dirs = ["/app/clients/stable", "/app/clients/unstable", "/app/clients/latest"]
    projects_list = []
    for d in dirs:
        files = glob(f"{d}/domains/*.yml")
        for file in files:
            with open(file, 'r') as stream:
                dict = yaml.safe_load(stream)
                name = dict["name"]
                projects_list.append(name)
    return projects_list

def get_config():
    dirs = ["/app/clients/stable", "/app/clients/unstable", "/app/clients/latest"]
    db_list = []
    for d in dirs:
        files = glob(f"{d}/domains/*.yml")
        for file in files:
            with open(file, 'r') as stream:
                dict = yaml.safe_load(stream)
                db = dict["mongo"]
                db_list.append(db)
    return db_list

