# 🎯 COMPLETE PROJECT SOURCE CODE

## 🔧 ALL FILES NEEDED - COPY & PASTE TO CREATE LOCALLY

---

## FILE STRUCTURE TO CREATE

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── client.js
│   ├── components/
│   │   ├── UploadCode.jsx
│   │   ├── ModelComparison.jsx
│   │   ├── ResultsTable.jsx
│   │   └── MetricsDisplay.jsx
│   ├── App.jsx
│   ├── index.js
│   └── index.css
├── .env
└── package.json (ALREADY UPLOADED)
```

---

## FILE 1: public/index.html

```html
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="theme-color" content="#000000"/><title>AI Bug Detection - Model Comparison</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}</style></head><body><div id="root"></div></body></html>
```

---

## FILE 2: src/index.js

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<React.StrictMode><App /></React.StrictMode>);
```

---

## FILE 3: src/index.css

```css
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
.container{max-width:1200px;margin:0 auto}
.header{background:white;padding:30px;border-radius:10px;box-shadow:0 4px 6px rgba(0,0,0,0.1);margin-bottom:30px;text-align:center}
.header h1{color:#333;font-size:28px;margin-bottom:10px}
.header p{color:#666;font-size:14px}
.main-content{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
.card{background:white;border-radius:10px;padding:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1)}
.card h2{color:#333;margin-bottom:15px;font-size:18px;border-bottom:2px solid #667eea;padding-bottom:10px}
textarea{width:100%;min-height:200px;padding:12px;border:1px solid #ddd;border-radius:5px;font-family:monospace;font-size:13px;resize:vertical}
button{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:12px 30px;border:none;border-radius:5px;cursor:pointer;font-size:14px;font-weight:600;margin-top:10px;transition:transform 0.2s}
button:hover{transform:translateY(-2px);box-shadow:0 6px 12px rgba(0,0,0,0.15)}
button:disabled{opacity:0.6;cursor:not-allowed}
.metric-row{display:flex;justify-content:space-between;padding:12px;border-bottom:1px solid #eee}
.metric-label{font-weight:600;color:#333}
.metric-value{color:#667eea}
.loading{text-align:center;padding:40px;color:#667eea}
.error{background:#fee;color:#c33;padding:15px;border-radius:5px;margin-top:10px;border-left:4px solid #c33}
.success{background:#efe;color:#3a3;padding:15px;border-radius:5px;margin-top:10px;border-left:4px solid #3a3}
@media(max-width:768px){.main-content{grid-template-columns:1fr}}
```

---

## FILE 4: src/api/client.js (KEY - API CONNECTIONS)

```javascript
import axios from 'axios';
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const apiClient = axios.create({baseURL:API_BASE,headers:{'Content-Type':'application/json'}});
apiClient.interceptors.response.use(response=>response,error=>{console.error('API Error:',error);return Promise.reject(error)});
export const bugDetectionAPI={predictBaseline:(codeContent,fileName='code.py')=>apiClient.post('/predict/baseline',{code_content:codeContent,file_name:fileName}),predictImproved:(codeContent,fileName='code.py')=>apiClient.post('/predict/improved',{code_content:codeContent,file_name:fileName}),compareModels:(codeContent,fileName='code.py')=>apiClient.post('/compare',{code_content:codeContent,file_name:fileName}),getMetrics:()=>apiClient.get('/metrics'),getHistory:(limit=10)=>apiClient.get(`/history?limit=${limit}`),healthCheck:()=>apiClient.get('/health')};
export default apiClient;
```

---

## FILE 5: src/App.jsx (MAIN APP)

```javascript
import React,{useState,useEffect} from 'react';
import{bugDetectionAPI}from'./api/client';
import UploadCode from'./components/UploadCode';
import ModelComparison from'./components/ModelComparison';
import ResultsTable from'./components/ResultsTable';
import MetricsDisplay from'./components/MetricsDisplay';
function App(){const[results,setResults]=useState(null);const[metrics,setMetrics]=useState(null);const[loading,setLoading]=useState(false);const[error,setError]=useState(null);useEffect(()=>{fetchMetrics();checkHealth()},[]);const checkHealth=async()=>{try{await bugDetectionAPI.healthCheck();console.log('✅ Backend running')}catch(err){setError('Backend not running. Start with: python -m app.main')}};const fetchMetrics=async()=>{try{const response=await bugDetectionAPI.getMetrics();setMetrics(response.data)}catch(err){console.error('Error:',err)}};const handleCompare=async(codeContent,fileName)=>{setLoading(true);setError(null);try{const response=await bugDetectionAPI.compareModels(codeContent,fileName);setResults(response.data)}catch(err){setError(err.response?.data?.detail||err.message||'Error analyzing')}finally{setLoading(false)}};return(<div className='container'><div className='header'><h1>🚀 AI Bug Detection</h1><p>Baseline vs Improved Model Comparison</p></div>{error&&<div className='error'>{error}</div>}<div className='main-content'><UploadCode onAnalyze={handleCompare}loading={loading}/><ModelComparison results={results}loading={loading}/></div>{results&&(<><ResultsTable results={results}/><MetricsDisplay metrics={metrics}results={results}/></>)}</div>)}
export default App;
```

---

## FILE 6: src/components/UploadCode.jsx

