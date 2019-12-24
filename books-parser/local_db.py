import MySQLdb

def connect():
  return MySQLdb.connect(host='localhost', user='root', passwd='888', db='scholar_results', charset='utf8')