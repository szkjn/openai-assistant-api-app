import openai
import os
import time
import logging
from datetime import datetime

from instructions import instructions

api_key = os.environ.get('OPENAI_API_KEY1')
client = openai.OpenAI(api_key=api_key)
model = "gpt-4-turbo"

# Hardcode assistant ID
assistant_id = "asst_3nU9VuYQgA7J8r2fLj8JjtZu"

# Create a thread
thread = client.beta.threads.create()

# Create a message
test_message = "À quels champs lexicals est associé la figure du cycliste débutant ou anonyme ?"
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = test_message
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id=assistant_id,
    instructions="Tu t'adresses principales à des chercheurs et chercheuses universitaires."
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=2):
    """
    Waits for a run to complete and prints the elapsed time.
    :param client: The Client instance
    :param thread_id: The ID of the thread
    :param run_id: The ID of the run
    :param sleep_interval: Time in seconds to wait between checks
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                
                # Get the messages once the run is completed
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# Run 
wait_for_run_completion(client=client, thread_id=thread.id, run_id=run.id)

# Steps and logs
run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
print(f"Steps ---> {run_steps.data}")


