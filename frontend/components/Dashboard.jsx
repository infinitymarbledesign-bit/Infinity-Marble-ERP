"""Frontend - React Component for Dashboard"""
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_customers: 0,
    total_quotations: 0,
    total_invoices: 0,
    total_materials: 0,
  });
  const [quotations, setQuotations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [customersRes, quotationsRes, invoicesRes, materialsRes] = await Promise.all([
        axios.get('/api/customers'),
        axios.get('/api/quotations'),
        axios.get('/api/invoices'),
        axios.get('/api/materials'),
      ]);

      setStats({
        total_customers: customersRes.data.total,
        total_quotations: quotationsRes.data.total,
        total_invoices: invoicesRes.data.total,
        total_materials: materialsRes.data.total,
      });
      
      setQuotations(quotationsRes.data.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Customers</h3>
          <p className="stat-value">{stats.total_customers}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Quotations</h3>
          <p className="stat-value">{stats.total_quotations}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Materials</h3>
          <p className="stat-value">{stats.total_materials}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Invoices</h3>
          <p className="stat-value">{stats.total_invoices}</p>
        </div>
      </div>
      
      <div className="recent-quotations">
        <h2>Recent Quotations</h2>
        <table>
          <thead>
            <tr>
              <th>Quotation #</th>
              <th>Customer</th>
              <th>Total</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {quotations.map(q => (
              <tr key={q.id}>
                <td>{q.quotation_number}</td>
                <td>{q.customer_name}</td>
                <td>${q.total_amount.toFixed(2)}</td>
                <td><span className={`status ${q.status}`}>{q.status}</span></td>
                <td>{new Date(q.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
