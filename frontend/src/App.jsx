import { useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.DEV ? "/api" : "http://127.0.0.1:5000";

const SAMPLE_STORY = `As a registered user,
I want to log in with my email and password,
So that I can access my account dashboard.

Acceptance Criteria:
- Valid email and password grant access to the dashboard
- Invalid credentials show "Invalid email or password"
- Account locks after 5 failed attempts within 15 minutes
- Empty email or password fields show inline validation errors`;

function ScoreRing({ score, label }) {
  if (score == null) return null;
  const color = score >= 80 ? "good" : score >= 60 ? "warn" : "bad";
  return (
    <div className={`score-ring ${color}`}>
      <span className="score-value">{score}%</span>
      <span className="score-label">{label}</span>
    </div>
  );
}

function App() {
  const [userStory, setUserStory] = useState("");
  const [output, setOutput] = useState("");
  const [featureFilename, setFeatureFilename] = useState("");
  const [featureName, setFeatureName] = useState("");
  const [scenarioCounts, setScenarioCounts] = useState(null);
  const [storyAnalysis, setStoryAnalysis] = useState(null);
  const [coverageAnalysis, setCoverageAnalysis] = useState(null);
  const [executionSimulation, setExecutionSimulation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const generateTestCases = async () => {
    if (!userStory.trim()) {
      setError("Please paste a user story before generating.");
      return;
    }

    setLoading(true);
    setError("");
    setCopied(false);
    setStoryAnalysis(null);
    setCoverageAnalysis(null);
    setExecutionSimulation(null);

    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userStory, saveFile: true, includeAnalysis: true }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate test cases");
      }

      setOutput(data.generated_test_cases);
      setFeatureFilename(data.feature_filename || "generated.feature");
      setFeatureName(data.feature_name || "");
      setScenarioCounts(data.scenario_counts || null);
      setStoryAnalysis(data.story_analysis || null);
      setCoverageAnalysis(data.coverage_analysis || null);
      setExecutionSimulation(data.execution_simulation || null);
    } catch (err) {
      const isNetworkError =
        err instanceof TypeError ||
        err.message === "Failed to fetch" ||
        err.message?.includes("NetworkError");

      setError(
        isNetworkError
          ? "Cannot reach the backend. Run: cd backend → start.bat"
          : err.message || "Something went wrong."
      );
      setOutput("");
      setFeatureFilename("");
      setFeatureName("");
      setScenarioCounts(null);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    if (!output) return;
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadFeatureFile = () => {
    if (!output) return;
    const blob = new Blob([output], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = featureFilename || "generated.feature";
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadBehavePackage = async () => {
    if (!output) return;
    try {
      const response = await fetch(`${API_BASE}/download-package`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          gherkin: output,
          feature_filename: featureFilename || "generated.feature",
          feature_name: featureName,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Package download failed");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = (featureFilename || "generated").replace(".feature", "_cucumber_behave.zip");
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Failed to download Behave package");
    }
  };

  const loadSample = () => {
    setUserStory(SAMPLE_STORY);
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <p className="badge">POC · Infinite Computer Solutions</p>
        <h1>Test Case Generator from User Story</h1>
        <p className="subtitle">
          AI QA platform — analyze user stories, generate Gherkin test cases, score coverage,
          and export Cucumber/Behave-ready packages.
        </p>
      </header>

      <main className="main three-col">
        <section className="panel input-panel">
          <div className="panel-header">
            <h2>User Story</h2>
            <button type="button" className="btn-secondary" onClick={loadSample}>
              Load sample
            </button>
          </div>
          <textarea
            rows={12}
            placeholder="Paste your user story here (As a..., I want..., So that... + acceptance criteria)"
            value={userStory}
            onChange={(e) => setUserStory(e.target.value)}
            disabled={loading}
          />
          <button type="button" className="btn-primary" onClick={generateTestCases} disabled={loading}>
            {loading ? "Analyzing & Generating…" : "Generate Test Cases"}
          </button>
          {error && <p className="error">{error}</p>}
        </section>

        <section className="panel analysis-panel">
          <div className="panel-header">
            <h2>QA Intelligence</h2>
          </div>

          {loading && (
            <p className="loading">Step 1: Story analysis → Step 2: Generate tests → Step 3: Coverage scan…</p>
          )}

          {!loading && !storyAnalysis && !coverageAnalysis && (
            <p className="placeholder">Story quality, coverage score, and simulation appear here after generation.</p>
          )}

          {(storyAnalysis || coverageAnalysis || executionSimulation) && (
            <div className="analysis-content">
              {storyAnalysis && !storyAnalysis.error && (
                <div className="analysis-block">
                  <h3>Story Quality</h3>
                  <ScoreRing score={storyAnalysis.quality_score} label="Quality" />
                  {!storyAnalysis.is_ready && storyAnalysis.issues?.length > 0 && (
                    <ul className="issue-list">
                      {storyAnalysis.issues.map((issue, i) => (
                        <li key={i}>{issue}</li>
                      ))}
                    </ul>
                  )}
                  <div className="req-grid">
                    <div><strong>Actors</strong><p>{storyAnalysis.actors?.join(", ") || "—"}</p></div>
                    <div><strong>Actions</strong><p>{storyAnalysis.actions?.join(", ") || "—"}</p></div>
                    <div><strong>Inputs</strong><p>{storyAnalysis.inputs?.join(", ") || "—"}</p></div>
                  </div>
                </div>
              )}

              {coverageAnalysis && !coverageAnalysis.error && (
                <div className="analysis-block">
                  <h3>Test Coverage</h3>
                  <ScoreRing score={coverageAnalysis.coverage_score} label="Coverage" />
                  {coverageAnalysis.covered?.length > 0 && (
                    <>
                      <p className="list-title covered-title">Covered</p>
                      <ul className="check-list">
                        {coverageAnalysis.covered.map((item, i) => (
                          <li key={i}>✔ {item}</li>
                        ))}
                      </ul>
                    </>
                  )}
                  {coverageAnalysis.missing?.length > 0 && (
                    <>
                      <p className="list-title missing-title">Missing Scenarios</p>
                      <ul className="issue-list">
                        {coverageAnalysis.missing.map((item, i) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </>
                  )}
                  {coverageAnalysis.security_gaps?.length > 0 && (
                    <>
                      <p className="list-title security-title">Security Gaps</p>
                      <ul className="issue-list security">
                        {coverageAnalysis.security_gaps.map((item, i) => (
                          <li key={i}>🔐 {item}</li>
                        ))}
                      </ul>
                    </>
                  )}
                </div>
              )}

              {executionSimulation?.results?.length > 0 && (
                <div className="analysis-block">
                  <h3>Execution Simulation</h3>
                  <p className="sim-summary">
                    {executionSimulation.summary.passed}/{executionSimulation.summary.total} scenarios passed
                  </p>
                  <ul className="sim-list">
                    {executionSimulation.results.map((r, i) => (
                      <li key={i} className={r.status}>
                        {r.status === "passed" ? "✔" : "✘"} {r.scenario}
                        <span className="sim-note">{r.note}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </section>

        <section className="panel output-panel">
          <div className="panel-header">
            <h2>Generated Gherkin</h2>
            {output && (
              <div className="actions">
                <button type="button" className="btn-secondary" onClick={copyToClipboard}>
                  {copied ? "Copied!" : "Copy"}
                </button>
                <button type="button" className="btn-secondary" onClick={downloadFeatureFile}>
                  Download .feature
                </button>
                <button type="button" className="btn-secondary" onClick={downloadBehavePackage}>
                  Cucumber/Behave ZIP
                </button>
              </div>
            )}
          </div>

          {!loading && !output && !error && (
            <p className="placeholder">Gherkin scenarios with @positive, @negative, @edge tags.</p>
          )}

          {output && (
            <div className="output">
              {scenarioCounts && (
                <p className="counts">
                  <span className="tag positive">{scenarioCounts.positive} positive</span>
                  <span className="tag negative">{scenarioCounts.negative} negative</span>
                  <span className="tag edge">{scenarioCounts.edge} edge</span>
                </p>
              )}
              <pre>{output}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
