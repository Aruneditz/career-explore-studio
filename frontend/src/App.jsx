import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppLayout from './components/Layout/AppLayout';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import SplashScreen from './components/Splash/SplashScreen';
import HomePage from './pages/Home/HomePage';
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import GoalsPage from './pages/Goals/GoalsPage';
import SkillsPage from './pages/Skills/SkillsPage';
import SkillOverviewPage from './pages/Skills/SkillOverviewPage';
import CompleteTopicsPage from './pages/Skills/CompleteTopicsPage';
import ImportantTopicsPage from './pages/Skills/ImportantTopicsPage';
import PracticalSectionPage from './pages/Skills/PracticalSectionPage';
import LearnCompletePage from './pages/Skills/LearnCompletePage';
import SelfEvaluationPage from './pages/Skills/SelfEvaluationPage';
import SkillInterviewPrepPage from './pages/Skills/SkillInterviewPrepPage';
import ProgressPage from './pages/Progress/ProgressPage';
import OverallEvaluationPage from './pages/Interview/OverallEvaluationPage';
import InterviewPrepPage from './pages/Interview/InterviewPrepPage';
import ProfilePage from './pages/Profile/ProfilePage';
import ErrorBoundary from './components/Common/ErrorBoundary';
import api from './services/api';

function AppContent() {
  const [showSplash, setShowSplash] = useState(() => {
    return !sessionStorage.getItem('ces_splash_shown');
  });

  const [backendHealth, setBackendHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(true);

  const fetchHealth = async () => {
    setHealthLoading(true);
    try {
      const data = await api.checkHealth();
      setBackendHealth(data);
    } catch (err) {
      console.warn('Backend connection error:', err.message);
      setBackendHealth({ status: 'error', database: 'disconnected' });
    } finally {
      setHealthLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const handleSplashFinish = () => {
    sessionStorage.setItem('ces_splash_shown', 'true');
    setShowSplash(false);
  };

  const backendStatus = backendHealth?.status === 'healthy' 
    ? 'healthy' 
    : healthLoading 
      ? 'loading' 
      : 'error';

  if (showSplash) {
    return <SplashScreen onFinish={handleSplashFinish} />;
  }

  return (
    <AppLayout backendStatus={backendStatus}>
        <Routes>
          {/* Public Home View */}
          <Route 
            path="/" 
            element={
              <HomePage 
                backendHealth={backendHealth} 
                onRefreshHealth={fetchHealth} 
                healthLoading={healthLoading}
              />
            } 
          />

          {/* Authentication Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Application Routes */}
          <Route 
            path="/goals" 
            element={
              <ProtectedRoute>
                <GoalsPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills" 
            element={
              <ProtectedRoute>
                <SkillsPage />
              </ProtectedRoute>
            } 
          />

          {/* Skill Workflow Stage Routes (Separate Routes as required by Section 10) */}
          <Route 
            path="/skills/:skillId/overview" 
            element={
              <ProtectedRoute>
                <SkillOverviewPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/topics" 
            element={
              <ProtectedRoute>
                <CompleteTopicsPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/important-topics" 
            element={
              <ProtectedRoute>
                <ImportantTopicsPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/practical" 
            element={
              <ProtectedRoute>
                <PracticalSectionPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/learn" 
            element={
              <ProtectedRoute>
                <LearnCompletePage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/evaluation" 
            element={
              <ProtectedRoute>
                <SelfEvaluationPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/skills/:skillId/interview-prep" 
            element={
              <ProtectedRoute>
                <SkillInterviewPrepPage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/progress" 
            element={
              <ProtectedRoute>
                <ProgressPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/overall-evaluation" 
            element={
              <ProtectedRoute>
                <OverallEvaluationPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/interview-prep" 
            element={
              <ProtectedRoute>
                <InterviewPrepPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } 
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
