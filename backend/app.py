from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io

from services.generator import generate_test_cases
from services.feature_writer import write_feature_file, OUTPUT_DIR
from services.gherkin_formatter import format_for_cucumber_behave
from services.behave_packager import build_behave_package, package_filename
from services.story_analyzer import analyze_user_story, format_requirements_for_prompt
from services.coverage_analyzer import analyze_coverage
from services.execution_simulator import simulate_execution

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {
        "message": "Test Case Generator API is running",
        "endpoints": ["/generate", "/analyze-story", "/health", "/download/<file>", "/download-package"],
    }


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/analyze-story", methods=["POST"])
def analyze_story():
    data = request.get_json(silent=True) or {}
    user_story = data.get("userStory", "")

    if not user_story.strip():
        return jsonify({"error": "userStory is required"}), 400

    try:
        return jsonify(analyze_user_story(user_story))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    user_story = data.get("userStory", "")
    save_file = data.get("saveFile", True)
    include_analysis = data.get("includeAnalysis", True)

    if not user_story.strip():
        return jsonify({"error": "userStory is required"}), 400

    try:
        story_analysis = None
        requirements_context = ""

        if include_analysis:
            try:
                story_analysis = analyze_user_story(user_story)
                requirements_context = format_requirements_for_prompt(story_analysis)
            except Exception as exc:
                story_analysis = {"error": str(exc), "quality_score": None}

        result = generate_test_cases(user_story, requirements_context)
        formatted = format_for_cucumber_behave(result["gherkin"], result["feature_name"])

        response = {
            "generated_test_cases": formatted,
            "feature_name": result["feature_name"],
            "model_used": result.get("model_used"),
            "scenario_counts": result.get("scenario_counts", {}),
            "story_analysis": story_analysis,
        }

        if include_analysis:
            try:
                response["coverage_analysis"] = analyze_coverage(user_story, formatted)
            except Exception as exc:
                response["coverage_analysis"] = {"error": str(exc), "coverage_score": None}

            response["execution_simulation"] = simulate_execution(formatted)

        if save_file:
            file_path = write_feature_file(result["gherkin"], result["feature_name"])
            response["feature_file"] = str(file_path)
            response["feature_filename"] = file_path.name

        return jsonify(response)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Generation failed: {exc}"}), 500


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    safe_name = filename.replace("..", "").replace("/", "").replace("\\", "")
    file_path = OUTPUT_DIR / safe_name

    if not file_path.exists() or not file_path.suffix == ".feature":
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True, download_name=safe_name, mimetype="text/plain")


@app.route("/download-package", methods=["POST"])
def download_package_body():
    """Download ZIP with .feature + Behave step defs + Cucumber README."""
    data = request.get_json(silent=True) or {}
    gherkin = data.get("gherkin", "")
    feature_filename = data.get("feature_filename", "generated.feature")
    feature_name = data.get("feature_name", "")

    if not gherkin.strip():
        return jsonify({"error": "gherkin content is required"}), 400

    try:
        zip_bytes = build_behave_package(gherkin, feature_filename, feature_name)
        zip_name = package_filename(feature_filename)
        return send_file(
            io.BytesIO(zip_bytes),
            as_attachment=True,
            download_name=zip_name,
            mimetype="application/zip",
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/download-package/<filename>", methods=["GET"])
def download_package_file(filename):
    """Download ZIP from a previously saved .feature file on the server."""
    safe_name = filename.replace("..", "").replace("/", "").replace("\\", "")
    file_path = OUTPUT_DIR / safe_name

    if not file_path.exists() or file_path.suffix != ".feature":
        return jsonify({"error": "File not found"}), 404

    gherkin = file_path.read_text(encoding="utf-8")
    feature_name = safe_name.replace(".feature", "").replace("_", " ").title()
    zip_bytes = build_behave_package(gherkin, safe_name, feature_name)
    zip_name = package_filename(safe_name)

    return send_file(
        io.BytesIO(zip_bytes),
        as_attachment=True,
        download_name=zip_name,
        mimetype="application/zip",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
