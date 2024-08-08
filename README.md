# python-tidb-chat2sql
利用Python+tidb向量数据库制作文生SQL功能


# LlamaIndex RAG Example with Simple UI

This example demonstrates how to use the LlamaIndex and TiDB Serverless to build a simple RAG(Retrival-Augmented Generation) application with simple UI.

## Prerequisites

- A running TiDB Serverless cluster with vector search enabled
- Python 3.8 or later
- OpenAI [API key](https://platform.openai.com/docs/quickstart)

## Run the example

### Clone this repo

```bash
git clone https://github.com/pingcap/tidb-vector-python.git
```

### Create a virtual environment

```bash
cd tidb-vector-python/examples/llamaindex-tidb-vector-with-ui
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set the environment variables

Get the `OPENAI_API_KEY` from [OpenAI](https://platform.openai.com/docs/quickstart)

Get the `TIDB_HOST`, `TIDB_USERNAME`, and `TIDB_PASSWORD` from the TiDB Cloud console, as described in the [Prerequisites](../README.md#prerequisites) section.

```bash
export OPENAI_API_KEY="sk-*******"
export TIDB_HOST="gateway01.*******.shared.aws.tidbcloud.com"
export TIDB_USERNAME="****.root"
export TIDB_PASSWORD="****"
```

### Prepare data and run the server

```bash
# prepare the data
python app.py prepare

# runserver
python app.py runserver
```

Now you can visit [http://127.0.0.1:3000/](http://127.0.0.1:3000/) to interact with the RAG application.