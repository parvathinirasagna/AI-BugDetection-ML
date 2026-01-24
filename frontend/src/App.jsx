import React, { useState } from 'react';
import './App.css';

function App() {
  const [codeInput, setCodeInput] = useState('');
  const [language, setLanguage] = useState('python');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDetectBug = async () => {
    if (!codeInput.trim()) {
      setError('Please enter code to analyze');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze-multilang', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code_snippet: codeInput,
          language: language,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze code');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const renderBugStatus = () => {
    if (!result) return null;

    const isBug = result.is_bug;
    const icon = isBug ? '🔴' : '✅';
    const status = isBug ? 'BUG DETECTED' : 'NO BUG DETECTED';
    const statusClass = isBug ? 'bug-status bug' : 'bug-status safe';

    return <div className={statusClass}>{icon} {status}</div>;
  };

  const renderConfidence = () => {
    if (!result) return null;

    const baseline = result.baseline_confidence || 0;
    const improved = result.improved_confidence || 0;

    return (
      <div className="confidence-container">
        <div className="model-prediction">
          <h3>Baseline Model (Nadim & Roy 2022)</h3>
          <div className="confidence-bar">
            <div 
              className="confidence-fill baseline" 
              style={{ width: `${baseline}%` }}
            ></div>
          </div>
          <p className="confidence-text">{baseline.toFixed(1)}% Confidence</p>
        </div>

        <div className="model-prediction">
          <h3>Improved Model (CodeBERT + Ensemble)</h3>
          <div className="confidence-bar">
            <div 
              className="confidence-fill improved" 
              style={{ width: `${improved}%` }}
            ></div>
          </div>
          <p className="confidence-text">{improved.toFixed(1)}% Confidence</p>
        </div>

        {improved > baseline && (
          <div className="improvement-badge">
            📈 Improvement: +{(improved - baseline).toFixed(1)}%
          </div>
        )}
      </div>
    );
  };

  const renderBugExplanation = () => {
    if (!result || !result.is_bug) return null;

    const explanation = result.explanation || result.bug_type || 'Bug detected in code';
    const bugDetails = result.bug_details || [];

    return (
      <div className="bug-explanation">
        <h3>🐛 Why This Code is Wrong:</h3>
        <p className="explanation-main">{explanation}</p>
        
        {bugDetails && bugDetails.length > 0 && (
          <div className="bug-details">
            <h4>Detected Issues:</h4>
            <ul>
              {bugDetails.map((detail, idx) => (
                <li key={idx}>{detail}</li>
              ))}
            </ul>
          </div>
        )}

        {result.suggestion && (
          <div className="suggestion">
            <h4>💡 Suggestion:</h4>
            <p>{result.suggestion}</p>
          </div>
        )}
      </div>
    );
  };

  const renderLanguageIcon = () => {
    const icons = {
      python: '🐍',
      java: '☕',
      cpp: '⚙️',
    };
    return icons[language] || '💻';
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🔍 AI-Powered Bug Detection</h1>
        <p>Detect potential bugs in your code using ML models</p>
        <p className="powered-by">Backend: localhost:8000 | Frontend: localhost:3000</p>
      </header>

      <div className="main-content">
        <div className="input-section">
          <div className="language-selector">
            <label>Language: {renderLanguageIcon()}</label>
            <select 
              value={language} 
              onChange={(e) => setLanguage(e.target.value)}
              className="language-select"
            >
              <option value="python">Python 🐍</option>
              <option value="java">Java ☕</option>
              <option value="cpp">C++ ⚙️</option>
            </select>
          </div>

          <div className="code-input-wrapper">
            <label>Enter Your Code</label>
            <textarea
              value={codeInput}
              onChange={(e) => setCodeInput(e.target.value)}
              placeholder={`Paste your ${language} code here...`}
              className="code-input"
              rows="12"
            />
          </div>

          <button 
            onClick={handleDetectBug}
            disabled={isLoading}
            className="detect-button"
          >
            {isLoading ? '🔄 Analyzing...' : '🔍 Detect Bugs'}
          </button>

          {error && <div className="error-message">❌ {error}</div>}
        </div>

        <div className="results-section">
          <h2>Results</h2>
          
          {!result ? (
            <div className="no-results">
              <p>Submit code to see analysis results...</p>
            </div>
          ) : (
            <>
              {renderBugStatus()}
              {renderConfidence()}
              {renderBugExplanation()}
              
              {result.language_detected && (
                <div className="metadata">
                  <p><strong>Detected Language:</strong> {result.language_detected}</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
