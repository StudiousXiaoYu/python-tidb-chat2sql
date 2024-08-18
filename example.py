from sentence_transformers import SentenceTransformer
import os
import sys
import click
import uvicorn
from fastapi import FastAPI, Request, Body
import uuid
from sqlalchemy import URL
import logging
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

# Load the connection string from the .env file
# 设置环境变量
# os.environ['OPENAI_API_BASE'] = ''
# os.environ['OPENAI_API_KEY'] =''
# os.environ['TIDB_HOST'] = ''
# os.environ['TIDB_USERNAME'] = ''
# os.environ['TIDB_PASSWORD'] = ''

MAX_MESSAGES = 10  # 例如，我们想要数组最大长度为10
messages = []

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

logger.info("Downloading and loading the embedding model...")
embed_model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L12-cos-v5", trust_remote_code=True)
embed_model_dims = embed_model.get_sentence_embedding_dimension()

def text_to_embedding(text):
    """Generates vector embeddings for the given text."""
    embedding = embed_model.encode(text)
    return embedding.tolist()

def generate_uuid():
    unique_id = uuid.uuid4()
    return str(unique_id)

def add_message(message):
    if len(messages) >= MAX_MESSAGES:
        messages.pop(0)  # 移除第一个元素
    messages.append(message)  # 添加新元素到末尾
logger.info("Initializing TiDB Vector Store....")
tidb_connection_url = URL(
    "mysql+pymysql",
    username=os.environ['TIDB_USERNAME'],
    password=os.environ['TIDB_PASSWORD'],
    host=os.environ['TIDB_HOST'],
    port=4000,
    database="test",
    query={"ssl_verify_cert": True, "ssl_verify_identity": True},
)

