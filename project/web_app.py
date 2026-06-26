import json
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import database

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
PORT = 8080


def send_json_response(handler, data, status=200):
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))


class StudyBotHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/sections":
            sections = database.get_sections()
            send_json_response(self, {"sections": sections})
            return

        if path == "/api/questions":
            section = query.get("section", [""])[0]
            questions = database.get_questions_by_section(section)
            payload = [
                {
                    "id": row[0],
                    "question_uz": row[1],
                    "question_en": row[2],
                    "question_ru": row[3],
                }
                for row in questions
            ]
            send_json_response(self, {"section": section, "questions": payload})
            return

        if path == "/api/question":
            qa_id = query.get("id", [""])[0]
            if not qa_id.isdigit():
                send_json_response(self, {"error": "Missing or invalid question id."}, status=400)
                return
            row = database.get_question_by_id(int(qa_id))
            if not row:
                send_json_response(self, {"error": "Question not found."}, status=404)
                return
            payload = {
                "id": row[0],
                "section": row[1],
                "category": row[2],
                "question_uz": row[3],
                "question_en": row[4],
                "question_ru": row[5],
                "answer_uz": row[6],
                "answer_en": row[7],
                "answer_ru": row[8],
            }
            send_json_response(self, payload)
            return

        if path == "/api/search":
            query_text = query.get("q", [""])[0]
            results = database.search_questions(query_text)
            payload = [
                {
                    "id": row[0],
                    "section": row[1],
                    "category": row[2],
                    "question_uz": row[3],
                    "question_en": row[4],
                    "question_ru": row[5],
                    "answer_uz": row[6],
                    "answer_en": row[7],
                    "answer_ru": row[8],
                }
                for row in results
            ]
            send_json_response(self, {"query": query_text, "results": payload})
            return

        if path == "/api/resources":
            results = database.get_resources()
            payload = [
                {
                    "id": row[0],
                    "section": row[1],
                    "category": row[2],
                    "question_uz": row[3],
                    "question_en": row[4],
                    "question_ru": row[5],
                    "answer_uz": row[6],
                    "answer_en": row[7],
                    "answer_ru": row[8],
                }
                for row in results
            ]
            send_json_response(self, {"resources": payload})
            return

        return super().do_GET()


if __name__ == "__main__":
    database.init_db()
    server = ThreadingHTTPServer(("", PORT), StudyBotHandler)
    print(f"📘 Student Assistant web app is running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
