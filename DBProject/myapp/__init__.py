from flask import Flask
import MySQLdb as mdb

app = Flask(__name__)

# db = mdb.connect(
#     host="mysqlsrv1.cs.tau.ac.il",
#     user="DbMysql01",
#     password="DbMysql01",
#     db="DbMysql01"
# )

from myapp import routes