from main import *

with open("tmp.txt") as f:
    query = f.read()

print(query)

# res = execute_mongodb_query(query)
res = execute_sql_query(query)
print(res)