# Initialize PyMySQL as MySQL DB connector
import pymysql
# Bypass Django version check for PyMySQL
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()
