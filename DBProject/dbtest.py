import MySQLdb as mdb
import csv

base_folder = "C:\\Users\\Gilad\\Desktop\\DBs\\"

db = mdb.connect(
    user="DbMysql01",
    password="DbMysql01",
    db="DbMysql01",
    port=3305
)

cur = db.cursor()


def insert_to_calories():
    with open(base_folder + "Calories.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO calories(id, total, fat) VALUES(%s, %s, %s)" % (row[0], row[1], row[2])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def insert_to_Carbohydrates():
    with open(base_folder + "Carbohydrates.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO carbohydrates(id, total, fiber, sugar) VALUES(%s, %s, %s, %s)" % \
                             (row[0], row[1], row[2], row[3])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def insert_to_fats():
    with open(base_folder + "Fats.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO fats(id, total, saturated, trans) VALUES(%s, %s, %s, %s)" % \
                             (row[0], row[1], row[2], row[3])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def insert_to_ing():
    with open(base_folder + "Ingredients.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO ingredients(meal_id, id, ingredient_name, measure) VALUES(%s, %s, %s, %s)"
                cur.execute(sqlcommand, [row[0], row[1], row[2].lower(), row[3]])
            else:
                is_header = False
        db.commit()


def proccess_input(str):
    if len(str) > 65535:
        print("too long")
        str = str.sub[:65534]
    str = str.encode("ascii", "replace")
    return str


def insert_to_meals():
    with open(base_folder + "Meals.csv") as file:
        reader = csv.reader(file)
        is_header = True
        keys = []
        for row in reader:
            if row[0] not in keys:
                if not is_header:
                    sqlcommand = ("INSERT INTO meals(meal_id, meal_name, instructions) VALUES(%s, %s, %s)")
                    data = (row[0], row[1], proccess_input(row[2]))
                    cur.execute(sqlcommand, data)
                    keys.append(row[0])
                else:
                    is_header = False
        db.commit()


def insert_to_protein():
    with open(base_folder + "Protein.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO protein(id, protein) VALUES(%s, %s)" % \
                             (row[0], row[1])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def insert_to_sterol():
    with open(base_folder + "Sterols.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO sterol(id, total) VALUES(%s, %s)" % \
                             (row[0], row[1])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def insert_to_tags():
    with open(base_folder + "Tags.csv") as file:
        reader = csv.reader(file)
        is_header = True
        keys = []
        for row in reader:
            if row[0] not in keys:
                if not is_header:
                    sqlcommand = ("INSERT INTO tags(meal_id, tag) VALUES(%s, %s)")
                    data = (row[0], row[1].lower())
                    cur.execute(sqlcommand, data)
                    keys.append(row[0])
                else:
                    is_header = False
        db.commit()


def insert_to_vitamins():
    with open(base_folder + "Vitamins.csv") as file:
        reader = csv.reader(file)
        is_header = True
        for row in reader:
            if not is_header:
                sqlcommand = "INSERT INTO vitamins(id, vitA, vitC) VALUES(%s, %s, %s)" % \
                             (row[0], row[1], row[2])
                print(sqlcommand)
                cur.execute(sqlcommand)
            else:
                is_header = False
        db.commit()


def print_db(name):
    sqlcommand = ("SELECT * FROM %s" % name)
    cur.execute(sqlcommand)
    for row in cur.fetchall():
        print(row)


# insert_to_vitamins()
print_db("vitamins")
