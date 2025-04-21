import os
import json
import mysql.connector
from pymongo import MongoClient
import requests
from flask import Flask, request, jsonify
from llm_agent.llm_api import LLM_AGENT
import re
import ast

app = Flask(__name__)

operations = ["find", "aggregate", "insertOne", "insertMany",
                  "updateOne", "updateMany", "deleteOne", "deleteMany", "count", "sort", "limit", "collection"]


# Load config file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'llm_agent', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


config = load_config()

# MySQL Connection
def get_mysql_connection():
    mysql_config = config["MYSQL_CONFIG"]
    return mysql.connector.connect(
        host=mysql_config["host"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )


# MongoDB Connection
def get_mongodb_connection():
    mongo_config = config["MONGODB_CONFIG"]
    client = MongoClient(f'mongodb://{mongo_config["host"]}:{mongo_config["port"]}/')
    return client[mongo_config["database"]]


# LLM API
# def get_llm_agent():
#     return LLM_AGENT()
def get_llm_agent():
    config_path = os.path.join(os.path.dirname(__file__), 'llm_agent', 'config.json')

    if not os.path.exists(config_path):
        raise Exception(f'CONFIG_FILE {config_path} doesn\'t exist')

    return LLM_AGENT(CONFIG_FILE=config_path)


# Determine if query is for SQL or NoSQL
def is_nosql_query(query):
    # Simple heuristic - can be improved
    if query.startswith("db"):
    # for keyword in nosql_keywords:
    #     if keyword in query.lower():
            return True
    return False


# Execute SQL query
def execute_sql_query(query):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)

        if query.lower().startswith(("select", "show")):
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return {"affected_rows": cursor.rowcount}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def parse_args(args_str):
    args = []
    brace_level = 0
    current = ''
    for c in args_str:
        if c == ',' and brace_level == 0:
            args.append(current.strip())
            current = ''
        else:
            current += c
            if c == '{':
                brace_level += 1
            elif c == '}':
                brace_level -= 1
    if current:
        args.append(current.strip())
    return args

def safe_parse_mongo_expr(expr):

    # step 1: 给所有 key 加引号（支持 $key 和普通 key）
    expr = re.sub(r'([{,]\s*)(\$?\w+)\s*:', r'\1"\2":', expr)

    # step 2: 替换 true/false/null → True/False/None（适配 ast）
    expr = expr.replace("true", "True").replace("false", "False").replace("null", "None")

    # step 3: 使用 ast.literal_eval 安全解析
    return ast.literal_eval(expr)
def parse_mongodb_query(query_text):
    query = query_text.strip().replace("\n", "")

    if re.match(r"db\.getCollectionNames\s*\(\s*\)", query_text):
        return {
            "operation": "listCollections"
        }

    try:
        collection_match = re.match(r"db\.(\w+)\.", query)
        if not collection_match:
            return {"error": "Collection name not found"}
        collection = collection_match.group(1)

        op_match = re.search(rf"\.({'|'.join(operations)})\s*\((.*?)\)", query, re.DOTALL) # to handle multi line
        if not op_match:
            return {"error": "No recognized operation found"}

        operation = op_match.group(1)
        args = op_match.group(2).strip()

        query_dict = {
            "collection": collection,
            "operation": operation
        }

        # Special case:

        # find with sort, limit, etc.
        if operation == "find":
            filter_dict = safe_parse_mongo_expr(args) if args else {}
            query_dict["filter"] = filter_dict

            # handle chained methods: sort, limit, count
            sort_match = re.search(r"\.sort\s*\((.*?)\)", query)
            if sort_match:
                sort_args = sort_match.group(1).strip()
                query_dict["sort"] = safe_parse_mongo_expr(sort_args)

            limit_match = re.search(r"\.limit\s*\((\d+)\)", query)
            if limit_match:
                query_dict["limit"] = int(limit_match.group(1))

            count_match = re.search(r"\.count\s*\(\)", query)
            if count_match:
                query_dict["count"] = True  # optional flag you can use downstream

        elif operation == "aggregate":
            query_dict["pipeline"] = safe_parse_mongo_expr(args)

        elif operation in ["insertOne", "insertMany", "updateOne", "updateMany", "deleteOne", "deleteMany"]:
            args_list = [a.strip() for a in parse_args(args)]
            parsed_args = [safe_parse_mongo_expr(arg) for arg in args_list]
            if operation.startswith("insert"):
                query_dict["documents"] = parsed_args if operation == "insertMany" else parsed_args[0]
            elif operation.startswith("update"):
                query_dict["filter"] = parsed_args[0]
                query_dict["update"] = parsed_args[1]
            elif operation.startswith("delete"):
                query_dict["filter"] = parsed_args[0]

        elif operation == "count":
            query_dict["count"] = True
            query_dict["filter"] = ast.safe_parse_mongo_expr(args) if args else {}

        return query_dict

    except Exception as e:
        return {"error": f"Failed to parse: {str(e)}"}


