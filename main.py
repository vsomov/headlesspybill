#!/usr/bin/env python

#import sqlite3
import pickle

#db = sqlite3.connect('sqlite.db')

# cursor = db.cursor()
# cursor.execute('''
#         CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, balance INT, ip TEXT, lastpayment TEXT, balancelimit INT )
#                ''')
# db.commit()

class Client(object):
    def __init__(self, name, code, balance, balancelimit, lastpayment):
        self.name = name
        self.code = code
        self.balance = balance
        self.balancelimit = balancelimit
        self.lastpayment = lastpayment

    def value(self):
        return self.price*self.stock

class ClientDatabase(object):
    def __init__(self, filename):
        self.filename = filename
        self.database = {}

        try:
            self.open()
        except IOError:
            self.save()

    def open(self):
        file = open(self.filename, "rb")
        self.database = pickle.load(file)
        file.close()

    def save(self):
        file = open(self.filename, "wb")
        pickle.dump(self.database, file)
        file.close()

    def printDB(self):
        for clientName, client in self.database.iteritems():
            print "client: %s(%s) - Price %.2f Stock %d Value %.2f" % \
                (client.name, client.code, client.price, client.stock, client.value())

    def addClient(self):
        print "Input client name"
        clientName = raw_input()

        print "Input client code"
        clientCode = raw_input()

        clientPrice = self.inputclientPrice()
        clientStock = self.inputclientStock()

        self.database[clientName] = Client(clientName, clientCode, clientPrice, clientStock)
        self.save()

    def inputClientPrice(self):
        clientPrice = None
        while not clientPrice:
            try:
                print "Input client price"
                clientPrice = float(raw_input())
            except ValueError:
                clientPrice = None
        return clientPrice

    def inputClientStock(self):
        clientStock = None
        while not clientStock:
            try:
                print "Client Stock:"
                clientStock = int(raw_input())
            except ValueError:
                clientStock = None
        return clientStock

    def selectClientByName(self):
        print "Input client name"
        return raw_input()

    def getClientByName(self, name):
        if name not in self.database:
            return None
        return self.database[name]

    def deleteClient(self):
        clientName = self.selectClientByName()

        try:
            del self.database[clientName]
        except KeyError:
            print "Client does not exists"
            return
        print "Client %s deleted" % clientName
        self.save()

    def changePriceAndSave(self):
        self.changePrice()
        self.save()

    def changePrice(self):
        clientName = self.selectClientByName()

        client = self.getClientByName(clientName)
        if not client:
            print "Client %s not in databse yet!" % clientName

        clientPrice = self.inputClientPrice()
        client.price = clientPrice

    def changeStockAndSave(self):
        clientName = self.selectClientByName()

        client = self.getClientByName(clientName)
        if not client:
            print "Client %s not in databse yet!" % clientName

        print "Current stock is %d!" % client.stock
        clientStock = self.inputClientStock()
        client.stock = clientStock

        self.save()

    def valueOfAllClients(self):
        collectedValue = 0.0
        for clientName, client in self.database.iteritems():
            collectedValue += client.value()
        print "Value of all clients is: %f" % collectedValue

    def stockOfAllClients(self):
        stockOfAllClients = 0
        for clientName, client in self.database.iteritems():
            stockOfAllClients += client.stock
        print "Stock of all clients is: %d" % stockOfAllClients

if __name__ == "__main__":

    print "Input database filename:"
    databaseFilename = raw_input()

    database = ClientDatabase(databaseFilename)

    choice = 0
    choices = {
        1 : database.printDB,
        2 : database.addClient,
        3 : database.deleteClient,
        4 : database.changeStockAndSave,
        5 : database.changePriceAndSave,
        6 : database.changePrice,
        7 : database.valueOfAllClients,
        8 : database.stockOfAllClients
    }

    while (choice != 9):
        print
        print "1. Print database"
        print "2. Add client"
        print "3. Delete client"
        print "4. Change stock and save"
        print "5. Change price and save"
        print "6. Change price"
        print "7. Value of all clients"
        print "8. Stock of all clients"
        print "9. Exit"
        print "Choose:"
        choice = raw_input()
        print
        try:
            choice = int(choice)
        except ValueError:
            choice = 0
        if choice in choices:
            choices[choice]()


# cursor = db.cursor()
# name1 = 'Siorik'
# phone1 = '3366858'
# email1 = 'user@example.com'
# # A very secure password
# password1 = '12345'
#
# name2 = 'John'
# phone2 = '5557241'
# email2 = 'johndoe@example.com'
# password2 = 'abcdef'
#
# # Insert user 1
# cursor.execute('''INSERT INTO users(name, phone, email, password)
#                   VALUES(?,?,?,?)''', (name1,phone1, email1, password1))
# print('First user inserted')
#
# # Insert user 2
# cursor.execute('''INSERT INTO users(name, phone, email, password)
#                   VALUES(?,?,?,?)''', (name2,phone2, email2, password2))
# print('Second user inserted')
#
# db.commit()


