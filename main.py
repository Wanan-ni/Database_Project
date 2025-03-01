import os
import json
import mysql.connector
from pymongo import MongoClient
import requests
from flask import Flask, request, jsonify
from llm_agent.llm_api import LLM_AGENT

app = Flask(__name__)

# MySQL Connection
def get_mysql_connection(password, database, host="localhost", user="root"):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# MongoDB Connection
def get_mongodb_connection(database, port, host="localhost"):
    client = MongoClient(f'mongodb://{host}:{port}/')
    return client[database]


# LLM API
def get_llm_agent():
    return LLM_AGENT()

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)