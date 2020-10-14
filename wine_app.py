from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime, timedelta
import psycopg2
import os


Builder.load_file('front_end.kv')

conn = psycopg2.connect(user="postgres", password="-MiDWP0$tGr3qL!-",
                        host="localhost", port="5432", database="wines.db")
db = conn.cursor()
tblAccount = "CREATE TABLE IF NOT EXISTS accounts(id SERIAL PRIMARY KEY, username TEXT NOT NULL, " \
             "password TEXT NOT NULL, join_date DATE DEFAULT CURRENT_DATE);"
db.execute(tblAccount)
tblMyWines = "CREATE TABLE IF NOT EXISTS my_wines(id SERIAL PRIMARY KEY, year INTEGER NOT NULL, " \
             "winery TEXT NOT NULL, varietal_or_title TEXT NOT NULL, review_date DATE DEFAULT CURRENT_DATE," \
             " review TEXT NOT NULL);"
db.execute(tblMyWines)


# class Authentication:
#
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#
#     @staticmethod
#     def est_user_file(username, password):
#         with open('user_auth.json') as auth_file:
#             current_user = json.load(auth_file)
#         start_time = datetime.now()
#         current_user[username] = {'username': username, 'password': password, 'created': start_time.strftime('%H:%M:%S')}
#         print('loaded')
#         with open('user_auth.json', 'w') as auth_file:
#             json.dump(current_user, auth_file, default=str)
#
#         print('logged in')
#
#     def get_current_user(self):
#         # if os.path.exists('user_auth.json'):
#         with open('user_auth.json') as auth_file:
#             current_user = json.load(auth_file)
#             print(timedelta(datetime.now() - current_user.created))
#             date_time = datetime.now()
#             hour = timedelta(seconds=3600)
#             delta = date_time - hour
#             print(delta)
#             while delta >
#         # else:
#         #     return None
#
#     # @staticmethod
#     # def delete_user_auth():
#     #     with open('user_auth.json') as auth_file:
#     #         lines = auth_file.readlines()
#     #
#     #     with open('user_auth.json', 'w') as auth_file:
#     #         for line in lines:
#     #             if line.strip('\n') !=
#

class LoginScreen(Screen):

    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):
        self.ids.username.text = username
        self.ids.password.text = password
        query = "SELECT * FROM accounts WHERE username=%s AND password=%s"
        if len(username and password) > 0:
            # TODO: make requirement for username to be unique.
            db.execute(query, [username, password])
            results = db.fetchall()
            for i in results:
                print(i)

            db.connection.commit()
            db.close()
            print('logged in')
            self.manager.current = 'main_screen'

        else:
            self.ids.wrong_log_in_creds.text = 'Please enter a username and password'


class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def sign_up_user(self, username, password):
        self.ids.username.text = username
        self.ids.password.text = password
        query = "INSERT INTO accounts(username, password) VALUES" \
                " ('" + username + "','" + password + "');"
        # TODO: Parameterize this query
        if len(username) < 1 and len(password) < 1:
            self.ids.empty_cred_field.text = 'Please enter a username and password'
        elif len(username) < 1:
            self.ids.empty_cred_field.text = 'Please enter a username'
        elif len(password) < 1:
            self.ids.empty_cred_field.text = 'Please enter a password'
        else:
            db.execute(query)
            db.connection.commit()
            db.close()
            self.manager.current = "main_screen"


class MainScreen(Screen):
    def log_out(self):
        self.manager.current = "login_screen"

    def add_new_wine_screen(self):
        self.manager.current = "add_wine_screen"

    def get_review(self, year, winery, varietal_or_title, review):
        conn = psycopg2.connect(user="postgres", password="-MiDWP0$tGr3qL!-",
                                host="localhost", port="5432", database="wines.db")
        db = conn.cursor()
        query = "SELECT review FROM my_wines WHERE year=%s AND winery=%s AND varietal_or_title=%s"

        if year and winery and varietal_or_title is not None:
            db.execute(query, (year, winery, varietal_or_title))
            results = db.fetchone()
            if results is None:
                print('none')
                self.ids.review.text = 'did not taste'

            else:
                self.ids.review.text = results[0]
                print(results[0])

            db.connection.commit()
            db.close()

        else:
            self.ids.review.text = 'Please enter a year, winery, and varietal/title'


class AddWineScreen(Screen):

    def add_wine(self, year, winery, varietal_or_title, review):
        query = "INSERT INTO my_wines(year, winery, varietal_or_title, review) VALUES" \
                "('" + year + "', '" + winery + "', '" + varietal_or_title + "', '" + review + "');"

        conn = psycopg2.connect(user="postgres", password="-MiDWP0$tGr3qL!-",
                                host="localhost", port="5432", database="wines.db")
        db = conn.cursor()
        if len(year or winery or varietal_or_title or review) > 0:
            db.execute(query)
            db.connection.commit()
            db.close()
            print("wine added")
        else:
            self.ids.empty_add_wine_field = 'Please enter year, winery, varietals or title and a review'

        self.manager.current = "main_screen"

    def log_out(self):
        self.manager.current = "login_screen"


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
