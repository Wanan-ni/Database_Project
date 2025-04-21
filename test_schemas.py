from main import get_mysql_schema, get_mongodb_schema

def test_mysql():
    print("Testing MySQL Schema...")
    mysql_schema = get_mysql_schema()
    print(mysql_schema)

def test_mongodb():
    print("Testing MongoDB Schema...")
    mongodb_schema = get_mongodb_schema()
    print(mongodb_schema)

if __name__ == "__main__":
    # test mysql and mongodb
    test_mysql()
    print("\n" + "-"*50 + "\n")
    test_mongodb()
