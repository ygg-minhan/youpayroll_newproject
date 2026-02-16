import React, { useState, useEffect } from 'react';
import { ArrowLeft, ChevronDown, FileText, FileBarChart, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Payslips = () => {
    const navigate = useNavigate();
    const [selectedYearRange, setSelectedYearRange] = useState('2026-2027');
    const [selectedMonth, setSelectedMonth] = useState('October');
    const [payslipData, setPayslipData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Generate years from 2020 to 2030
    const yearRanges = Array.from({ length: 11 }, (_, i) => {
        const start = 2020 + i;
        return `${start}-${start + 1}`;
    });
    const months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March'];

    useEffect(() => {
        fetchPayslip();
    }, [selectedYearRange, selectedMonth]);

    const fetchPayslip = async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            const startYear = parseInt(selectedYearRange.split('-')[0]);
            const monthIndex = months.indexOf(selectedMonth);

            // Financial year logic: April to Dec is startYear, Jan to March is startYear + 1
            const targetYear = monthIndex < 9 ? startYear : startYear + 1;

            const response = await fetch(`http://127.0.0.1:8000/api/payslips/?month=${selectedMonth}&year=${targetYear}`, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.length > 0) {
                    setPayslipData(data[0]);
                } else {
                    setPayslipData(null);
                }
            } else {
                setError('Failed to fetch data');
            }
        } catch (err) {
            setError('Connection error');
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-IN').format(value);
    };

    return (
        <div className="payslips-page">
            {/* Header Section */}
            <header className="page-header">
                <div className="header-left">
                    <button onClick={() => navigate(-1)} className="back-btn">
                        <ArrowLeft size={24} />
                    </button>
                    <h1>Payslips</h1>
                </div>

                {/* Year Filter */}
                <div className="year-filter">
                    <span>Financial Year</span>
                    <div className="dropdown-container">
                        <select
                            className="year-dropdown"
                            value={selectedYearRange}
                            onChange={(e) => setSelectedYearRange(e.target.value)}
                        >
                            {yearRanges.map(range => (
                                <option key={range} value={range}>{range}</option>
                            ))}
                        </select>
                        <ChevronDown className="dropdown-icon" size={16} />
                    </div>
                </div>
            </header>

            {/* Month Filter */}
            <div className="month-filter-container">
                <div className="month-filter">
                    {months.map((month) => (
                        <button
                            key={month}
                            className={`month-btn ${selectedMonth === month ? 'active' : ''}`}
                            onClick={() => setSelectedMonth(month)}
                        >
                            {month}
                        </button>
                    ))}
                </div>
            </div>

            {/* Content Area */}
            {loading ? (
                <div className="loading-state">
                    <Loader2 className="animate-spin" size={48} />
                    <p>Fetching your payroll details...</p>
                </div>
            ) : error ? (
                <div className="error-state">
                    <p>{error}</p>
                    <button onClick={fetchPayslip} className="retry-btn">Retry</button>
                </div>
            ) : payslipData ? (
                <div className="payroll-summary-card">
                    <div className="summary-grid">
                        <div className="summary-item">
                            <span className="label">Gross Pay</span>
                            <span className="value">{formatCurrency(payslipData.gross_pay)}</span>
                        </div>
                        <div className="summary-item">
                            <span className="label">Reimbursement</span>
                            <span className="value">{formatCurrency(payslipData.reimbursement)}</span>
                        </div>
                        <div className="summary-item">
                            <span className="label text-red">Deductions</span>
                            <span className="value text-red">{formatCurrency(payslipData.deductions)}</span>
                        </div>
                        <div className="summary-item highlight">
                            <span className="label text-green">Take home</span>
                            <span className="value text-green">{formatCurrency(payslipData.take_home)}</span>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="action-buttons">
                        <button
                            className="action-btn primary-action"
                            onClick={() => {
                                if (payslipData.file) {
                                    const url = payslipData.file.startsWith('http')
                                        ? payslipData.file
                                        : `http://127.0.0.1:8000${payslipData.file}`;
                                    window.open(url, '_blank');
                                }
                            }}
                            disabled={!payslipData.file}
                        >
                            <FileText size={20} />
                            Payslip
                        </button>
                        <button
                            className="action-btn secondary-action"
                            onClick={() => {
                                if (payslipData.tax_worksheet) {
                                    const url = payslipData.tax_worksheet.startsWith('http')
                                        ? payslipData.tax_worksheet
                                        : `http://127.0.0.1:8000${payslipData.tax_worksheet}`;
                                    window.open(url, '_blank');
                                }
                            }}
                            disabled={!payslipData.tax_worksheet}
                        >
                            <FileBarChart size={20} />
                            Tax Worksheet
                        </button>
                    </div>
                </div>
            ) : (
                <div className="empty-state">
                    <FileText size={64} opacity={0.2} />
                    <h3>No Data Available</h3>
                    <p>We couldn't find any payslip records for {selectedMonth} {selectedYearRange}.</p>
                    <p className="hint">If you think this is a mistake, please contact HR.</p>
                </div>
            )}

            <style>{`
        .payslips-page {
           padding: 2rem;
           max-width: 1000px;
           margin: 0 auto;
        }

        .page-header {
           display: flex;
           justify-content: space-between;
           align-items: center;
           margin-bottom: 2.5rem;
        }

        .header-left {
           display: flex;
           align-items: center;
           gap: 1.5rem;
        }

        .back-btn {
           background: #fff;
           border: 1px solid var(--border-color);
           cursor: pointer;
           padding: 0.6rem;
           border-radius: 12px;
           transition: all 0.2s;
           display: flex;
           align-items: center;
           justify-content: center;
           box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .back-btn:hover { 
            background: #f8fafc;
            transform: translateX(-2px);
        }

        h1 {
           font-size: 2rem;
           font-weight: 800;
           color: #1e293b;
           margin: 0;
        }

        .year-filter {
           display: flex;
           align-items: center;
           gap: 1rem;
           font-size: 0.95rem;
           color: #64748b;
        }

        .dropdown-container {
            position: relative;
            display: flex;
            align-items: center;
        }

        .year-dropdown {
           appearance: none;
           background: #fff;
           border: 1px solid var(--border-color);
           padding: 0.6rem 2.5rem 0.6rem 1.2rem;
           border-radius: 12px;
           font-weight: 600;
           color: #1e293b;
           cursor: pointer;
           font-size: 0.95rem;
           outline: none;
           transition: border-color 0.2s;
        }

        .year-dropdown:hover {
            border-color: var(--primary-color);
        }

        .dropdown-icon {
            position: absolute;
            right: 1rem;
            pointer-events: none;
            color: #64748b;
        }

        .month-filter-container {
            overflow-x: auto;
            margin-bottom: 2.5rem;
            padding-bottom: 0.5rem;
            scrollbar-width: thin;
        }

        .month-filter {
           display: flex;
           gap: 2rem;
           border-bottom: 1px solid #e2e8f0;
           min-width: max-content;
        }

        .month-btn {
           background: none;
           border: none;
           font-size: 1rem;
           font-weight: 500;
           color: #64748b;
           padding-bottom: 1rem;
           cursor: pointer;
           position: relative;
           white-space: nowrap;
           transition: all 0.2s;
        }
        
        .month-btn:hover {
            color: #1e293b;
        }

        .month-btn.active {
           color: var(--primary-color);
           font-weight: 700;
        }
        .month-btn.active::after {
           content: '';
           position: absolute;
           bottom: -1px;
           left: 0;
           width: 100%;
           height: 3px;
           background: var(--primary-color);
           border-radius: 3px 3px 0 0;
        }

        .payroll-summary-card {
           background: #fff;
           border-radius: 24px;
           padding: 3rem;
           box-shadow: 0 10px 25px rgba(0,0,0,0.05);
           border: 1px solid #f1f5f9;
        }

        .summary-grid {
           display: grid;
           grid-template-columns: repeat(2, 1fr);
           gap: 3rem;
           margin-bottom: 3.5rem;
        }

        .summary-item {
           display: flex;
           flex-direction: column;
           gap: 0.8rem;
        }

        .label {
           font-size: 1rem;
           color: #64748b;
           font-weight: 500;
        }
        
        .value {
           font-size: 2.25rem;
           font-weight: 800;
           color: #1e293b;
           letter-spacing: -0.02em;
        }

        .text-red { color: #ef4444; }
        .text-green { color: #10b981; }

        .action-buttons {
           display: flex;
           gap: 2rem;
        }

        .action-btn {
           flex: 1;
           display: flex;
           align-items: center;
           justify-content: center;
           gap: 0.75rem;
           padding: 1.25rem;
           border-radius: 16px;
           font-weight: 700;
           font-size: 1rem;
           transition: all 0.2s;
           cursor: pointer;
        }

        .action-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            filter: grayscale(1);
        }
        
        .primary-action {
           background: #B800C4;
           color: white;
           border: none;
           box-shadow: 0 4px 12px rgba(184, 0, 196, 0.2);
        }
        .primary-action:not(:disabled):hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(184, 0, 196, 0.3);
        }

        .secondary-action {
           background: #fff;
           color: #1e293b;
           border: 1px solid #e2e8f0;
        }
        .secondary-action:not(:disabled):hover { 
            background: #f8fafc;
            transform: translateY(-2px);
            border-color: #cbd5e1;
        }

        .loading-state, .error-state, .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 5rem 2rem;
            text-align: center;
            background: #fff;
            border-radius: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        }

        .loading-state p { margin-top: 1rem; color: #64748b; }
        .animate-spin { animation: spin 1s linear infinite; color: #B800C4; }

        .empty-state h3 { margin: 1.5rem 0 0.5rem; color: #1e293b; }
        .empty-state p { color: #64748b; margin: 0; }
        .hint { font-size: 0.85rem; margin-top: 1rem !important; }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .summary-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .action-buttons {
                flex-direction: column;
                gap: 1rem;
            }
            .value { font-size: 1.75rem; }
            .page-header { flex-direction: column; align-items: flex-start; gap: 1.5rem; }
            .year-filter { align-self: flex-end; }
        }
      `}</style>
        </div>
    );
};

export default Payslips;
