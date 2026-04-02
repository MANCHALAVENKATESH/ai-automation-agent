# test_chromadb.py
import warnings
warnings.filterwarnings("ignore")

import os
import sys

print("Testing ChromaDB fix...")
print("-" * 40)

try:
    import chromadb
    print(f"✅ ChromaDB version: {chromadb.__version__}")

    # Test new client
    client = chromadb.PersistentClient(path="./data/test_chroma")
    print("✅ PersistentClient created")

    # Test collection
    col = client.get_or_create_collection("test_collection")
    print("✅ Collection created")

    # Test adding data
    col.add(
        documents=["Search Python on Google"],
        metadatas=[{"success": "True", "steps": "[]"}],
        ids=["test-1"]
    )
    print("✅ Data added")

    # Test querying
    results = col.query(
        query_texts=["Search JavaScript on Google"],
        n_results=1
    )
    print(f"✅ Query works: {results['documents']}")

    # Test count
    count = col.count()
    print(f"✅ Count works: {count} items")

    # Cleanup test data
    client.delete_collection("test_collection")
    print("✅ Cleanup done")

    print("-" * 40)
    print("🎉 ChromaDB is working correctly!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("-" * 40)
    print("Try: pip install --upgrade chromadb")