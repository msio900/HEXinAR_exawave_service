# Value Object

class ClientVO:
    def __init__(self, id, pwd, name, phone_num, email):
        self.__id = id
        self.__pwd = pwd
        self.__name = name
        self.__phone_num = phone_num
        self.__email = email


    def getId(self):
        return self.__id

    def getPwd(self):
        return self.__pwd

    def getName(self):
        return self.__name

    def getEmail(self):
        return self.__email

    def getPhone_num(self):
        return self.__phone_num

    def __str__(self):
        return str(self.__id) + ' ' + self.__pwd + ' ' + self.__name + ' ' + self.__phone_num + \
               ' ' + self.__email

if __name__ == '__main__':
    client = ClientVO('1', '123456','김말숙','010-1234-5678','123456@gmail.com')
    print(client)