vector_store = TiDBVectorClient(
   # The table which will store the vector data.
   table_name='embedded_documents',
   # The connection string to the TiDB cluster.
   connection_string=tidb_connection_url,
   # The dimension of the vector generated by the embedding model.
   vector_dimension=embed_model_dims,
   # Determine whether to recreate the table if it already exists.
   drop_existing_table=False,
)
def text_to_insert_by_example():
    documents = [
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Enrollments (
                            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID，自增主键',
                            student_id INT COMMENT '学生ID（参考学生表中的ID）',
                            course_id INT COMMENT '课程ID（参考课程表中的ID）',
                            enroll_date DATE NOT NULL COMMENT '注册日期',
                            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                            create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                            update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                        );""",
            "embedding": text_to_embedding("""CREATE TABLE Enrollments (
                            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID，自增主键',
                            student_id INT COMMENT '学生ID（参考学生表中的ID）',
                            course_id INT COMMENT '课程ID（参考课程表中的ID）',
                            enroll_date DATE NOT NULL COMMENT '注册日期',
                            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                            create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                            update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                        );"""),
            "metadata": {"remark": "学生-课程关联表（Enrollments）"},
        },
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Courses (
                        id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID，自增主键',
                        course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
                        credits INT NOT NULL COMMENT '学分',
                        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                        update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                    );""",
            "embedding": text_to_embedding("""CREATE TABLE Courses (
                        id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID，自增主键',
                        course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
                        credits INT NOT NULL COMMENT '学分',
                        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                        update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                    );"""),
            "metadata": {"remark": "课程信息表（Courses）"},
        },
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Classrooms (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教室ID，自增主键',
                    room_number VARCHAR(20) UNIQUE NOT NULL COMMENT '教室房间号',
                    capacity INT NOT NULL COMMENT '教室容量',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );""",
            "embedding": text_to_embedding("""CREATE TABLE Classrooms (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教室ID，自增主键',
                    room_number VARCHAR(20) UNIQUE NOT NULL COMMENT '教室房间号',
                    capacity INT NOT NULL COMMENT '教室容量',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );"""),
            "metadata": {"remark": "教室信息表（Classrooms）"},
        },
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Classes (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '班级ID，自增主键',
                    class_name VARCHAR(50) NOT NULL COMMENT '班级名称',
                    teacher_id INT COMMENT '教师ID（参考教师表中的ID）',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );""",
            "embedding": text_to_embedding("""CREATE TABLE Classes (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '班级ID，自增主键',
                    class_name VARCHAR(50) NOT NULL COMMENT '班级名称',
                    teacher_id INT COMMENT '教师ID（参考教师表中的ID）',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );"""),
            "metadata": {"remark": "班级信息表（Classes）"},
        },
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Students (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '学生ID，自增主键',
                    first_name VARCHAR(50) NOT NULL COMMENT '学生名字',
                    last_name VARCHAR(50) NOT NULL COMMENT '学生姓氏',
                    dob DATE NOT NULL COMMENT '出生日期',
                    email VARCHAR(100) UNIQUE NULL COMMENT '学生电子邮件',
                    phone VARCHAR(20) NULL COMMENT '学生电话',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );""",
            "embedding": text_to_embedding("""CREATE TABLE Students (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '学生ID，自增主键',
                    first_name VARCHAR(50) NOT NULL COMMENT '学生名字',
                    last_name VARCHAR(50) NOT NULL COMMENT '学生姓氏',
                    dob DATE NOT NULL COMMENT '出生日期',
                    email VARCHAR(100) UNIQUE NULL COMMENT '学生电子邮件',
                    phone VARCHAR(20) NULL COMMENT '学生电话',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );"""),
            "metadata": {"remark": "学生信息表（Students）"},
        },
        {
            "id": generate_uuid(),
            "text": """CREATE TABLE Teachers (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教师ID，自增主键',
                    first_name VARCHAR(50) NOT NULL COMMENT '教师名字',
                    last_name VARCHAR(50) NOT NULL COMMENT '教师姓氏',
                    email VARCHAR(100) UNIQUE NOT NULL COMMENT '教师电子邮件',
                    phone VARCHAR(20) NULL COMMENT '教师电话',
                    hire_date DATE NOT NULL COMMENT '入职日期',
                    department VARCHAR(50) NULL COMMENT '所在部门',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );""",
            "embedding": text_to_embedding("""CREATE TABLE Teachers (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教师ID，自增主键',
                    first_name VARCHAR(50) NOT NULL COMMENT '教师名字',
                    last_name VARCHAR(50) NOT NULL COMMENT '教师姓氏',
                    email VARCHAR(100) UNIQUE NOT NULL COMMENT '教师电子邮件',
                    phone VARCHAR(20) NULL COMMENT '教师电话',
                    hire_date DATE NOT NULL COMMENT '入职日期',
                    department VARCHAR(50) NULL COMMENT '所在部门',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    create_user VARCHAR(50) NOT NULL COMMENT '创建用户',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
                    update_user VARCHAR(50) NOT NULL COMMENT '更新用户'
                );"""),
            "metadata": {"remark": "教师信息表（Teachers）"},
        },
    ]

    vector_store.insert(
        ids=[doc["id"] for doc in documents],
        texts=[doc["text"] for doc in documents],
        embeddings=[doc["embedding"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
    )

def print_result(query, result):
   print(f"Search result (\"{query}\"):")
   resultStr = ""
   for r in result:
      resultStr += f"- text: \"{r.document}\", distance: {r.distance}"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/ask')
async def ask(query: str):
    query_embedding = text_to_embedding(query)
    search_result = vector_store.query(query_embedding, k=3)
    gem_result = print_result(query, search_result)
    my_content=f"""请你根据提供的知识库参考片段，回答用户的问题。如果提供的参考内容无法回答用户问题，请回复【该内容并未匹配任何内容，请维护相关知识点后再查询】。
            """
    query = f"""用户问题如下：{query}， 知识库参考片段如下：{gem_result}"""
    logger.info(query)
    llm = OpenAI()
    add_message(ChatMessage(role="user", content=query))
    messages.insert(0,ChatMessage(
            role="system", content = my_content
        ),)
    result_content = llm.chat(messages).message.content
    if gem_result :
        result_content += "[1]"
    resp = {
        "data": result_content,
        "link": gem_result
    }
    return JSONResponse(content=resp)

@click.group(context_settings={'max_content_width': 150})
def cli():
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help="Host, default=127.0.0.1")
@click.option('--port', default=3000, help="Port, default=3000")
@click.option('--reload', is_flag=True, help="Enable auto-reload")
def runserver(host, port, reload):
    uvicorn.run(
        "__main__:app", host=host, port=port, reload=reload,
        log_level="debug", workers=1,
    )


@cli.command()
def prepare():
    text_to_insert_by_example()


if __name__ == '__main__':
    cli()