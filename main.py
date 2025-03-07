import os
import json
import mysql.connector
from pymongo import MongoClient
import requests
from flask import Flask, request, jsonify
from llm_agent.llm_api import LLM_AGENT

app = Flask(__name__)


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
def is_nosql_query(query_text):
    # Simple heuristic - can be improved
    nosql_keywords = ["find", "aggregate", "insertOne", "updateOne", "deleteOne",
                      "insertMany", "updateMany", "deleteMany", "collection"]

    for keyword in nosql_keywords:
        if keyword in query_text.lower():
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


# Execute MongoDB query
def execute_mongodb_query(query_text):
    db = get_mongodb_connection()

    try:
        # Parse the query text into executable code
        # CAUTION: This is for educational purposes only
        # In production, you should use a safer approach to parse and validate queries

        # Example for simplicity (assuming find query on reviews collection)
        if "db.reviews.find" in query_text:
            # Extract the filter criteria
            filter_start = query_text.find("{")
            filter_end = query_text.rfind("}")

            if filter_start != -1 and filter_end != -1:
                filter_str = query_text[filter_start:filter_end + 1]
                filter_dict = eval(filter_str)  # CAUTION: eval is dangerous in production

                results = list(db.reviews.find(filter_dict, {"_id": 0}))
                return results

        return {"error": "Could not parse MongoDB query"}
    except Exception as e:
        return {"error": str(e)}


def process_query():
    user_input = request.json.get('query')

    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Get query from LLM
    generated_query = query_llm(user_input)

    # Execute appropriate query
    if is_nosql_query(generated_query):
        results = execute_mongodb_query(generated_query)
    else:
        results = execute_sql_query(generated_query)

    return jsonify({
        "user_input": user_input,
        "generated_query": generated_query,
        "results": results
    })


# Convert natural language query to SQL or MongoDB query using LLM.
def query_llm(user_input):
    llm_agent = get_llm_agent()

    mysql_schema = get_mysql_schema()
    mongodb_schema = get_mongodb_schema()

    prompt = f"""
You are a database query translator that converts natural language to either SQL or MongoDB queries.

MySQL Database Schema:
{mysql_schema}

MongoDB Collections Schema:
{mongodb_schema}

Important rules:
1. If the query seems to fit a relational data model with structured data, generate a SQL query.
2. If the query seems to fit a document-based model or mentions specific MongoDB features, generate a MongoDB query.
3. For SQL, return only the SQL query statement without any explanation.
4. For MongoDB, return only executable MongoDB query code like db.collection.find({{}}) without any explanation.
5. Use appropriate protection against SQL injection.

User query: {user_input}

Determine if this is a SQL or MongoDB query and provide the appropriate query:
"""

    generated_query = llm_agent.call_llm(prompt)

    generated_query = generated_query.strip()

    return generated_query


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