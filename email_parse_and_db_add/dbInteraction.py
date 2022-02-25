import mysql.connector


class dbInteract():

    def __init__(self, connector):
        self.cursor = connector.cursor()

        try:
            select_table = "select * from coin_names"
            self.cursor.execute(select_table)
        except:
            create_table = "create table coin_names(name varchar(5) NOT NULL, PRIMARY KEY (name))"
            self.cursor.execute(create_table)
        self.cursor.fetchall()
        try:
            select_table = "select * from txns"
            self.cursor.execute(select_table)
        except:
            create_table = """create table txns(name varchar(5) NOT NULL, 
                                                total_spent DECIMAL(7, 2) NOT NULL,
                                                date DATETIME NOT NULL,
                                                coin_price DECIMAL(30, 15) NOT NULL,
                                                amt_invested DECIMAL(7, 2) NOT NULL,
                                                fees DECIMAL(7, 2) NOT NULL,
                                                coin_amt_bght DECIMAL(30, 15) NOT NULL,
                                                ref_code varchar(8) NOT NULL,
                                                PRIMARY KEY (ref_code),
                                                FOREIGN KEY (name) REFERENCES coin_names(name))"""
            self.cursor.execute(create_table)
        self.cursor.fetchall()

    def insert_into_db(self, obj):
        # Check if the name of the coin exists in the table coin_names
        check_coin_name = "select * from coin_names where name=%(coinName)s"
        self.cursor.execute(check_coin_name, obj)
        res = self.cursor.fetchall()

        # If it does not, then insert the coin name into the table coin_names
        # This is done to help reference the foreign key from the table txns
        if len(res) == 0:
            insert_coin_name = "insert into coin_names values (%(coinName)s)"
            self.cursor.execute(insert_coin_name, obj)
        
        # Check if the reference code of the transaction already exists in the table txns
        check_ref_code = "select * from txns where ref_code=%(refCode)s"
        self.cursor.execute(check_ref_code, obj)

        # If the entry exists in the database, then abort the function.
        if not len(self.cursor.fetchall()) == 0:
            return
        
        # Else, add the entry to the database.
        add_entry = """insert into txns values (%(coinName)s, %(ttlSpnt)s, %(date)s, %(exchgRate)s, 
                                                %(amtBght)s, %(fee)s, %(coinAmt)s, %(refCode)s)"""
        self.cursor.execute(add_entry, obj)

