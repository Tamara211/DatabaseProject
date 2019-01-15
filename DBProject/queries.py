import MySQLdb as mdb

db = mdb.connect(
    user="DbMysql01",
    password="DbMysql01",
    db="DbMysql01",
    port=3305
)

INST_FROM_NAME = 1
CONTAINS_ING = 2
NO_SUGAR = 3
HAS_INTAKE = 4
HAS_TAG = 5

CALORIES = 1
CARBON = 2
FIBER = 3
FATS = 4
SATURATED = 5
TRANS = 6
PROTEIN = 7
STEROL = 8
VITA = 9
VITC = 10

cur = db.cursor()


def inst_from_name(name):
    sql_command = "SELECT meals.instructions, ingredients.ingredient_name, ingredients.measure FROM meals, ingredients WHERE meals.meal_name=%s " \
                  "AND meals.meal_id = ingredients.meal_id"

    cur.execute(sql_command, [name])
    inst = ""
    ing = []
    for row in cur.fetchall():
        inst = row[0]
        ing.append(row[1:])
    print(inst)
    for i in ing:
        print(i)
    return inst, ing


def contains_ing(ings):
    user_input = "I.ingredient_name=%s "
    if len(ings) > 1:
        additive = " OR I.ingredient_name=%s" * (len(ings) - 1)
    else:
        additive = ""
    user_input = user_input + additive
    sql_command = "SELECT DISTINCT M.meal_name, M.instructions FROM meals AS M, ingredients AS I" \
                  " Where I.meal_id = M.meal_id AND (" + user_input + ")"
    meals = []
    cur.execute(sql_command, ings)
    for row in cur.fetchall():
        meals.append(row)
    return meals


def no_sugar():
    sql_command = "SELECT DISTINCT meals.meal_name, meals.instructions FROM   meals, ingredients WHERE  meals.meal_id = ingredients.meal_id AND ingredients.ingredient_name <> 'sugar' " \
                  "AND ingredients.ingredient_name <> 'Sugar'"

    cur.execute(sql_command)
    meals = []
    cur.execute(sql_command)
    for row in cur.fetchall():
        meals.append(row)
    return meals


def has_tag(tag):
    sql_command = "SELECT meals.meal_name, meals.instructions FROM meals, tags " \
                  "WHERE meals.meal_id = tags.meal_id " \
                  "AND tags.tag = %s"
    meals = []
    cur.execute(sql_command, tag)
    for row in cur.fetchall():
        meals.append(row)
    return meals


def sql_executor(params):
    command_ind = params[0]
    if command_ind == INST_FROM_NAME:
        return inst_from_name(params[1:])
    elif command_ind == CONTAINS_ING:
        return contains_ing(params[1:])
    elif command_ind == NO_SUGAR:
        return no_sugar()
    elif command_ind == HAS_INTAKE:
        return has_intake(params[1:])
    elif command_ind == HAS_TAG:
        return has_tag(params[1:])
    else:
        return None


def concat_commands(commands, is_and=True):
    final_meals = []
    for command in commands:
        command_meals = sql_executor(command)
        if len(command_meals) == 0:
            return []
        if len(final_meals) == 0:
            final_meals.extend(command_meals)
        else:
            if is_and:
                final_meals = list(set(final_meals).intersection(set(command_meals)))
            else:
                final_meals.extend(command_meals)
    return final_meals


def parse_intake_table(table_type):
    if table_type == CALORIES:
        return "calories", "calories.total", "calories.id"
    elif table_type == CARBON:
        return "carbohydrates", "carbohydrates.total", "carbohydrates.id"
    elif table_type == FIBER:
        return "carbohydrates", "carbohydrates.fiber", "carbohydrates.id"
    elif table_type == FATS:
        return "fats", "fats.total", "fats.id"
    elif table_type == SATURATED:
        return "fats", "fats.saturated", "fats.id"
    elif table_type == TRANS:
        return "fats", "fats.trans", "fats.id"
    elif table_type == PROTEIN:
        return "protein", "protein.total", "protein.id"
    elif table_type == STEROL:
        return "sterol", "sterol.total", "sterol.id"
    elif table_type == VITA:
        return "vitamins", "vitamins.vitA", "vitamins.id"
    elif table_type == VITC:
        return "vitamins", "vitamins.vitC", "vitamins.id"
    else:
        return None, None, None


def get_has_intake_sql(params):
    table_type = params[0]
    amount = params[1]
    at_least = params[2]
    table_name, coloum, id = parse_intake_table(table_type)
    if at_least:
        oper = ">="
    else:
        oper = "<="
    sql_command = "SELECT meals.meal_name AS id, meals.instructions AS inst " \
                  "FROM  meals, " \
                  "(SELECT ingredients.meal_id AS id, SUM(ingredients.measure*" + coloum + ") AS sumamount " \
                    "FROM  ingredients, " + table_name + " " \
                    "WHERE ingredients.id =" + id + " " \
                    "GROUP  BY ingredients.meal_id) AS counter " \
                    "WHERE  meals.meal_id = counter.id  AND counter.sumamount " + oper + " %s"
    # meals = []
    # cur.execute(sql_command, [amount])
    # for row in cur.fetchall():
    #     meals.append(row)
    #
    # return meals
    return sql_command, amount


def has_intake(list_of_commands):
    sql_list = []
    amount_list = []
    for command in list_of_commands:
        sql, am = get_has_intake_sql(command)
        sql_list.append(sql)
        amount_list.append(am)

    meals = []
    if len(sql_list) == 1:
        cur.execute(sql_list[0], amount_list)
        for row in cur.fetchall():
            meals.append(row)
    else:
        sql_command = "SELECT dbq1.id, dbq1.inst FROM "
        i = 1
        for sql in sql_list:
            sql_command += "( " + sql + ") as dbq%d" % i
            if i != len(sql_list):
                sql_command += ", "
            else:
                sql_command += " "
            i += 1
        sql_command += " WHERE "
        for i in range(1, len(sql_list)):
            sql_command += "dbq1.id = dbq%d.id " % (i + 1)
            if i < len(sql_list) - 1:
                sql_command += " AND "
        print(sql_command)
        cur.execute(sql_command, amount_list)
        for row in cur.fetchall():
            meals.append(row)

    return meals


# command1 = [CONTAINS_ING, "Beef"]
# command2 = [CONTAINS_ING, "Bread"]
# user_params = [command1, command2]
# res = concate_commands(user_params)
# print(len(res))
intake1 = [STEROL, "10", False]
intake2 = [PROTEIN, "300", True]
intake3 = [VITC, "100", True]


# res = concate_commands([command1, command2, command3, command4])
# res = sql_executor([HAS_INTAKE, intake1, intake2])
res = concat_commands([[HAS_INTAKE, intake1, intake2, intake3], [NO_SUGAR], [HAS_TAG, "Vegetarian"]])
for meal in res:
    print(meal)
