"""Graph Reader."""

from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

import yaml

class GraphReader(BaseReader):
    """Graph reader.

    Combines all Graph query results into the Document used by LlamaIndex.

    Args:
        uri (str): Graph Database URI
        username (str): Username
        password (str): Password 

    """

    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str
    ) -> None:
        """Initialize with parameters."""
        try:
            from neo4j import GraphDatabase, basic_auth

        except ImportError:
            raise ImportError(
                "`neo4j` package not found, please run `pip install neo4j`"
            )
        if uri:
            if uri is None:
                raise ValueError("`uri` must be provided.")
            self.client = GraphDatabase.driver(uri=uri, auth=basic_auth(username, password))
            self.database = database
            
    def load_data(
        self, query: str, parameters: Dict = {}
    ) -> List[Document]:
        """Run the Cypher with optional parameters and turn results into documents

        Args:
            query (str): Graph Cypher query string.
            parameters (Dict): optional query parameters.

        Returns:
            List[Document]: A list of documents.

        """

        records, summary, keys = self.client.execute_query(query, parameters, database_ = self.database)

        documents = [Document(yaml.dump(entry.data())) for entry in records]

        return documents