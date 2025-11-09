import React from 'react';
import IndividualForm from '../components/IndividualForm';
import { useNavigate } from 'react-router-dom';

const AddIndividual = () => {
  const navigate = useNavigate();

  const handleSave = (individual) => {
    // Redirect to view page after successful save
    navigate('/view');
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <IndividualForm
      onSave={handleSave}
      onCancel={handleCancel}
    />
  );
};

export default AddIndividual;