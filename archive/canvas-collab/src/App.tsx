import { useState, useEffect } from 'react';
import { api, Workspace } from './api/client';
import './App.css';

function App() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loading, setLoading] = useState(true);
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [agentMessage, setAgentMessage] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    loadWorkspaces();
  }, []);

  const loadWorkspaces = async () => {
    try {
      const data = await api.listWorkspaces();
      setWorkspaces(data);
    } catch (error) {
      console.error('Failed to load workspaces:', error);
    } finally {
      setLoading(false);
    }
  };

  const createWorkspace = async () => {
    if (!newWorkspaceName.trim()) return;

    try {
      await api.createWorkspace(newWorkspaceName);
      setNewWorkspaceName('');
      await loadWorkspaces();
    } catch (error) {
      console.error('Failed to create workspace:', error);
    }
  };

  const testAgent = async () => {
    if (!agentMessage.trim()) return;

    setIsStreaming(true);
    setAgentResponse('');

    try {
      await api.sendToAgent(
        'test-widget',
        agentMessage,
        (chunk) => setAgentResponse(prev => prev + chunk),
        () => {
          setIsStreaming(false);
          console.log('Agent completed');
        },
        (error) => {
          setIsStreaming(false);
          console.error('Agent error:', error);
          setAgentResponse(prev => prev + `\n\nError: ${error}`);
        }
      );
    } catch (error) {
      setIsStreaming(false);
      console.error('Failed to send to agent:', error);
    }
  };

  return (
    <div className="app">
      <h1>Canvas Collab - Web Version</h1>

      <div className="section">
        <h2>Workspaces</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <div className="workspace-list">
              {workspaces.length === 0 ? (
                <p>No workspaces yet. Create one below!</p>
              ) : (
                workspaces.map(ws => (
                  <div key={ws.id} className="workspace-item">
                    <strong>{ws.name}</strong>
                    <span>{new Date(ws.created_at).toLocaleDateString()}</span>
                  </div>
                ))
              )}
            </div>

            <div className="create-workspace">
              <input
                type="text"
                value={newWorkspaceName}
                onChange={(e) => setNewWorkspaceName(e.target.value)}
                placeholder="New workspace name"
                onKeyPress={(e) => e.key === 'Enter' && createWorkspace()}
              />
              <button onClick={createWorkspace}>Create Workspace</button>
            </div>
          </>
        )}
      </div>

      <div className="section">
        <h2>Test Claude AI</h2>
        <div className="agent-test">
          <textarea
            value={agentMessage}
            onChange={(e) => setAgentMessage(e.target.value)}
            placeholder="Type a message for Claude..."
            rows={3}
          />
          <button onClick={testAgent} disabled={isStreaming || !agentMessage.trim()}>
            {isStreaming ? 'Streaming...' : 'Send to Claude'}
          </button>

          {agentResponse && (
            <div className="agent-response">
              <h3>Claude's Response:</h3>
              <pre>{agentResponse}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
