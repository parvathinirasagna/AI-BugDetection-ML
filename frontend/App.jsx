import React, { useState } from 'react';
import './App.css';
import BugDetectorForm from './components/BugDetectorForm';
import ResultDisplay from './components/ResultDisplay';
import ModelComparison from './components/ModelComparison';

function App() {
  const [detectionResult, setDetectionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [models, setModels] = useState('both'); // 'baseline', 'improved', or 'both'

  const handleDetectBug = async (codeSnippet) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/detect_bug', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code_snippet: codeSnippet,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to detect bugs');
      }

      const data = await response.json();
      setDetectionResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while detecting bugs');
      setDetectionResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🔍 AI-Powered Bug Detection System</h1>
        <p>Detect potential bugs and issues in your source code using machine learning</p>
      </header>

      <div className="app-container">
        <div className="left-section">
          <BugDetectorForm onDetect={handleDetectBug} isLoading={isLoading} />
        </div>

        <div className="right-section">
          {error && (
            <div className="error-message">
              <span>❌ Error: {error}</span>
            </div>
          )}

          {detectionResult && (
            <>
              <ResultDisplay result={detectionResult} />
              <ModelComparison 
                baseline={detectionResult.baseline_detection}
                improved={detectionResult.improved_detection}
                consensus={detectionResult.consensus}
              />
            </>
          )}

          {isLoading && (
            <div className="loading-message">
              <div className="spinner"></div>
              <p>Analyzing code... Please wait</p>
            </div>
          )}

          {!detectionResult && !isLoading && !error && (
            <div className="empty-state">
              <p>👈 Enter your code snippet on the left to detect bugs</p>
              <p>The system will analyze using both baseline and improved models</p>
            </div>
          )}
        </div>
      </div>

      <footer className="app-footer">
        <p>AI Bug Detection ML • Nadim & Roy (2022) Baseline + Improved Models</p>
        <p>Models: Random Forest + CodeBERT Embeddings + Ensemble Methods</p>
      </footer>
    </div>
  );
}

export default App;
