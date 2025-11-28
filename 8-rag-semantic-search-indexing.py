"""
RAG语义搜索向量存储。

"""


## 1.加载文档
from langchain_community.document_loaders import PyPDFLoader
import os


file_path = r"./docs/SQL 语句参考.pdf"

if not os.path.exists(file_path):
    print(f"文件不存在：{file_path}")
else:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(len(docs)) # 打印文档数量22页
    # print(docs[0])

# page_content='SQL 语句教程 ......' 
# metadata={
#     'producer': 'Acrobat Distiller 7.0 (Windows)', 
#     'creator': 'Acrobat PDFMaker 7.0 for Word', 
#     'creationdate': '2007-03-12T15:25:54+08:00', 
#     'subject': 'SQL', 
#     '所有者': 'Destino', 
#     'author': 'Destino', 
#     'moddate': '2007-03-12T15:27:23+08:00', 
#     'company': 'Microsoft', 
#     'comments': '关于SQL语法的介绍。', 
#     'sourcemodified': 'D:20070210030442', 
#     'title': 'SQL语句', 
#     '完成日期': '1983-12-20', 
#     'source': './docs/SQL 语句参考.pdf', 
#     'total_pages': 22, 
#     'page': 0, 
#     'page_label': '1'}

## 2.拆分
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = text_splitter.split_documents(docs)
print(len(all_splits))  # 输出分块的数量：47


## 3.嵌入模型
# pip install langchain-ollama
# nomic-embed-text:v1.5
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)
print(f"vector_1 length:{len(vector_1)}")
print(vector_1[:10])
# vector_1 length:768
# [0.015972577, 0.009814614, -0.11629287, -0.02931841, 0.068047225, -0.03182108, 0.043254767, -0.00037423102, 0.041003242, -0.0009468535]

## 4.向量存储
# pip install langchain-chroma
from langchain_chroma import Chroma
vector_store = Chroma(collection_name="example_collection", embedding_function=embeddings, persist_directory="./chroma_langchain_db")
ids = vector_store.add_documents(all_splits)
print(ids[0])
