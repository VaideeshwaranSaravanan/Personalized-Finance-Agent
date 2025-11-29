from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService


class Helper:
    def Http_options():
        retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
        )
        return retry_config


    def show_python_code_and_result(response):
        for i in range(len(response)):
            # Check if the response contains a valid function call result from the code executor
            if (
                (response[i].content.parts)
                and (response[i].content.parts[0])
                and (response[i].content.parts[0].function_response)
                and (response[i].content.parts[0].function_response.response)
            ):
                response_code = response[i].content.parts[0].function_response.response
                if "result" in response_code and response_code["result"] != "```":
                    if "tool_code" in response_code["result"]:
                        print(
                            "Generated Python Code >> ",
                            response_code["result"].replace("tool_code", ""),
                        )
                    else:
                        print("Generated Python Response >> ", response_code["result"])
