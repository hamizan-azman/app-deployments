from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/api/sitemap", methods=["GET"]) poc1
def sitemap():
    web_path = request.args.get("web_path")
    if not web_path:
        return jsonify({"error": "missing web_path parameter"}), 400
    print(web_path)
    sitemap_loader = SitemapLoader(web_path=web_path)
    docs = sitemap_loader.load()

    results = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs]
    return jsonify({"count": len(results), "docs": results})

@app.route() poc2

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11000)

# curl "http://127.0.0.1:10000/api/sitemap?web_path=http://10.3.228.5:8080/infinite-loop.xml"
