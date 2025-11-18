/**
 * Main App component with routing
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Dashboard } from './views/Dashboard';
import { TaskDetail } from './views/TaskDetail';
import Canvas from './views/Canvas';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Canvas />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/tasks/:taskId" element={<TaskDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
