#!/usr/bin/env python3
"""
Test script to verify the complete integration pipeline
"""
import os
import sys
import json
import subprocess

def test_enhanced_ingestion():
    """Test the enhanced ingestion script"""
    print("🧪 Testing enhanced ingestion...")

    # Run enhanced_ingest.py
    try:
        result = subprocess.run(
            ["python", "enhanced_ingest.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Enhanced ingestion completed successfully")
        print(f"   Output: {result.stdout.strip()}")

        # Check if required files exist
        required_files = ["chunks.json", "vectors.json", "index_info.json"]
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file} created")
            else:
                print(f"❌ {file} missing")
                return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Enhanced ingestion failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def test_vector_search():
    """Test the vector search functionality"""
    print("\n🧪 Testing vector search...")

    try:
        # Import and test vector search
        from vector_search import SimpleVectorStore

        vs = SimpleVectorStore("vectors.json")
        stats = vs.get_stats()

        if stats["status"] == "loaded":
            print(f"✅ Vector store loaded with {stats['total_vectors']} vectors")

            # Test search
            results = vs.similarity_search("benefits", k=3)
            if results:
                print(f"✅ Search returned {len(results)} results")
                print(f"   Top result score: {results[0][2]:.4f}")
                return True
            else:
                print("❌ Search returned no results")
                return False
        else:
            print(f"❌ Vector store not loaded: {stats}")
            return False

    except Exception as e:
        print(f"❌ Vector search test failed: {e}")
        return False

def test_query_system():
    """Test the query system"""
    print("\n🧪 Testing query system...")

    try:
        # Import the query module and test
        import query

        # Test the answer_question function
        answer = query.answer_question("What benefits does Primr offer?")

        if answer and len(answer) > 10:
            print("✅ Query system working")
            print(f"   Sample answer: {answer[:100]}...")
            return True
        else:
            print(f"❌ Query system returned poor answer: {answer}")
            return False

    except Exception as e:
        print(f"❌ Query system test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Primr Slack Assistant Integration")
    print("=" * 50)

    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print(f"📍 Working directory: {os.getcwd()}")

    # Check if we have data files
    data_files = [f for f in os.listdir("data") if f.endswith(('.md', '.txt'))]
    print(f"📄 Found {len(data_files)} data files: {data_files}")

    if not data_files:
        print("❌ No data files found. Please add some .md or .txt files to the data/ directory")
        return False

    # Run tests
    tests = [
        test_enhanced_ingestion,
        test_vector_search,
        test_query_system
    ]

    results = []
    for test in tests:
        success = test()
        results.append(success)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")

    test_names = [
        "Enhanced Ingestion",
        "Vector Search",
        "Query System"
    ]

    all_passed = True
    for i, (name, passed) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 All tests passed! The integration is working correctly.")
        print("\n📋 Next steps:")
        print("   1. Set up Slack bot tokens in .env file")
        print("   2. Start the Slack bot: python slack_bot.py")
        print("   3. Start the Next.js admin UI: npm run dev")
        return True
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
