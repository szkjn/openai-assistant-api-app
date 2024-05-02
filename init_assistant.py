import openai
import os

from instructions import instructions

api_key = os.environ.get('OPENAI_API_KEY1')
client = openai.OpenAI(api_key=api_key)
model = "gpt-4-turbo"

def create_assistant(client, model):

    try:
        assistant = client.beta.assistants.create(
            name="Iris",
            instructions=instructions,
            tools=[{"type": "file_search"}],
            model=model,
        )

        print(f"INIT Assistant : {assistant.id}")
        return assistant
    
    except Exception as e:
        print(f"ERROR while creating assistant: {e}")


def upload_files(client, name, folder_path):

    try:
        vector_store = client.beta.vector_stores.create(name=name)

        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_paths.append(os.path.join(root, file))

        file_streams = [open(path, "rb") for path in file_paths]

        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        print(file_batch.status)
        print(file_batch.file_counts)

        print(f"INIT Vector Store : {vector_store.id}")
        return vector_store
    
    except Exception as e:
        print(f"ERROR while uploading files: {e}")


if __name__ == "__main__":

    try:
        # Create assistant
        assistant= create_assistant(client, model)

        # Upload files and create vector store
        name = "Corpus Miroir du Cyclisme"
        folder_path = "data/Années 1960"
        vector_store = upload_files(client, name, folder_path)

        # Update assistant
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )

    except Exception as e:
        print(f"ERROR while initiating assistant: {e}")

