# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_delete_from_index.py
DESCRIPTION:
    This sample demonstrates how to select and show unique documents on Azure AI Search vector embeddings index. 
    We provided a function to demonstrate how to delete documents from the index one by one.
    ***TEST IT ON A DEV ENVIRONMENT BEFORE YOU RUN IT ON PRODUCTION!!!***
USAGE:
    python sample_delete_from_index.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - the endpoint of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - the name of your search index (e.g. "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - your search API key
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))


def show_all_documents_query():
    # [START show_all_documents_query]

    results = search_client.search(
        select=["title", "chunk_id"]
    )

    # print(f"Result: {results}")
    total_documents = 0 
    for result in results:
        print(f"Title   : {result['title']}")
        # print(f"Chunk_id: {result['chunk_id']}")
        total_documents += 1
    
    print(f"total documents: {total_documents}")
    return results, total_documents
    # [END show_all_documents_query]


def select_unique_title_documents_query():
    # [START select_unique_title_documents_query]

    results = search_client.search(
        select=["title", "chunk_id"]
    )

    unique_title_documents = []
    for result in results:
        if result["title"] not in unique_title_documents:
            # print(f"Adding title: {result['title']}")
            unique_title_documents.append(result["title"])

    print(f"Total unique documents: {len(unique_title_documents)}")
    counter = 1
    for title in unique_title_documents:
        print(f"{counter}. {title}")
        counter += 1

    return unique_title_documents
    # [END select_unique_title_documents_query]


def select_query_by_title(title):
    # [START select_query_by_title]
    results = search_client.search(select=["title", "chunk_id"])

    chunk_ids = [] 
    for result in results:
        if result["title"] == title:
            print("Title: {}".format(result["title"]))
            # print("Chunk_id: {}".format(result["chunk_id"]))
            chunk_ids.append(result["chunk_id"])

    print(f"Total chunk_ids: {len(chunk_ids)}")
    return chunk_ids
    # [END select_query_by_title]


def delete_document(title):
    # [START delete_document]

    chunk_ids = select_query_by_title(title)

    for chunk_id in chunk_ids:
        print(f"---------------------")
        print(f"chunk_id: {chunk_id}")
        result = search_client.delete_documents(documents=[{"chunk_id": chunk_id}])
        print("Deleted document succeeded: {}".format(result[0].succeeded))
    # [END delete_document]


if __name__ == "__main__":
    select_unique_title_documents_query()
    # delete_document("<YOUR DOCUMENT TITLE>")

