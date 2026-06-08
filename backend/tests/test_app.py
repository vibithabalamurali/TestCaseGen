"""Pytest suite for Flask API — happy path validation (no live LLM calls)."""

from unittest.mock import patch

import pytest


class TestHealthAndHome:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}

    def test_home_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "/generate" in data["endpoints"]


class TestGenerateEndpoint:
    def test_generate_requires_user_story(self, client):
        response = client.post("/generate", json={})
        assert response.status_code == 400
        assert "userStory" in response.get_json()["error"]

    @patch("app.analyze_coverage")
    @patch("app.analyze_user_story")
    @patch("app.generate_test_cases")
    def test_generate_testcases(
        self,
        mock_generate,
        mock_story,
        mock_coverage,
        client,
        mock_llm_response,
    ):
        mock_generate.return_value = mock_llm_response
        mock_story.return_value = {
            "quality_score": 85,
            "is_ready": True,
            "issues": [],
            "actors": ["registered user"],
            "actions": ["log in"],
            "inputs": ["email", "password"],
            "preconditions": ["user is on login page"],
            "acceptance_criteria": ["valid credentials grant access"],
        }
        mock_coverage.return_value = {
            "coverage_score": 82,
            "covered": ["Login success with valid credentials"],
            "missing": ["SQL injection test"],
            "security_gaps": ["Rate limiting"],
        }

        response = client.post(
            "/generate",
            json={
                "userStory": "As a user, I want to login using email and password",
                "saveFile": False,
                "includeAnalysis": True,
            },
        )

        assert response.status_code == 200
        text = response.get_data(as_text=True)
        assert "Feature" in text
        assert "Scenario" in text
        assert "Given" in text
        assert "When" in text
        assert "Then" in text

        data = response.get_json()
        assert data["feature_name"] == "User Login"
        assert data["scenario_counts"]["positive"] >= 1
        assert data["coverage_analysis"]["coverage_score"] == 82
        assert data["execution_simulation"]["summary"]["total"] == 3


class TestDownloadEndpoints:
    def test_download_package_requires_gherkin(self, client):
        response = client.post("/download-package", json={})
        assert response.status_code == 400

    def test_feature_package_download(self, client, mock_llm_response):
        response = client.post(
            "/download-package",
            json={
                "gherkin": mock_llm_response["gherkin"],
                "feature_filename": "user_login.feature",
                "feature_name": "User Login",
            },
        )

        assert response.status_code == 200
        assert response.content_type == "application/zip"
        assert len(response.data) > 100

    def test_feature_file_download(self, client, mock_llm_response, tmp_path):
        from services.feature_writer import OUTPUT_DIR, write_feature_file

        file_path = write_feature_file(
            mock_llm_response["gherkin"],
            "User Login",
            tmp_path / "user_login.feature",
        )

        with patch("app.OUTPUT_DIR", tmp_path):
            response = client.get(f"/download/{file_path.name}")

        assert response.status_code == 200
        assert "text" in response.content_type
        assert "Feature: User Login" in response.get_data(as_text=True)
