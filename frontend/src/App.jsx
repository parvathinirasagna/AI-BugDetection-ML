import React, { useState } from 'react';
import './App.css';

function App() {
  const [codeInput, setCodeInput] = useState('');
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
      const response = await fetch('http://localhost:8000/detect_bug', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code_snippet: codeInput,
        }),
      });

      if (!response.ok) {
        throw new Error('Backend API error');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to detect bugs');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🔍 AI-Powered Bug Detection</h1>
        <p>Detect potential bugs in your code using ML models</p>
      </header>

      <div className="app-container">
        <div className="left-section">
          <h2>Enter Your Code</h2>
          <textarea
            value={codeInput}
            onChange={(e) => setCodeInput(e.target.value)}
            placeholder="Paste Python code here..."
            style={{
              width: '100%',
              height: '300px',
              padding: '10px',
              fontFamily: 'monospace',
              fontSize: '14px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              marginTop: '10px',
              marginBottom: '15px',
            }}
          />
          <button
            onClick={handleDetectBug}
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '10px 20px',
              backgroundColor: '#667eea',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '16px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1,
            }}
          >
            {isLoading ? 'Analyzing...' : 'Detect Bugs'}
          </button>
        </div>

        <div className="right-section">
          {error && (
            <div className="error-message" style={{ color: '#c33', padding: '10px', backgroundColor: '#fee', borderRadius: '4px' }}>
              ❌ {error}
            </div>
          )}

          {isLoading && (
            <div className="loading-message" style={{ textAlign: 'center', padding: '40px' }}>
              <p>Analyzing code...</p>
            </div>
          )}

          {result && (
            <div style={{ backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '4px' }}>
              <h3>Results</h3>
              <p><strong>Is Bug:</strong> {result.is_bug ? '🔴 YES - Bug Detected' : '🟢 NO - Code OK'}</p>
              <p><strong>Baseline Prediction:</strong> {result.baseline_prediction ? 'Bug' : 'OK'} (Confidence: {(result.confidence_baseline * 100).toFixed(1)}%)</p>
              <p><strong>Improved Prediction:</strong> {result.improved_prediction ? 'Bug' : 'OK'} (Confidence: {(result.confidence_improved * 100).toFixed(1)}%)</p>
            </div>
          )}

          {!result && !isLoading && !error && (
            <div className="empty-state" style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
              <p>👈 Enter code on the left to detect bugs</p>
            </div>
          )}
        </div>
      </div>

      <footer className="app-footer">
        <p>AI Bug Detection • Backend: localhost:8000 | Frontend: localhost:3000</p>
      </footer>
    </div>
  );
}

export default App;
