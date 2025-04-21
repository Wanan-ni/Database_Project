import requests

def main():
    print("********* Welcome to use ChatDB *********")
    url = "http://127.0.0.1:5000/"
    cnt = 0
    all_token_cnt = 0
    while True:
        user_query = input("please input your query: ")

        if user_query.lower() in ['exit', 'quit']:
            print("Bye.")
            break

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={"query": user_query}
            )

            if response.status_code == 200:
                result = response.json()
                print("\n ************** LLM generated query **************")
                print(result.get("generated_query", "N/A"))

                print("\n ************** Query result **************")
                output = result.get("results", "")
                if isinstance(output, str):
                    print(output)
                else:
                    for item in output:
                        print(item)

                print("\n ************** Monitor **************")
                print(f'Total queries executed:{cnt+1}')
                print(f'Current tokens used:{result.get("current_tokens_num")}')
                print(f'Total tokens used:{result.get("current_tokens_num") + all_token_cnt}')
            else:
                print(f"❌ Fail: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"⚠️ Error: {e}")
        print("\n")
        cnt += 1
        all_token_cnt += result.get("current_tokens_num")

if __name__ == "__main__":
    main()
