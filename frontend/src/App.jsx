import { useEffect, useRef, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const emptyUser = { email: '', full_name: '', password: '' };

export default function App() {
  const [authMode, setAuthMode] = useState('login');
  const [userForm, setUserForm] = useState(emptyUser);
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [me, setMe] = useState(null);
  const [status, setStatus] = useState('');
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  useEffect(() => {
    if (token) {
      fetch(`${API_URL}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => (res.ok ? res.json() : Promise.reject()))
        .then((data) => setMe(data))
        .catch(() => setToken(''));
    }
  }, [token]);

  const login = async (event) => {
    event.preventDefault();
    const form = new URLSearchParams();
    form.append('username', userForm.email);
    form.append('password', userForm.password);

    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString(),
    });

    if (!response.ok) {
      setStatus('Login failed');
      return;
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
    setStatus('Logged in successfully');
  };

  const register = async (event) => {
    event.preventDefault();
    const response = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userForm),
    });

    if (!response.ok) {
      const err = await response.json();
      setStatus(err.detail || 'Registration failed');
      return;
    }

    setStatus('Registration successful. Please log in.');
    setAuthMode('login');
    setUserForm({ ...emptyUser, email: userForm.email });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const fileInput = event.target.elements.audio.files[0];
    if (!fileInput) {
      setStatus('Please choose an audio file');
      return;
    }

    const formData = new FormData();
    formData.append('file', fileInput);

    const response = await fetch(`${API_URL}/api/v1/sound/analyze`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      setStatus(data.detail || 'Analysis failed');
      return;
    }

    setResult(data);
    setStatus('Analysis complete');
    fetchHistory();
  };

  const fetchHistory = async () => {
    if (!token) return;
    const response = await fetch(`${API_URL}/api/v1/sound/history`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      const data = await response.json();
      setHistory(data);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [token]);

  const startRecording = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setStatus('Microphone access is not available in this browser');
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;

    const recorder = new MediaRecorder(stream);
    mediaRecorderRef.current = recorder;
    chunksRef.current = [];

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
      }
    };

    recorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      const file = new File([blob], 'stethoscope-recording.webm', { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/api/v1/sound/analyze`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
        setStatus('Recording analyzed');
        fetchHistory();
      } else {
        setStatus(data.detail || 'Unable to analyze recording');
      }

      stream.getTracks().forEach((track) => track.stop());
      setRecording(false);
    };

    recorder.start();
    setRecording(true);
    setStatus('Recording...');
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken('');
    setMe(null);
    setResult(null);
  };

  if (!token || !me) {
    return (
      <div className="app-shell">
        <div className="auth-card">
          <div className="tab-toggle">
            <button className={authMode === 'login' ? 'active' : ''} onClick={() => setAuthMode('login')}>Login</button>
            <button className={authMode === 'register' ? 'active' : ''} onClick={() => setAuthMode('register')}>Register</button>
          </div>

          <h1>Stethoscope Sound Analyzer</h1>

          <form onSubmit={authMode === 'login' ? login : register}>
            {authMode === 'register' && (
              <input
                type="text"
                placeholder="Full name"
                value={userForm.full_name}
                onChange={(e) => setUserForm({ ...userForm, full_name: e.target.value })}
              />
            )}
            <input
              type="email"
              placeholder="Email"
              value={userForm.email}
              onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
            />
            <input
              type="password"
              placeholder="Password"
              value={userForm.password}
              onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
            />
            <button type="submit">{authMode === 'login' ? 'Login' : 'Create account'}</button>
          </form>

          {status && <p className="status">{status}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell dashboard">
      <header className="topbar">
        <div>
          <h2>Welcome, {me.full_name}</h2>
        </div>
        <button className="secondary" onClick={logout}>Logout</button>
      </header>

      <div className="panel-grid">
        <section className="panel">
          <h3>Upload audio</h3>
          <form onSubmit={handleSubmit}>
            <input type="file" name="audio" accept="audio/*" />
            <button type="submit">Analyze sound</button>
          </form>

          <div className="recorder-block">
            <button onClick={recording ? stopRecording : startRecording} className={recording ? 'recording' : ''}>
              {recording ? 'Stop recording' : 'Start microphone recording'}
            </button>
          </div>

          {status && <p className="status">{status}</p>}
        </section>

        <section className="panel result-panel">
          <h3>Prediction</h3>
          {result ? (
            <div className="result-card">
              <p><strong>Sound type:</strong> {result.sound_type}</p>
              <p><strong>Pathology:</strong> {result.predicted_pathology}</p>
              <p><strong>Confidence:</strong> {result.confidence}</p>
              <p><strong>File:</strong> {result.file_name}</p>
            </div>
          ) : (
            <p>No analysis yet.</p>
          )}
        </section>
      </div>

      <section className="panel history-panel">
        <h3>Analysis history</h3>
        {history.length === 0 ? (
          <p>No records yet.</p>
        ) : (
          <ul>
            {history.map((item) => (
              <li key={item.id}>
                <span>{item.file_name}</span>
                <span>{item.sound_type}</span>
                <span>{item.predicted_pathology}</span>
                <span>{item.confidence}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
