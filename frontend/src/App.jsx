import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  const [view, setView] = useState(token ? 'chat' : 'login');
  
  // Auth Form Inputs
  const [authForm, setAuthForm] = useState({ username: '', password: '', email: '' });
  const [authError, setAuthError] = useState('');
  
  // Chat States
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [serverStatus, setServerStatus] = useState('checking'); // checking, online, offline
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/admin/')
      .then(() => setServerStatus('online'))
      .catch((err) => {
        if (err.response) {
          setServerStatus('online'); 
        } else {
          setServerStatus('offline');
        }
      });
  }, []);

  useEffect(() => {
    if (token && view === 'chat') {
      // Deferring loading state update to microtask queue to avoid cascading render warnings
      Promise.resolve().then(() => setLoading(true));
      
      axios.get('http://127.0.0.1:8000/api/chat/history/', {
        headers: { Authorization: `Token ${token}` }
      })
      .then((res) => {
        const formattedHistory = [];
        res.data.forEach((msg) => {
          formattedHistory.push({ text: msg.message, sender: 'user', time: msg.timestamp });
          formattedHistory.push({ text: msg.reply, sender: 'bot', time: msg.timestamp });
        });
        
        if (formattedHistory.length === 0) {
          setMessages([
            {
              text: `Welcome back, ${username}! I am SmartAssist. Ask me anything, and our chats will be logged securely in our SQLite database.`,
              sender: 'bot',
              time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }
          ]);
        } else {
          setMessages(formattedHistory);
        }
      })
      .catch((err) => {
        console.error("Failed to load chat history:", err);
      })
      .finally(() => {
        setLoading(false);
      });
    }
  }, [token, view, username]);

  const handleAuth = async (e) => {
    e.preventDefault();
    setAuthError('');
    const endpoint = view === 'login' ? 'login' : 'register';
    
    try {
      const res = await axios.post(`http://127.0.0.1:8000/api/${endpoint}/`, authForm);
      const receivedToken = res.data.token;
      const receivedUser = res.data.username;
      
      localStorage.setItem('token', receivedToken);
      localStorage.setItem('username', receivedUser);
      
      setToken(receivedToken);
      setUsername(receivedUser);
      setAuthForm({ username: '', password: '', email: '' });
      setView('chat');
    } catch (err) {
      setAuthError(err.response?.data?.error || 'Authentication failed. Please check inputs.');
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { text: input, sender: 'user', time: currentTime };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/chat/', 
        { message: input },
        { headers: { Authorization: `Token ${token}` } }
      );
      
      const botMsg = { 
        text: res.data.reply, 
        sender: 'bot', 
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = { 
        text: "Error generating response. Please check your network and Gemini API key config.", 
        sender: 'bot', 
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setToken('');
    setUsername('');
    setMessages([]);
    setView('login');
  };

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      backgroundColor: '#121214',
      color: '#e1e1e6',
      fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    },
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '16px 24px',
      backgroundColor: '#1a1a1e',
      borderBottom: '1px solid #29292e',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    },
    headerTitle: {
      margin: 0,
      fontSize: '1.25rem',
      fontWeight: '600',
    },
    statusBadge: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontSize: '0.85rem',
      padding: '4px 12px',
      borderRadius: '20px',
      backgroundColor: '#29292e',
    },
    statusDot: {
      width: '8px',
      height: '8px',
      borderRadius: '50%',
      backgroundColor: serverStatus === 'online' ? '#4caf50' : serverStatus === 'offline' ? '#f44336' : '#ffeb3b',
      boxShadow: serverStatus === 'online' ? '0 0 8px #4caf50' : 'none',
    },
    authContainer: {
      display: 'flex',
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      padding: '24px',
    },
    authCard: {
      width: '100%',
      maxWidth: '400px',
      backgroundColor: '#1a1a1e',
      border: '1px solid #29292e',
      borderRadius: '16px',
      padding: '32px',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    },
    formGroup: {
      marginBottom: '20px',
    },
    label: {
      display: 'block',
      marginBottom: '8px',
      fontSize: '0.9rem',
      color: '#a0a0ab',
    },
    input: {
      width: '100%',
      padding: '12px 16px',
      borderRadius: '8px',
      border: '1px solid #29292e',
      backgroundColor: '#202024',
      color: '#ffffff',
      fontSize: '0.95rem',
      outline: 'none',
      boxSizing: 'border-box',
    },
    button: {
      width: '100%',
      padding: '14px',
      borderRadius: '8px',
      border: 'none',
      backgroundColor: '#0070f3',
      color: '#ffffff',
      fontSize: '1rem',
      fontWeight: '600',
      cursor: 'pointer',
      marginTop: '10px',
      transition: 'background-color 0.2s',
    },
    logoutBtn: {
      backgroundColor: 'transparent',
      border: '1px solid #ff4d4d',
      color: '#ff4d4d',
      padding: '6px 12px',
      borderRadius: '6px',
      cursor: 'pointer',
      fontSize: '0.85rem',
      fontWeight: '600',
      marginLeft: '12px',
    },
    chatArea: {
      flex: 1,
      overflowY: 'auto',
      padding: '24px',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
    },
    messageRow: (sender) => ({
      display: 'flex',
      justifyContent: sender === 'user' ? 'flex-end' : 'flex-start',
      width: '100%',
    }),
    messageBubble: (sender) => ({
      maxWidth: '75%',
      padding: '12px 16px',
      borderRadius: sender === 'user' ? '18px 18px 2px 18px' : '18px 18px 18px 2px',
      backgroundColor: sender === 'user' ? '#0070f3' : '#202024',
      color: sender === 'user' ? '#ffffff' : '#e1e1e6',
      boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
    }),
    messageText: {
      margin: 0,
      fontSize: '0.95rem',
      lineHeight: '1.5',
      whiteSpace: 'pre-line',
    },
    messageTime: {
      display: 'block',
      textAlign: 'right',
      fontSize: '0.75rem',
      color: 'rgba(255, 255, 255, 0.5)',
      marginTop: '4px',
    },
    botTime: {
      display: 'block',
      textAlign: 'right',
      fontSize: '0.75rem',
      color: '#8e8e93',
      marginTop: '4px',
    },
    inputForm: {
      padding: '16px 24px',
      backgroundColor: '#1a1a1e',
      borderTop: '1px solid #29292e',
      display: 'flex',
      gap: '12px',
    },
    chatInput: {
      flex: 1,
      padding: '14px 20px',
      borderRadius: '24px',
      border: '1px solid #29292e',
      backgroundColor: '#202024',
      color: '#ffffff',
      fontSize: '0.95rem',
      outline: 'none',
    },
    chatSendBtn: {
      padding: '0 24px',
      borderRadius: '24px',
      border: 'none',
      backgroundColor: '#0070f3',
      color: '#ffffff',
      fontSize: '0.95rem',
      fontWeight: '600',
      cursor: 'pointer',
    },
    errorText: {
      color: '#ff4d4d',
      fontSize: '0.85rem',
      marginTop: '10px',
      textAlign: 'center',
    },
    toggleText: {
      textAlign: 'center',
      marginTop: '20px',
      fontSize: '0.9rem',
      color: '#a0a0ab',
    },
    toggleLink: {
      color: '#0070f3',
      cursor: 'pointer',
      fontWeight: '600',
      marginLeft: '5px',
    },
    loader: {
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      padding: '12px 16px',
      borderRadius: '18px',
      backgroundColor: '#202024',
      width: 'max-content',
    },
    dot: {
      width: '6px',
      height: '6px',
      backgroundColor: '#8e8e93',
      borderRadius: '50%',
      animation: 'bounce 1.4s infinite ease-in-out both',
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>SmartAssist API 🤖</h1>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={styles.statusBadge}>
            <span style={styles.statusDot}></span>
            <span>{serverStatus === 'online' ? 'Server Live' : 'Checking Server...'}</span>
          </div>
          {token && (
            <button style={styles.logoutBtn} onClick={handleLogout}>
              Logout ({username})
            </button>
          )}
        </div>
      </header>

      {view !== 'chat' ? (
        <div style={styles.authContainer}>
          <div style={styles.authCard}>
            <h2 style={{ marginTop: 0, marginBottom: '24px', textAlign: 'center' }}>
              {view === 'login' ? 'Sign In' : 'Create Account'}
            </h2>
            <form onSubmit={handleAuth}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Username</label>
                <input
                  type="text"
                  required
                  style={styles.input}
                  value={authForm.username}
                  onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
                  placeholder="Enter username"
                />
              </div>

              {view === 'register' && (
                <div style={styles.formGroup}>
                  <label style={styles.label}>Email Address</label>
                  <input
                    type="email"
                    style={styles.input}
                    value={authForm.email}
                    onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
                    placeholder="Enter email (optional)"
                  />
                </div>
              )}

              <div style={styles.formGroup}>
                <label style={styles.label}>Password</label>
                <input
                  type="password"
                  required
                  style={styles.input}
                  value={authForm.password}
                  onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                  placeholder="Enter password"
                />
              </div>

              <button type="submit" style={styles.button}>
                {view === 'login' ? 'Login' : 'Sign Up'}
              </button>

              {authError && <div style={styles.errorText}>{authError}</div>}
            </form>

            <p style={styles.toggleText}>
              {view === 'login' ? "Don't have an account?" : "Already have an account?"}
              <span
                style={styles.toggleLink}
                onClick={() => {
                  setView(view === 'login' ? 'register' : 'login');
                  setAuthError('');
                }}
              >
                {view === 'login' ? 'Register Now' : 'Login here'}
              </span>
            </p>
          </div>
        </div>
      ) : (
        <>
          <main style={styles.chatArea}>
            {messages.map((msg, index) => (
              <div key={index} style={styles.messageRow(msg.sender)}>
                <div style={styles.messageBubble(msg.sender)}>
                  <p style={styles.messageText}>{msg.text}</p>
                  <span style={msg.sender === 'user' ? styles.messageTime : styles.botTime}>
                    {msg.time}
                  </span>
                </div>
              </div>
            ))}
            
            {loading && (
              <div style={styles.messageRow('bot')}>
                <div style={styles.loader}>
                  <span style={{...styles.dot, animationDelay: '-0.32s'}}></span>
                  <span style={{...styles.dot, animationDelay: '-0.16s'}}></span>
                  <span style={styles.dot}></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </main>

          <form onSubmit={handleSend} style={styles.inputForm}>
            <input
              style={styles.chatInput}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question for SmartAssist..."
              disabled={loading}
            />
            <button 
              type="submit" 
              style={{ ...styles.chatSendBtn, opacity: loading || !input.trim() ? 0.6 : 1 }}
              disabled={loading || !input.trim()}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </form>
        </>
      )}
      
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1.0); }
        }
      `}</style>
    </div>
  );
}