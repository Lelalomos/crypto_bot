from sqlitedict import SqliteDict
from utillity import read_config
import os

class cache_manager:
    def __init__(self, database_name:str) -> None:
        os.makedirs(os.path.join(os.getcwd(),'cache'), exist_ok=True)
        self.db = SqliteDict(os.path.join(os.getcwd(),'cache',f"{database_name}.sqlite"))

    def close(self) -> None:
        self.db.close()

    def commit(self) -> None:
        self.db.commit()

    def clear_data(self) -> None:
        self.db.clear()

    def update(self, key:str, value:any) -> None:
        self.db[key] = value
        self.commit()

    def update_buy(self, value:str) -> None:
        self.db['price_buy'] = self.db['price_buy']+f"{value} "
        self.commit()

    def update_sell(self, value:str) -> None: 
        self.db['price_sell'] = self.db['price_sell']+f"{value} "
        self.commit()

    def get_values(self, key:str) -> str:
        return self.db[key]

    def get_multiple_value(self, list_key:list) -> list:
        return [self.db[key] for key in list_key]

    def get_all_data(self) -> dict:
        c = dict()
        for k,v in self.db.items():
            c[k] = v
        return c

    def init_data(self, path_json:str) -> None:
        j_data = read_config(path_json)
        for k,v in j_data.items():
            self.db[k] = v

        self.db['price_buy'] = ""
        self.db['price_sell'] = ""
        self.commit()
    

