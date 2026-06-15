"""Frontend - React Component for Quotation Generator"""
import React, { useState } from 'react';
import axios from 'axios';

const QuotationGenerator = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    customer_id: '',
    project_type: '',
    area: '',
    finish: '',
    budget: '',
    description: '',
  });
  const [quotation, setQuotation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleGenerateAIQuotation = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/api/ai/quotation/generate', {
        customer_id: parseInt(formData.customer_id),
        requirements: {
          project_type: formData.project_type,
          area: parseFloat(formData.area),
          finish: formData.finish,
          budget: parseFloat(formData.budget),
          description: formData.description,
        },
      });
      setQuotation(response.data);
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.error || 'Error generating quotation');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await axios.get(
        `/api/export/quotation/${quotation.quotation_id}/pdf`,
        { responseType: 'blob' }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `quotation_${quotation.quotation_id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError('Error exporting to PDF');
    }
  };

  return (
    <div className="quotation-generator">
      <h1>AI Quotation Generator</h1>
      
      {error && <div className="alert alert-error">{error}</div>}
      
      {step === 1 ? (
        <div className="form-container">
          <h2>Enter Project Details</h2>
          
          <div className="form-group">
            <label>Customer ID:</label>
            <input
              type="number"
              name="customer_id"
              value={formData.customer_id}
              onChange={handleInputChange}
              placeholder="Enter customer ID"
            />
          </div>
          
          <div className="form-group">
            <label>Project Type:</label>
            <input
              type="text"
              name="project_type"
              value={formData.project_type}
              onChange={handleInputChange}
              placeholder="e.g., Kitchen Countertop"
            />
          </div>
          
          <div className="form-group">
            <label>Area (sq ft):</label>
            <input
              type="number"
              step="0.01"
              name="area"
              value={formData.area}
              onChange={handleInputChange}
              placeholder="e.g., 100"
            />
          </div>
          
          <div className="form-group">
            <label>Finish:</label>
            <select
              name="finish"
              value={formData.finish}
              onChange={handleInputChange}
            >
              <option value="">Select finish</option>
              <option value="polished">Polished</option>
              <option value="honed">Honed</option>
              <option value="brushed">Brushed</option>
              <option value="matte">Matte</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Budget ($):</label>
            <input
              type="number"
              step="0.01"
              name="budget"
              value={formData.budget}
              onChange={handleInputChange}
              placeholder="e.g., 5000"
            />
          </div>
          
          <div className="form-group">
            <label>Description:</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Describe the project requirements..."
              rows="4"
            />
          </div>
          
          <button
            onClick={handleGenerateAIQuotation}
            disabled={loading}
            className="btn btn-primary"
          >
            {loading ? 'Generating...' : 'Generate with AI'}
          </button>
        </div>
      ) : (
        <div className="quotation-result">
          <h2>Quotation Generated Successfully</h2>
          
          <div className="quotation-info">
            <p><strong>Quotation ID:</strong> {quotation.quotation_id}</p>
            <p><strong>Message:</strong> {quotation.message}</p>
          </div>
          
          <div className="action-buttons">
            <button onClick={handleExportPDF} className="btn btn-success">
              📄 Export as PDF
            </button>
            <button
              onClick={() => { setStep(1); setQuotation(null); }}
              className="btn btn-secondary"
            >
              Create New Quotation
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuotationGenerator;
