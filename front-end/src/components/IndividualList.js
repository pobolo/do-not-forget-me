import React, { useState, useEffect } from 'react';
import IndividualCard from './IndividualCard';
import IndividualForm from './IndividualForm';
import SearchBar from './SearchBar';
import { wealthAPI } from '../services/api';
import './IndividualList.css';

const IndividualList = () => {
  const [individuals, setIndividuals] = useState([]);
  const [filteredIndividuals, setFilteredIndividuals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingIndividual, setEditingIndividual] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadIndividuals();
  }, []);

  useEffect(() => {
    filterIndividuals();
  }, [individuals, searchQuery]);

  const loadIndividuals = async () => {
    try {
      setLoading(true);
      const response = await wealthAPI.getAllIndividuals();
      if (response.data.success) {
        setIndividuals(response.data.individuals);
      }
    } catch (err) {
      setError('Failed to load individuals');
      console.error('Error loading individuals:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterIndividuals = () => {
    if (!searchQuery.trim()) {
      setFilteredIndividuals(individuals);
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = individuals.filter(individual =>
      individual.first_name.toLowerCase().includes(query) ||
      individual.last_name.toLowerCase().includes(query) ||
      individual.company.toLowerCase().includes(query) ||
      individual.industry.toLowerCase().includes(query)
    );
    setFilteredIndividuals(filtered);
  };

  const handleAddIndividual = () => {
    setEditingIndividual(null);
    setShowForm(true);
  };

  const handleEditIndividual = (individual) => {
    setEditingIndividual(individual);
    setShowForm(true);
  };

  const handleDeleteIndividual = async (id) => {
    if (window.confirm('Are you sure you want to delete this individual?')) {
      try {
        const response = await wealthAPI.deleteIndividual(id);
        if (response.data.success) {
          setIndividuals(prev => prev.filter(ind => ind.id !== id));
        }
      } catch (err) {
        setError('Failed to delete individual');
        console.error('Error deleting individual:', err);
      }
    }
  };

  const handleSaveIndividual = (savedIndividual) => {
    if (editingIndividual) {
      // Update existing individual
      setIndividuals(prev =>
        prev.map(ind =>
          ind.id === savedIndividual.id ? savedIndividual : ind
        )
      );
    } else {
      // Add new individual
      setIndividuals(prev => [...prev, savedIndividual]);
    }
    setShowForm(false);
    setEditingIndividual(null);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingIndividual(null);
  };

  if (loading) {
    return <div className="loading">Loading individuals...</div>;
  }

  if (showForm) {
    return (
      <IndividualForm
        individual={editingIndividual}
        onSave={handleSaveIndividual}
        onCancel={handleCancelForm}
        isEdit={!!editingIndividual}
      />
    );
  }

  return (
    <div className="individual-list-container">
      <div className="list-header">
        <h1>Wealthy Individuals</h1>
        <button
          onClick={handleAddIndividual}
          className="btn btn-primary add-btn"
        >
          Add New Individual
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <SearchBar
        value={searchQuery}
        onChange={setSearchQuery}
        placeholder="Search by name, company, or industry..."
      />

      <div className="list-stats">
        <span>Showing {filteredIndividuals.length} of {individuals.length} individuals</span>
      </div>

      <div className="individuals-grid">
        {filteredIndividuals.map(individual => (
          <IndividualCard
            key={individual.id}
            individual={individual}
            onEdit={handleEditIndividual}
            onDelete={handleDeleteIndividual}
          />
        ))}
      </div>

      {filteredIndividuals.length === 0 && !loading && (
        <div className="empty-state">
          <h3>No individuals found</h3>
          <p>
            {searchQuery
              ? 'Try adjusting your search terms'
              : 'Get started by adding your first individual'
            }
          </p>
        </div>
      )}
    </div>
  );
};

export default IndividualList;