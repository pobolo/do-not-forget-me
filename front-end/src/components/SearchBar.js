import React from 'react';
import './SearchBar.css';

const SearchBar = ({ value, onChange, placeholder = "Search..." }) => {
  return (
    <div className="search-bar">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="search-input"
      />
      <div className="search-icon">
        🔍
      </div>
    </div>
  );
};

export default SearchBar;