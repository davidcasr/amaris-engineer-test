import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Context Providers
import { UserProvider } from './context/UserContext';
import { NotificationProvider } from './context/NotificationContext';

// Components
import Layout from './components/layout/Layout';
import ErrorBoundary from './components/common/ErrorBoundary';
import NotificationToast from './components/common/NotificationToast';

// Pages
import Funds from './pages/Funds';
import MyFunds from './pages/MyFunds';
import Transactions from './pages/Transactions';
import Settings from './pages/Settings';

// Styles
import './styles/globals.css';

function App() {
  return (
    <ErrorBoundary>
      <NotificationProvider>
        <UserProvider>
          <Router>
            <Layout>
              <Routes>
                {/* Redirect root to funds */}
                <Route path="/" element={<Navigate to="/funds" replace />} />
                
                {/* Main pages */}
                <Route path="/funds" element={<Funds />} />
                <Route path="/my-funds" element={<MyFunds />} />
                <Route path="/transactions" element={<Transactions />} />
                <Route path="/settings" element={<Settings />} />
                
                {/* Catch all - redirect to funds */}
                <Route path="*" element={<Navigate to="/funds" replace />} />
              </Routes>
              
              {/* Global notification system */}
              <NotificationToast />
            </Layout>
          </Router>
        </UserProvider>
      </NotificationProvider>
    </ErrorBoundary>
  );
}

export default App;