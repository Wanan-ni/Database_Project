from main import query_llm

test_query = "Show all job applications"
generated_query = query_llm(test_query)
print("Generated Query:", generated_query)
