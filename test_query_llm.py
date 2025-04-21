from main import query_llm

test_query = "Show all job applications, mongodb"
generated_query = query_llm(test_query)
print("Generated Query:", generated_query)
