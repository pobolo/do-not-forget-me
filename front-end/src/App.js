import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import AddIndividual from './pages/AddIndividual';
import ViewIndividuals from './pages/ViewIndividuals';
import WealthRankingPage from './pages/WealthRankingPage';
import Analytics from './pages/Analytics';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add" element={<AddIndividual />} />
            <Route path="/view" element={<ViewIndividuals />} />
            <Route path="/ranking" element={<WealthRankingPage />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;