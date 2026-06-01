import { useState, useEffect, useRef } from 'react'; 
import axios from 'axios';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      text: "Hello! I am SmartAssist AI. How can I help you today?",
      sender: 'bot',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [serverStatus, setServerStatus] = useState('checking'); // checking, online, offline
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Check backend connection
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/chat/')
      .then(() => setServerStatus('online'))
      .catch((err) => {
        if (err.response) {
          setServerStatus('online'); // Server running, status 405/400 context matches live state
        } else {
          setServerStatus('offline');
        }
      });
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { text: input, sender: 'user', time: currentTime };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/chat/', { message: input });
      
      const botMsg = { 
        text: res.data.reply, 
        sender: 'bot', 
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = { 
        text: "Sorry, I am facing trouble reaching the server. Please check your Django backend state.", 
        sender: 'bot', 
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
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
      gap: '6px',
      fontSize: '0.85rem',
      padding: '4px 10px',
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
    input: {
      flex: 1,
      padding: '14px 20px',
      borderRadius: '24px',
      border: '1px solid #29292e',
      backgroundColor: '#202024',
      color: '#ffffff',
      fontSize: '0.95rem',
      outline: 'none',
    },
    button: {
      padding: '0 24px',
      borderRadius: '24px',
      border: 'none',
      backgroundColor: '#0070f3',
      color: '#ffffff',
      fontSize: '0.95rem',
      fontWeight: '600',
      cursor: 'pointer',
    },
    loader: {
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      padding: '12px 16px',
      borderRadius: '18px',
      backgroundColor: '#202024',
    },
    dot: {
      width: '6px',
      height: '6px',
      backgroundColor: '#8e8e93',
      borderRadius: '50%',
      animation: 'bounce 1.4s infinite ease-in-out both'
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>SmartAssist API 🤖</h1>
        <div style={styles.statusBadge}>
          <span style={styles.statusDot}></span>
          <span>
            {serverStatus === 'online' ? 'Connected' : serverStatus === 'offline' ? 'Offline' : 'Checking...'}
          </span>
        </div>
      </header>

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
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question for SmartAssist..."
          disabled={loading}
        />
        <button 
          type="submit" 
          style={{ ...styles.button, opacity: loading || !input.trim() ? 0.6 : 1 }}
          disabled={loading || !input.trim()}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1.0); }
        }
      `}</style>
    </div>
  );
}

export default App;