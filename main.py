#!/usr/bin/env python

#import sqlite3
import pickle
import os

#db = sqlite3.connect('sqlite.db')

# cursor = db.cursor()
# cursor.execute('''
#         CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, balance INT, ip TEXT, lastpayment TEXT, balancelimit INT )
#                ''')
# db.commit()

class Client(object):
    def __init__(self, name, ip, code, balance, balancelimit, lastpayment):
        self.name = name
        self.ip = ip
        self.code = code
        self.balance = balance
        self.balancelimit = balancelimit
        self.lastpayment = lastpayment

    def value(self):
        return self.balance*self.balancelimit

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
            print "client: %s(%s) - Ip Address %s(%s) - Balance %.2f BalanceLimit %d Value %.2f" % \
                (client.name, client.ip, client.code, client.balance, client.balancelimit, client.lastpayment, client.value())

    def addClient(self):
        print "Input client name"
        clientName = raw_input()

        print "Input ip address"
        clientIp = raw_input()

        print "Input client code"
        clientCode = raw_input()

        clientBalance = self.inputClientBalance()
        clientBalanceLimit = self.inputClientBalanceLimit()
        clientLastPayment = self.inputClientLastPayment()

        self.database[clientName] = Client(clientName, clientIp, clientCode, clientBalance, clientBalanceLimit, clientLastPayment)
        self.save()

    def inputClientBalance(self):
        clientBalance = None
        while not clientBalance:
            try:
                print "Input client balance"
                clientBalance = float(raw_input())
            except ValueError:
                clientBalance = None
        return clientBalance

    def inputClientBalanceLimit(self):
        clientBalanceLimit = None
        while not clientBalanceLimit:
            try:
                print "Client Balance limit:"
                clientBalanceLimit = int(raw_input())
            except ValueError:
                clientBalanceLimit = None
        return clientBalanceLimit

    def inputClientLastPayment(self):
        clientLastPayment = None
        while not clientLastPayment:
            try:
                print "Client's last payment date:"
                clientLastPayment = int(raw_input())
            except ValueError:
                clientBalanceLimit = None
        return clientLastPayment

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
            print "Client %s not in database yet!" % clientName

        clientBalance = self.inputClientBalance()
        client.balance = clientBalance

    def changeStockAndSave(self):
        clientName = self.selectClientByName()

        client = self.getClientByName(clientName)
        if not client:
            print "Client %s not in database yet!" % clientName

        print "Current stock is %d!" % client.balancelimit
        clientBalanceLimit = self.inputClientBalanceLimit()
        client.balancelimit = clientBalanceLimit

        self.save()

    def valueOfAllClients(self):
        collectedValue = 0.0
        for clientName, client in self.database.iteritems():
            collectedValue += client.value()
        print "Value of all clients is: %f" % collectedValue

    def stockOfAllClients(self):
        stockOfAllClients = 0
        for clientName, client in self.database.iteritems():
            stockOfAllClients += client.balancelimit
        print "Stock of all clients is: %d" % stockOfAllClients

    def blockClient(self):
        clientName = self.selectClientByName()
        try:
            cstate = os.popen('ipconfig')
            cstatenow = cstate.read()
            print cstatenow
        except KeyError:
            print "Client does not exists"
            return
        print "Client %s blocked" % clientName
        self.save()

    def unblockClient(self):
        clientName = self.selectClientByName()

        try:
            print self.database[clientName]
        except KeyError:
            print "Client does not exists"
            return
        print "Client %s enabled" % clientName
        self.save()


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
        8 : database.stockOfAllClients,
        9 : database.blockClient,
        10 : database.unblockClient
    }

    while (choice != 11):
        print
        print "1.  Print database"
        print "2.  Add client"
        print "3.  Delete client"
        print "4.  Change stock and save"
        print "5.  Change price and save"
        print "6.  Change price"
        print "7.  Value of all clients"
        print "8.  Stock of all clients"
        print "9.  Block client"
        print "10. Unblock client"
        print "11. Exit"
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


