"""
自定义装载器BaseLoader。读取格式特殊的 .log 文件，转换为 Document 对象。
1. 创建一个继承BaseLoader的子类
2. 重写lazy_load方法
"""

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from typing import Iterator
import os

class CustomLogLoader(BaseLoader):
    """
    自定义装载器BaseLoader。读取格式特殊的 .log 文件，转换为 Document 对象。
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        yield 实现了 惰性加载 (Lazy Loading),每次迭代只产生一个 Document
        """
        with open(self.file_path, "r") as f:
            for line in f:
                yield Document(
                    page_content=line,
                    metadata={"source": self.file_path}
                )
                
file_path = r"./docs/押金上发_NOROUTE.LOG"

if not os.path.exists(file_path):
    print(f"文件不存在：{file_path}")
else:   
    loader = CustomLogLoader(file_path)
    docs = loader.lazy_load()
    for doc in docs:
        print(doc)
        # print(doc.metadata)
        # print(doc.page_content)

# page_content='代理报错：
# ' metadata={'source': './docs/押金上发_NOROUTE.LOG'}
# page_content='2015-12-04 14:36:08.750427 debug [] 47206054930176 -> odac_app_lookup_CBsPartitionNotifyInfo, Key is [12102]
# ' metadata={'source': './docs/押金上发_NOROUTE.LOG'}
# page_content='2015-12-04 14:36:08.717790 debug [mdb_proxy, mdbproxy] 47206048622336 -> CRasMonitorMapreduce::map function  entered
# ' metadata={'source': './docs/押金上发_NOROUTE.LOG'}
