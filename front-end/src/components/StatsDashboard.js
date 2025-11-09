import React, { useState, useEffect } from 'react';
import { wealthAPI } from '../services/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import './StatsDashboard.css';

const StatsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [redisInfo, setRedisInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const response = await wealthAPI.getStats();
      if (response.data.success) {
        setStats(response.data.wealth_statistics);
        setRedisInfo(response.data.redis_info);
      }
    } catch (err) {
      setError('Failed to load statistics');
      console.error('Error loading stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) {
    return <div className="loading">Loading statistics...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!stats) {
    return <div className="error-message">No statistics available</div>;
  }

  const industryData = Object.entries(stats.industry_distribution || {}).map(([name, value]) => ({
    name,
    value
  }));

  const wealthTierData = Object.entries(stats.wealth_tier_distribution || {}).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="stats-dashboard">
      <h1>Analytics Dashboard</h1>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Individuals</h3>
          <div className="metric-value">{stats.total_individuals}</div>
        </div>
        <div className="metric-card">
          <h3>Total Wealth</h3>
          <div className="metric-value">{formatCurrency(stats.total_wealth)}</div>
        </div>
        <div className="metric-card">
          <h3>Average Wealth</h3>
          <div className="metric-value">{formatCurrency(stats.average_wealth)}</div>
        </div>
        <div className="metric-card">
          <h3>Max Wealth</h3>
          <div className="metric-value">{formatCurrency(stats.max_wealth)}</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-card">
          <h3>Industry Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={industryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Wealth Tier Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={wealthTierData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {wealthTierData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Redis Info */}
      {redisInfo && (
        <div className="redis-info">
          <h3>Redis Information</h3>
          <div className="redis-stats">
            <div className="redis-stat">
              <span className="label">Connected Clients:</span>
              <span className="value">{redisInfo.connected_clients}</span>
            </div>
            <div className="redis-stat">
              <span className="label">Used Memory:</span>
              <span className="value">{redisInfo.used_memory_human}</span>
            </div>
            <div className="redis-stat">
              <span className="label">Peak Memory:</span>
              <span className="value">{redisInfo.used_memory_peak_human}</span>
            </div>
            <div className="redis-stat">
              <span className="label">Cache Hit Rate:</span>
              <span className="value">
                {redisInfo.keyspace_hits} / {redisInfo.keyspace_hits + redisInfo.keyspace_misses}
              </span>
            </div>
            <div className="redis-stat">
              <span className="label">Total Commands:</span>
              <span className="value">{redisInfo.total_commands_processed}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatsDashboard;