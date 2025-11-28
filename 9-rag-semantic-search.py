"""
RAG语义搜索。

"""

## 1.文档和文档加载器
from langchain_core.documents import Document

documents = [
    Document(
        page_content=".",
        metadata={"source": "./docs/SQL 语句参考.pdf"}
    ),
    Document(
        page_content=".",
        metadata={"source": "./docs/SQL 语句参考.pdf"}
    )
]

## 2.嵌入模型
# pip install langchain-ollama
# nomic-embed-text:v1.5
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")


## 3.向量查询
# pip install langchain-chroma
from langchain_chroma import Chroma
vector_store = Chroma(collection_name="example_collection", embedding_function=embeddings, persist_directory="./chroma_langchain_db")

# 相识度查询
print("相识度查询")
results = vector_store.similarity_search("外部连接左连接")
for index, result in enumerate(results):
    print(index)
    print(result.page_content[:100])

# 0
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# 1
# SQL语句教程(23) TRIM
# SQL 中的 TRIM 函数是用来移除掉一个字串中的字头或字尾。最常见的用途是移除字首或字尾的空白。这
# 个函数在不同的资料库中有不同的名称：
# MySQL: TRIM
# 2
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 3
# SUBSTR(str,pos,len): 由中的第位置开始，选出接下去的个字元。
# 假设我们有以下的表格：
# Geography 表格
# region_name store_name
# East Bo

# 相识度分数查询
print("相识度分数查询")
results = vector_store.similarity_search_with_score("外部连接左连接")
for doc, score in results:
    print(f"文档内容:{doc.page_content[:100]}")
    print(f"分数:{score}")
# 文档内容:很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# 分数:0.8886711001396179
# 文档内容:SQL语句教程(23) TRIM
# SQL 中的 TRIM 函数是用来移除掉一个字串中的字头或字尾。最常见的用途是移除字首或字尾的空白。这
# 个函数在不同的资料库中有不同的名称：
# MySQL: TRIM
# 分数:0.8887832164764404
# 文档内容:ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 分数:0.899551272392273
# 文档内容:SUBSTR(str,pos,len): 由中的第位置开始，选出接下去的个字元。
# 假设我们有以下的表格：
# Geography 表格
# region_name store_name
# East Bo
# 分数:0.9732035398483276

# 使用向量进行相识度查询
print("使用向量进行相识度查询")
embedding = embeddings.embed_query("外部连接左连接")
results = vector_store.similarity_search_by_vector(embedding)
print(f"共找到{len(results)}个结果")
for index ,result in enumerate(results):
    print(index)
    print(result.page_content[:100])
    
# 使用向量进行相识度查询
# 共找到4个结果
# 0
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# 1
# SQL语句教程(23) TRIM
# SQL 中的 TRIM 函数是用来移除掉一个字串中的字头或字尾。最常见的用途是移除字首或字尾的空白。这
# 个函数在不同的资料库中有不同的名称：
# MySQL: TRIM
# 2
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 3
# SUBSTR(str,pos,len): 由中的第位置开始，选出接下去的个字元。
# 假设我们有以下的表格：
# Geography 表格
# region_name store_name
# East Bo

# 使用chain 进行查询
print("使用chain 进行查询")
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain

@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=3)


results = retriever.batch(
    ["外部连接左连接","右连接"]
)

for index, documents in enumerate(results):
    print(index)
    for document in documents:
        print(document.page_content[:100])

# 使用chain 进行查询
# 0
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# SQL语句教程(23) TRIM
# SQL 中的 TRIM 函数是用来移除掉一个字串中的字头或字尾。最常见的用途是移除字首或字尾的空白。这
# 个函数在不同的资料库中有不同的名称：
# MySQL: TRIM
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 1
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# 请读者注意：在不同的数据库中，日期的储存法可能会有所不同。在这里我们选择了其中一种储存法。
# 结果:
# store_name sales date
# San Diego $250 jan-07-199
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 使用as_retriever 创建向量检索器
print("使用as_retriever 创建向量检索器")
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

results = retriever.batch(
    ["外部连接左连接","右连接"]
)

for index, documents in enumerate(results):
    print(index)
    for document in documents:
        print(document.page_content[:100])
        
# 使用as_retriever 创建向量检索器
# 0
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# SQL语句教程(23) TRIM
# SQL 中的 TRIM 函数是用来移除掉一个字串中的字头或字尾。最常见的用途是移除字首或字尾的空白。这
# 个函数在不同的资料库中有不同的名称：
# MySQL: TRIM
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

# 1
# 很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述
# 请读者注意：在不同的数据库中，日期的储存法可能会有所不同。在这里我们选择了其中一种储存法。
# 结果:
# store_name sales date
# San Diego $250 jan-07-199
# ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT

## 使用MultiQueryRetriever查询扩展
print("使用MultiQueryRetriever查询扩展")
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)

from langchain_classic.retrievers import MultiQueryRetriever
# 使用默认提示词从LLM中生成多个查询
multi_query_retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=llm, parser_key="lines")

original_query = "外部连接左连接"

print(f"原始查询: {original_query}")

docs = multi_query_retriever.invoke(original_query)

print(f"总共找到 {len(docs)} 个结果")

for i, doc in enumerate(docs):
    print(f"\n{i+1}. 来源：{doc.metadata['source']}")
    print(f"内容片段:{doc.page_content[:100]}")
    
# 使用MultiQueryRetriever查询扩展
# 原始查询: 外部连接左连接
# 总共找到 5 个结果

# 1. 来源：./docs/SQL 语句参考.pdf
# 内容片段:ALTER TABLE Customer ADD PRIMARY KEY (SID);
# 请注意，在用 ALTER TABLE 语句来添加主键之前，我们需要确认被用来当做主键的栏位是设定为『NOT


# 2. 来源：./docs/SQL 语句参考.pdf
# 内容片段:很明显地，这就复杂多了。在这里我们可以看到表格别名的功用：它能让 SQL 句容易被了解，尤其是这
# 个 SQL 句含盖好几个不同的表格时。
# 接下来我们看第三行， 就是 WHERE 子句。 这是我们阐述

# 3. 来源：./docs/SQL 语句参考.pdf
# 内容片段:SQL语句教程(25) Create View
# 视观表 (Views) 可以被当作是虚拟表格。它跟表格的不同是，表格中有实际储存资料，而视观表是建立在
# 表格之上的一个架构，它本身并不实际储存资料。


# 4. 来源：./docs/SQL 语句参考.pdf
# 内容片段:请读者注意：在不同的数据库中，日期的储存法可能会有所不同。在这里我们选择了其中一种储存法。
# 结果:
# store_name sales date
# San Diego $250 jan-07-199

# 5. 来源：./docs/SQL 语句参考.pdf
# 内容片段:SQL语句教程(26) Create Index
# 索引 (Index)  可以帮助我们从表格中快速地找到需要的资料。举例来说，假设我们要在一本园艺书中找如
# 何种植青椒的讯息。若这本书没有索引的话，那我