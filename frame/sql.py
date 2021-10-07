class Sql:
    selone = "SELECT * FROM client WHERE pwd='%s' AND email='%s'"
    selall = "SELECT * FROM client"
    insert = "INSERT INTO client (pwd,name,email,phone_num) VALUES ('%s','%s','%s','%s')"
    update = "UPDATE client SET pwd='%s', name='%s', phone_num='%s' WHERE email='%s'"
    delete = "DELETE FROM client WHERE email='%s'"