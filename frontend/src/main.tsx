import React, { Component, ErrorInfo, ReactNode } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error in application:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#122311',
          color: '#eaece6',
          fontFamily: 'Inter, sans-serif',
          padding: '2rem',
          textAlign: 'center',
        }}>
          <div style={{
            background: 'rgba(255, 0, 85, 0.08)',
            border: '1px solid rgba(255, 0, 85, 0.4)',
            borderRadius: 16,
            padding: '2.5rem',
            maxWidth: '640px',
            backdropFilter: 'blur(16px)',
          }}>
            <h1 style={{ fontFamily: 'Oswald, sans-serif', fontSize: '2rem', color: '#FF0055', marginBottom: '1rem', letterSpacing: '0.05em' }}>
              APPLICATION ERROR CAUGHT
            </h1>
            <p style={{ color: 'rgba(234,236,230,0.7)', marginBottom: '1.5rem', lineHeight: 1.6, fontSize: '0.9rem' }}>
              {this.state.error?.message || 'An unexpected error occurred during rendering.'}
            </p>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: '0.75rem 2rem',
                borderRadius: '9999px',
                backgroundColor: 'rgba(0, 240, 255, 0.15)',
                border: '1px solid #00F0FF',
                color: '#00F0FF',
                fontFamily: 'JetBrains Mono, monospace',
                cursor: 'pointer',
                fontSize: '0.85rem',
                letterSpacing: '0.05em',
                transition: 'all 0.2s ease',
              }}
            >
              RELOAD PAGE
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