# Execute MongoDB query
def execute_mongodb_query(query):
    db = get_mongodb_connection()

    try:
        query_dict = parse_mongodb_query(query)
        # print(query_dict)
        collection_name = query_dict.get("collection", None)
        operation = query_dict.get("operation", None)

        #db operations
        if not collection_name:
            if operation == "listCollections":
                return db.list_collection_names()


        #collection operations
        if not operation:
            return {"error": "Missing collection or operation"}
        collection = db[collection_name]

        if operation == "find":
            filter_ = query_dict.get("filter", {})

            if isinstance(filter_, tuple):
                filter_, projection = filter_
            else:
                projection = {"_id": 0}

            tmp = collection.find(filter_, projection)
            if "sort" in query_dict:
                sort_fields = query_dict["sort"]
                # Convert dict to list of tuples: {"age": -1} → [("age", -1)]
                if isinstance(sort_fields, dict):
                    tmp = tmp.sort(list(sort_fields.items()))
            if "limit" in query_dict:
                tmp = tmp.limit(query_dict["limit"])

            results = list(tmp)
            if query_dict.get("count"):
                return {"count": len(results)}

            return results

        elif operation == "aggregate":
            pipeline = query_dict.get("pipeline", [])
            results = list(collection.aggregate(pipeline))
            return results

        elif operation == "insertOne":
            document = query_dict.get("documents", {})
            if not document:
                return {"error": "Missing document for insertOne"}
            result = collection.insert_one(document)
            return {"inserted_id": str(result.inserted_id)}

        elif operation == "insertMany":
            document = query_dict.get("documents", [])
            if not document:
                return {"error": "Missing documents for insertMany"}
            result = collection.insert_many(document)
            return {"inserted_ids": [str(i) for i in result.inserted_ids]}

        elif operation in ["updateOne", "updateMany"]:
            filter_ = query_dict.get("filter")
            update = query_dict.get("update")
            if not update:
                return {"error": "Missing filter or update data"}

            if operation == "updateOne":
                result = collection.update_one(filter_, update)
            else:
                result = collection.update_many(filter_, update)

            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        # === DELETE ===
        elif operation in ["deleteOne", "deleteMany"]:
            filter_ = query_dict.get("filter")
            if not filter_:
                return {"error": "Missing filter for delete"}

            if operation == "deleteOne":
                result = collection.delete_one(filter_)
            else:
                result = collection.delete_many(filter_)

            return {"deleted_count": result.deleted_count}
        else:
            return {"error": f"Unsupported operation: {operation}"}

    except Exception as e:
        return {"error": str(e)}

def clean_query(text):
    match = re.search(r"```(?:\w+)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    else:
        return text.strip()

@app.route("/", methods=["POST"])
def process_query():
    user_input = request.json.get('query')

    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Get query from LLM
    llm_info_dic = query_llm(user_input)
    print(llm_info_dic["generated_query"])
    generated_query = clean_query(llm_info_dic["generated_query"])



    # Execute appropriate query
    if is_nosql_query(generated_query):
        results = execute_mongodb_query(generated_query)
    else:
        results = execute_sql_query(generated_query)

    return jsonify({
        "user_input": user_input,
        "generated_query": generated_query,
        "results": results,
        "all_tokens_num": llm_info_dic["all_tokens_num"],
        "current_tokens_num": llm_info_dic["current_tokens_num"]

    })




# Convert natural language query to SQL or MongoDB query using LLM.
def query_llm(user_input):
    llm_agent = get_llm_agent()

    mysql_schema = get_mysql_schema()
    mongodb_schema = get_mongodb_schema()

    prompt = """
            You are a database query translator that converts natural language to either SQL or MongoDB queries.
            
            MySQL Database Schema:
            {}
            
            MongoDB Collections Schema:
            {}
            
            Important rules:
            1. If the query seems to fit a relational data model with structured data, generate a SQL query.
            2. If the query seems to fit a document-based model or mentions specific MongoDB features, generate a MongoDB query.
            3. FAll SQL queries must be fully executable by the `mysql` CLI client.
            4. All MongoDB queries must be valid JavaScript syntax accepted by `mongosh`. We only accept these operations {}
            5. Use appropriate protection against SQL injection.
            
            User query: {}
            
            Determine if this is a SQL or MongoDB query provide the appropriate query with markdown. Remember Just give me one type query(SQL or MongoDB), JUST QUERY! NO EXPLAINATIONS NO COMMENTS ARE NEEDED
            
            """.format(mysql_schema, mongodb_schema, operations, user_input)
    print(prompt)
    llm_info_dic = {}
    generated_query = llm_agent.call_llm(prompt)

    llm_info_dic["generated_query"] = generated_query.strip()

    llm_info_dic["all_tokens_num"] = llm_agent.all_tokens
    llm_info_dic["current_tokens_num"] = llm_agent.current_tokens

    return llm_info_dic


def get_mysql_schema():
    conn = get_mysql_connection()
    cursor = conn.cursor()
    schema = []

    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            table_schema = f"Table: {table_name}\nColumns:\n"
            for column in columns:
                table_schema += f"- {column[0]} ({column[1]})\n"

            schema.append(table_schema)

        return "\n".join(schema)
    except Exception as e:
        return f"Error fetching MySQL schema: {str(e)}"
    finally:
        cursor.close()
        conn.close()


def get_mongodb_schema():
    db = get_mongodb_connection()
    schema = []

    try:
        collections = db.list_collection_names()

        for collection_name in collections:
            sample = db[collection_name].find_one()

            if sample:
                collection_schema = f"Collection: {collection_name}\nExample document structure:\n"
                for key, value in sample.items():
                    if key == "_id":
                        continue
                    collection_schema += f"- {key}: {type(value).__name__}\n"

                schema.append(collection_schema)

        return "\n".join(schema)
    except Exception as e:
        return f"Error fetching MongoDB schema: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