```javascript
import React,{useState}from'react';
function UploadCode({onAnalyze,loading}){const[code,setCode]=useState('');const[fileName,setFileName]=useState('code.py');const handleAnalyze=()=>{if(!code.trim()){alert('Enter code');return}onAnalyze(code,fileName)};return(<div className='card'><h2>📝 Enter Code</h2><input type='text'placeholder='File name'value={fileName}onChange={(e)=>setFileName(e.target.value)}style={{width:'100%',padding:'8px',marginBottom:'10px'}}/><textarea value={code}onChange={(e)=>setCode(e.target.value)}placeholder='Paste code here...'disabled={loading}/><button onClick={handleAnalyze}disabled={loading}>{loading?'⏳ Analyzing...':'🔍 Analyze'}</button></div>)}
export default UploadCode;
```

---

## FILE 7: src/components/ModelComparison.jsx

```javascript
import React from'react';
function ModelComparison({results,loading}){if(loading)return<div className='loading'>⏳ Analyzing...</div>;if(!results)return<div className='card'><h2>📊 Results</h2><p>Upload code to see results</p></div>;const getColor=(prob)=>prob>0.7?'#c33':prob>0.4?'#f90':'#3a3';return(<div className='card'><h2>📊 Results</h2><div style={{marginTop:'20px'}}><h3 style={{color:'#667eea',marginBottom:'10px'}}>Baseline</h3><div className='metric-row'><span>Prediction:</span><span style={{color:getColor(results.baseline.bug_probability),fontWeight:'bold'}}>{results.baseline.prediction}</span></div><div className='metric-row'><span>Probability:</span><span style={{color:getColor(results.baseline.bug_probability)}}>{(results.baseline.bug_probability*100).toFixed(1)}%</span></div><div className='metric-row'><span>Confidence:</span><span>{(results.baseline.confidence*100).toFixed(1)}%</span></div></div><div style={{marginTop:'20px'}}><h3 style={{color:'#667eea',marginBottom:'10px'}}>Improved</h3><div className='metric-row'><span>Prediction:</span><span style={{color:getColor(results.improved.bug_probability),fontWeight:'bold'}}>{results.improved.prediction}</span></div><div className='metric-row'><span>Probability:</span><span style={{color:getColor(results.improved.bug_probability)}}>{(results.improved.bug_probability*100).toFixed(1)}%</span></div><div className='metric-row'><span>Confidence:</span><span>{(results.improved.confidence*100).toFixed(1)}%</span></div></div></div>)}
export default ModelComparison;
```

---

## FILE 8: src/components/ResultsTable.jsx

```javascript
import React from'react';
function ResultsTable({results}){return(<div className='card'><h2>📋 Detailed Results</h2><div className='metric-row'><span>Agreement:</span><span>{results.agreement?'✅ Yes':'❌ No'}</span></div><div className='metric-row'><span>Baseline Execution Time:</span><span>{results.baseline.execution_time.toFixed(3)}s</span></div><div className='metric-row'><span>Improved Execution Time:</span><span>{results.improved.execution_time.toFixed(3)}s</span></div><div className='metric-row'><span>Time Difference:</span><span>{(results.improved.execution_time-results.baseline.execution_time).toFixed(3)}s</span></div></div>)}
export default ResultsTable;
```

---

## FILE 9: src/components/MetricsDisplay.jsx

```javascript
import React from'react';
function MetricsDisplay({metrics,results}){if(!metrics)return null;return(<div className='card'><h2>📈 Model Performance Metrics</h2><div><h3 style={{marginTop:'15px',color:'#667eea'}}>Baseline Model</h3><div className='metric-row'><span>Accuracy:</span><span>{(metrics.baseline.accuracy*100).toFixed(1)}%</span></div><div className='metric-row'><span>F1-Score:</span><span>{metrics.baseline.f1_score.toFixed(3)}</span></div><div className='metric-row'><span>AUC-ROC:</span><span>{metrics.baseline.auc_roc.toFixed(3)}</span></div></div><div><h3 style={{marginTop:'15px',color:'#667eea'}}>Improved Model</h3><div className='metric-row'><span>Accuracy:</span><span style={{color:'#3a3'}}>{(metrics.improved.accuracy*100).toFixed(1)}%</span></div><div className='metric-row'><span>F1-Score:</span><span style={{color:'#3a3'}}>{metrics.improved.f1_score.toFixed(3)}</span></div><div className='metric-row'><span>AUC-ROC:</span><span style={{color:'#3a3'}}>{metrics.improved.auc_roc.toFixed(3)}</span></div></div><div><h3 style={{marginTop:'15px',color:'#667eea'}}>Improvement</h3><div className='metric-row'><span>Accuracy Gain:</span><span style={{color:'#3a3'}}>+{((metrics.improved.accuracy-metrics.baseline.accuracy)*100).toFixed(1)}%</span></div><div className='metric-row'><span>F1-Score Gain:</span><span style={{color:'#3a3'}}>+{(metrics.improved.f1_score-metrics.baseline.f1_score).toFixed(3)}</span></div></div></div>)}
export default MetricsDisplay;
```

---

## SETUP INSTRUCTIONS

### Step 1: Create All Files
Copy each file section above and create the corresponding file in your project

### Step 2: Install Dependencies
```bash
cd frontend
npm install
```

### Step 3: Start Frontend
```bash
npm start
```

App runs at: **http://localhost:3000**

### Step 4: Start Backend (Separate Terminal)
```bash
cd backend
python -m app.main
```

API runs at: **http://localhost:8000**

---

✅ ALL FILES COMPLETE AND READY TO USE
