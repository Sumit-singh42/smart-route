try:
    print("1. Importing SentenceTransformer...")
    from sentence_transformers import SentenceTransformer
    print("   Success.")
    
    print("2. Importing QdrantClient...")
    from qdrant_client import QdrantClient
    print("   Success.")

    print("3. Initializing Embedding Model (Download might happen here)...")
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
    print("   Success.")

    print("4. Initializing Qdrant (Local)...")
    client = QdrantClient(path="./qdrant_test_data")
    print("   Success.")

    print("5. Test Encoding...")
    vec = model.encode("hello").tolist()
    print(f"   Success. Vector length: {len(vec)}")

except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
