from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from sys import argv
from os import getcwd

import mysql.connector

class Database(QMainWindow):
    logging = False
    flag = True
    table = ''
    
    def __init__(self):
        super(Database, self).__init__()
        loadUi('UI\\Main.ui', self)

        self.setWindowIcon(QtGui.QIcon(getcwd() + '\\Img\\WHI3PER.ico'))

        # ========================================================== #

        self.LIGHT.triggered.connect(self.lightMode)
        self.DARK.triggered.connect(self.darkMode)
        self.GRAY.triggered.connect(self.grayMode)
        self.PURPLE.triggered.connect(self.purpleMode)
        self.BLUE.triggered.connect(self.blueMode)
        self.ABOUT.triggered.connect(self.aboutMe)

        # ========================================================== #
        
        self.LOGGIN_BUTTON.clicked.connect(self.logIn)
        self.ADD_BUTTON.clicked.connect(self.addUser)

        self.SHOW_ALL_USERS.clicked.connect(self.userListAll)
        self.SHOW_ALL_USERNAMES.clicked.connect(self.userListUsernames)
        self.SHOW_ALL_PASSWORDS.clicked.connect(self.userListPasswords)
        self.SHOW_ALL_GMAILS.clicked.connect(self.userListGmails)
            
        self.EDIT_BUTTON.clicked.connect(self.editUser)
        self.SEARCH_BUTTON.clicked.connect(self.searchUser)
        self.REMOVE_BUTTON_2.clicked.connect(self.removeUser)
            
        self.EXIT_BUTTON.clicked.connect(self.exitProgram)

    # ============================================================================================== #

    def lightMode(self):
        self.setStyleSheet('''''')
    
    # ============================================================================================== #
    
    def darkMode(self):
        self.setStyleSheet('''
            QWidget {
                background-color: rgb(0, 0, 0);
                color: rgb(0, 255, 255);
            }
            QPushButton {
                background-color: rgb(46, 46, 46);
                color: rgb(0, 255, 255);
            }
            QLabel { color: rgb(0, 255, 255); }
            QTextBrowser { color: rgb(0, 255, 255); }
            QMenuBar { color: rgb(85, 255, 127); }
            QTabBar::tab { background-color: rgb(46, 46, 46); }
            ''')
        
    # ============================================================================================== #

    def grayMode(self):
        self.setStyleSheet('''
            QWidget {
                background-color: rgb(35, 35, 35);
                color: rgb(255, 255, 0);
            }

            QPushButton { background-color: rgb(55, 55, 55); }
            QTextBrowser { color: rgb(255, 255, 0); }
            QLabel { color: rgb(85, 255, 127); }
            QMenuBar { color: rgb(85, 255, 127); }
            QTabBar::tab { background-color: rgb(55, 55, 55); }
            ''')
    
    # ============================================================================================== #
    
    def purpleMode(self):
        self.setStyleSheet('''
            QWidget {
                background-color: rgb(29, 26, 48);
                color: #FFFFFF;
            }
            QPushButton {
                background-color: rgb(241, 170, 155);
                color: rgb(29, 26, 48);
            }
            QLineEdit {
                background-color: rgb(240, 195, 142);
	        color: rgb(29, 26, 48);
            }
            QLabel { color: rgb(241, 170, 155); }
            QTextBrowser { color: rgb(240, 195, 142); }
            QMenuBar { color: rgb(159, 232, 250); }
            QTabBar::tab { background-color: rgb(29, 26, 48); }
            ''')
    
    # ============================================================================================== #
    
    def blueMode(self):
        self.setStyleSheet('''
            QWidget {
                background-color: rgb(29, 84, 132);
                color: #FFFFFF;
            }
            QPushButton {
                background-color: rgb(159, 232, 250);
	            color: rgb(29, 26, 48);
            }
            QLineEdit {
                background-color: rgb(240, 195, 142);
                color: rgb(29, 26, 48);
            }
            QLabel { color: rgb(170, 255, 255); }
            QTextBrowser { color: rgb(240, 195, 142); }
            QMenuBar { color: rgb(159, 232, 250); }
            QTabBar::tab { background-color: rgb(29, 84, 132); }
            ''')
        
    # ============================================================================================== #

    def aboutMe(self):
        loadUi('UI\\About Me.ui', self)
        self.LOGO_LABEL.setPixmap(QPixmap(getcwd() + '\\Img\\WHI3PER.png'))
        self.EMAIL.setPixmap(QPixmap(getcwd() + '\\Img\\Gmail.png'))
        self.GITHUB.setPixmap(QPixmap(getcwd() + '\\Img\\Github.png'))
        self.LINKDIN.setPixmap(QPixmap(getcwd() + '\\Img\\Linkdin.png'))
        self.TELEGRAM.setPixmap(QPixmap(getcwd() + '\\Img\\Telegram.png'))
        
    # ============================================================================================== #
    
    def logIn(self):
        self.LOGS.clear()

        global data
        global cursor
        
        username_  = self.MySQL_USERNAME.text()
        password_  = self.MySQL_PASSWORD.text()
        database_  = self.MySQL_DATABASE.text()
        self.table = self.MySQL_TABLE.text()
        
        try:
            data = mysql.connector.connect(user = username_, password = password_, host = '127.0.0.1', database = database_)
            cursor = data.cursor()
            self.LOGS.append('Logging successful.')
            self.logging = True
            
        except:
            self.LOGS.append('Logging failed.')
            self.logging = False
            
        self.MySQL_USERNAME.clear()
        self.MySQL_PASSWORD.clear()
        self.MySQL_DATABASE.clear()
        self.MySQL_TABLE.clear()

    # ============================================================================================== #

    def addUser(self):
        self.LOGS.clear()
        
        if self.logging:
            username = self.USERNAME.text()
            password = self.PASSWORD.text()
            gmail    = self.GMAIL.text()

            try:
                cursor.execute(f'INSERT INTO {self.table} VALUES (\'{username}\', \'{password}\', \'{gmail}\')')
                                                                                                    
                data.commit()
                self.LOGS.append('User added successfully.')

            except mysql.connector.Error as err:
                self.LOGS.append(f'Error: {err}')
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
            
        self.USERNAME.clear()
        self.PASSWORD.clear()
        self.GMAIL.clear()
    
    # ============================================================================================== #

    def userListAll(self):
        self.LOGS.clear()

        if self.logging:
            cursor.execute('SELECT * FROM %s;' %(self.table))
        
            for (username, password, gmail) in cursor:
                self.flag = False
                self.LOGS.append(f'Username: {username}\nPassword: {password}\nGmail   : {gmail}\n')
                
            if self.flag:
                self.LOGS.append('Empty.')
            self.flag = True
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
    
    # ============================================================================================== #

    def userListUsernames(self):
        self.LOGS.clear()
        
        if self.logging:
            cursor.execute('SELECT username FROM %s;' %(self.table))
    
            for username in cursor:
                username = str(username)
                self.LOGS.append(f'Username: {username[2:-3]}')
                self.flag = False
                
            if self.flag:
                self.LOGS.append('Empty.')
            self.flag = True
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
    
    # ============================================================================================== #

    def userListPasswords(self):
        self.LOGS.clear()
        
        if self.logging:
            cursor.execute('SELECT password FROM %s;' %(self.table))
    
            for password in cursor:
                password = str(password)
                self.LOGS.append(f'Password: {password[2:-3]}')
                self.flag = False

            if self.flag:
                self.LOGS.append('Empty.')
            self.flag = True
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
    
    # ============================================================================================== #

    def userListGmails(self):
        self.LOGS.clear()
        
        if self.logging:
            cursor.execute('SELECT gmail FROM %s;' %(self.table))
    
            for gmail in cursor:
                gmail = str(gmail)
                self.LOGS.append(f'Gmail: {gmail[2:-3]}')
                self.flag = False

            if self.flag:
                self.LOGS.append('Empty.')
            self.flag = True
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
    
    # ============================================================================================== #
    
    def editUser(self):
        self.LOGS.clear()

        if self.logging:
            new_username = self.NEW_USERNAME.text()
            new_password = self.NEW_PASSWORD.text()
            username     = self.SEARCH_USERNAME_1.text()

            try:
                cursor.execute(f'UPDATE {self.table} SET username = \'{new_username}\', password = \'{new_password}\' WHERE username = \'{username}\'')
        
                if cursor.rowcount:
                    self.LOGS.append(f'User {username} updated successfully.')
                else:
                    self.LOGS.append(f'User {username} not found.')
            
                data.commit()

            except mysql.connector.Error as err:
                self.LOGS.append(f"Error: {err}")
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
            
        self.NEW_USERNAME.clear()
        self.NEW_PASSWORD.clear()
        self.SEARCH_USERNAME_1.clear()

    # ============================================================================================== #

    def searchUser(self):
        self.LOGS.clear()

        if self.logging:
            username = self.SEARCH_USERNAME_2.text()

            try:
                cursor.execute(f'SELECT * FROM {self.table} WHERE username = \'{username}\'')
                results = cursor.fetchall()
        
                if results:
                    for item in results:
                        self.LOGS.append('\n'.join(item))
                else:
                    self.LOGS.append('User not found.')
            
            except mysql.connector.Error as err:
                self.LOGS.append(f"Error: {err}")
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
        
        self.SEARCH_USERNAME_2.clear()

    # ============================================================================================== #
    
    def removeUser(self):
        self.LOGS.clear()

        if self.logging:
            username = self.SEARCH_USERNAME_3.text()

            try:
                if username == '*':
                    cursor.execute(f'DELETE FROM {self.table};')
                    self.LOGS.append(f'{cursor.rowcount} users deleted.')
            
                else:
                    cursor.execute(f'DELETE FROM {self.table} WHERE username = \'{username}\'')
                    if cursor.rowcount:
                        self.LOGS.append(f'User {username} deleted successfully.')
                    else:
                        self.LOGS.append(f'User {username} not found.')
                
                data.commit()
        
            except mysql.connector.Error as err:
                self.LOGS.append(f"Error: {err}")
                
        else:
            self.LOGS.append('Logging failed.')
            self.LOGS.append('~ First logging to MySQL.')
            
        
        self.SEARCH_USERNAME_3.clear()

    # ============================================================================================== #

    def exitProgram(self):
        exit()
    
    # =============================================================================================== #
