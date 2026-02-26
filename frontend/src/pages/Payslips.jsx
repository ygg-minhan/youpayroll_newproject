import React, { useState, useEffect } from 'react';
import { ChevronDown, FileText, Download, Eye, Filter, Loader2, ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Payslips = () => {
    const navigate = useNavigate();
    const [selectedYearRange, setSelectedYearRange] = useState('2024-2025');
    const [selectedMonth, setSelectedMonth] = useState('Month');
    const [payslips, setPayslips] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const yearRanges = ['2023-2024', '2024-2025', '2025-2026'];
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    useEffect(() => {
        fetchPayslips();
    }, [selectedYearRange, selectedMonth]);

    const fetchPayslips = async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            const startYear = parseInt(selectedYearRange.split('-')[0]);

            let url = `http://127.0.0.1:8002/api/payslips/?year=${startYear}`;
            if (selectedMonth !== 'Month') {
                url += `&month=${selectedMonth}`;
            }

            const response = await fetch(url, {
                headers: { 'Authorization': `Token ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setPayslips(data);
                if (data.length === 0) {
                    // Inject mock data for UI demo purposes if no real data
                    const samplePdf = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf';
                    setPayslips([{
                        id: 1,
                        month: 'March',
                        gross_pay: 2602.0,
                        reimbursement: 1602.0,
                        deductions: 0.0,
                        take_home: 80.0,
                        file: samplePdf,
                        tax_worksheet: samplePdf
                    }]);
                }
            } else {
                throw new Error('Failed to fetch');
            }
        } catch (err) {
            console.log('Using fallback mock data');
            const samplePdf = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf';
            setPayslips([{
                id: 1,
                month: 'March',
                gross_pay: 2602.0,
                reimbursement: 1602.0,
                deductions: 0.0,
                take_home: 80.0,
                file: samplePdf,
                tax_worksheet: samplePdf
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleAction = async (fileUrl, action, fileName) => {
        if (!fileUrl || fileUrl === '#') {
            alert(`${action} not available for this record.`);
            return;
        }

        const token = localStorage.getItem('token');
        const baseUrl = 'http://127.0.0.1:8002';
        const fullUrl = fileUrl.startsWith('http') ? fileUrl : `${baseUrl}${fileUrl}`;

        if (action === 'View') {
            window.open(fullUrl, '_blank');
        } else if (action === 'Download') {
            try {
                const response = await fetch(fullUrl, {
                    headers: { 'Authorization': `Token ${token}` }
                });
                if (!response.ok) throw new Error('File download failed');

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', fileName || 'document.pdf');
                document.body.appendChild(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);
            } catch (err) {
                console.error('Download error:', err);
                // Fallback to direct link if fetch fails
                window.open(fullUrl, '_blank');
            }
        }
    };

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 1,
            maximumFractionDigits: 2,
        }).format(value);
    };

    return (
        <div className="payslips-page-v2">
            <header className="page-header">
                <button className="back-nav-btn" onClick={() => navigate('/')}>
                    <div className="back-icon-box">
                        <ChevronLeft size={20} />
                    </div>
                    <span>Back</span>
                </button>
            </header>

            <div className="payslips-card pop-in">
                {/* Filters Section */}
                <div className="filters-row">
                    <div className="filter-dropdown">
                        <Filter size={18} className="filter-icon" />
                        <span className="filter-label">Financial Year</span>
                        <select
                            className="filter-select"
                            value={selectedYearRange}
                            onChange={(e) => setSelectedYearRange(e.target.value)}
                        >
                            {yearRanges.map(range => (
                                <option key={range} value={range}>{range}</option>
                            ))}
                        </select>
                        <ChevronDown size={18} className="chevron-icon" />
                    </div>

                    <div className="filter-dropdown">
                        <Filter size={18} className="filter-icon" />
                        <span className="filter-label">Filter By</span>
                        <select
                            className="filter-select"
                            value={selectedMonth}
                            onChange={(e) => setSelectedMonth(e.target.value)}
                        >
                            <option value="Month">Month</option>
                            {months.map(m => (
                                <option key={m} value={m}>{m}</option>
                            ))}
                        </select>
                        <ChevronDown size={18} className="chevron-icon" />
                    </div>
                </div>

                {/* Desktop Table Section */}
                <div className="table-responsive desktop-only-table">
                    <table className="payslips-table">
                        <thead>
                            <tr>
                                <th>Month</th>
                                <th>Gross pay</th>
                                <th>Reimbursement</th>
                                <th>Deductions</th>
                                <th>Take Home</th>
                                <th>Payslip</th>
                                <th>Tax worksheet</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr>
                                    <td colSpan="7" className="table-status">
                                        <Loader2 className="spinning-icon" size={24} />
                                        <span>Loading payslips...</span>
                                    </td>
                                </tr>
                            ) : payslips.length > 0 ? (
                                payslips.map((slip) => (
                                    <tr key={slip.id}>
                                        <td className="month-cell">{slip.month}</td>
                                        <td className="amount-cell">{formatCurrency(slip.gross_pay)}</td>
                                        <td className="amount-cell">{formatCurrency(slip.reimbursement)}</td>
                                        <td className="amount-cell">{formatCurrency(slip.deductions)}</td>
                                        <td className="amount-cell">{formatCurrency(slip.take_home)}</td>
                                        <td>
                                            <div className="action-buttons-group">
                                                <button
                                                    className="btn-table-action"
                                                    title="View"
                                                    onClick={() => navigate(`/payslips/${slip.month}`)}
                                                >
                                                    <Eye size={16} />
                                                </button>
                                                <button className="btn-table-action" title="Download" onClick={() => handleAction(slip.file, 'Download', `Payslip_${slip.month}.pdf`)}>
                                                    <Download size={16} />
                                                </button>
                                            </div>
                                        </td>
                                        <td>
                                            <div className="action-buttons-group">
                                                <button className="btn-table-action" title="View" onClick={() => handleAction(slip.tax_worksheet, 'View')}>
                                                    <Eye size={16} />
                                                </button>
                                                <button className="btn-table-action" title="Download" onClick={() => handleAction(slip.tax_worksheet, 'Download', `TaxWorksheet_${slip.month}.pdf`)}>
                                                    <Download size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="7" className="table-status">No payslips found for the selected period.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Mobile Card View */}
                <div className="mobile-cards-view">
                    {loading ? (
                        <div className="loading-state">
                            <Loader2 className="spinning-icon" size={32} />
                            <p>Loading payslips...</p>
                        </div>
                    ) : payslips.length > 0 ? (
                        <div className="payslips-list-mobile">
                            {/* Summary Card for Mobile */}
                            <div className="payroll-summary-grid">
                                <div className="summary-item">
                                    <span>Gross Pay</span>
                                    <strong>{formatCurrency(payslips[0]?.gross_pay || 0)}</strong>
                                </div>
                                <div className="summary-item">
                                    <span>Reimbursement</span>
                                    <strong>{formatCurrency(payslips[0]?.reimbursement || 0)}</strong>
                                </div>
                                <div className="summary-item">
                                    <span>Deductions</span>
                                    <strong className="deduction-val">{formatCurrency(payslips[0]?.deductions || 0)}</strong>
                                </div>
                                <div className="summary-item highlight">
                                    <span>Take Home</span>
                                    <strong>{formatCurrency(payslips[0]?.take_home || 0)}</strong>
                                </div>
                            </div>

                            <h3 className="list-title">Detailed Payslips</h3>
                            {payslips.map(slip => (
                                <div key={slip.id} className="payslip-mobile-card">
                                    <div className="card-main">
                                        <div className="month-indicator">
                                            <FileText size={24} color="#B800C4" />
                                            <div>
                                                <h4>{slip.month} Payslip</h4>
                                                <span>Financial Year {selectedYearRange}</span>
                                            </div>
                                        </div>
                                        <div className="card-actions-v2">
                                            <button className="btn-mobile-v2" onClick={() => navigate(`/payslips/${slip.month}`)}>View</button>
                                            <button className="btn-mobile-v2" onClick={() => handleAction(slip.file, 'Download', `Payslip_${slip.month}.pdf`)}>Download</button>
                                        </div>
                                    </div>
                                    <div className="card-footer-v2">
                                        <div className="footer-item">
                                            <span className="lbl">Tax Worksheet</span>
                                            <div className="f-actions">
                                                <button onClick={() => handleAction(slip.tax_worksheet, 'View')}><Eye size={16} /></button>
                                                <button onClick={() => handleAction(slip.tax_worksheet, 'Download', `TaxWorksheet_${slip.month}.pdf`)}><Download size={16} /></button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="empty-state">No payslips found for the selected period.</div>
                    )}
                </div>
            </div>

            <style>{`
                .payslips-page-v2 {
                    padding: 1rem 0;
                    padding-bottom: 5rem;
                }

                .page-header {
                    margin-bottom: 2rem;
                }

                .back-nav-btn {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    background: none;
                    border: none;
                    cursor: pointer;
                    color: #1e293b;
                    font-weight: 700;
                    font-size: 0.95rem;
                    transition: all 0.2s;
                    padding: 0;
                }

                .back-icon-box {
                    width: 32px;
                    height: 32px;
                    background: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                }

                .back-nav-btn:hover {
                    transform: translateX(-4px);
                    color: #B800C4;
                }

                .payslips-card {
                    background: var(--card-bg);
                border-radius: 24px;
                padding: 2.5rem;
                box-shadow: 0 4px 30px var(--shadow-color);
                border: 1px solid var(--border-color);
                }

                /* Filters Styling */
                .filters-row {
                    display: flex;
                gap: 1.5rem;
                margin-bottom: 2.5rem;
                }

                .filter-dropdown {
                    display: flex;
                align-items: center;
                gap: 0.75rem;
                background: var(--bg-color);
                border: 1px solid var(--border-color);
                padding: 0.75rem 1.25rem;
                border-radius: 12px;
                position: relative;
                cursor: pointer;
                min-width: 200px;
                }

                .filter-icon {color: var(--text-secondary); }
                .filter-label {color: var(--text-secondary); font-size: 0.95rem; font-weight: 500; }

                .filter-select {
                    appearance: none;
                background: transparent;
                border: none;
                color: var(--text-primary);
                font-weight: 700;
                font-size: 1rem;
                cursor: pointer;
                outline: none;
                flex: 1;
                padding-right: 1.5rem;
                z-index: 2;
                }

                .chevron-icon {
                    position: absolute;
                right: 1.25rem;
                color: var(--text-secondary);
                pointer-events: none;
                }

                /* Table Styling */
                .table-responsive {
                    overflow - x: auto;
                }

                .payslips-table {
                    width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                }

                .payslips-table thead th {
                    background: var(--bg-color);
                color: var(--text-primary);
                font-weight: 700;
                font-size: 1rem;
                padding: 1.25rem 1rem;
                text-align: left;
                border-bottom: 1px solid var(--border-color);
                }

                .payslips-table thead th:first-child {border - top - left - radius: 12px; border-bottom-left-radius: 12px; }
                .payslips-table thead th:last-child {border - top - right - radius: 12px; border-bottom-right-radius: 12px; }

                .payslips-table tbody td {
                    padding: 1.5rem 1rem;
                color: var(--text-secondary);
                font-weight: 600;
                font-size: 0.95rem;
                border-bottom: 1px solid var(--border-color);
                }

                .month-cell {color: var(--text-primary); font-weight: 700; }
                .amount-cell {color: var(--text-primary); font-weight: 700; }

                /* Action Buttons */
                .action-buttons-group {
                    display: flex;
                gap: 0.75rem;
                align-items: center;
                }

                .btn-table-action {
                    width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 1px solid var(--border-color);
                background: var(--card-bg);
                color: #B800C4;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s;
                }

                .btn-table-action:hover {
                    background: #B800C4;
                color: white;
                border-color: #B800C4;
                transform: scale(1.1);
                }

                .table-status {
                    text - align: center;
                padding: 4rem 0 !important;
                color: var(--text-secondary);
                }

                .spinning-icon {
                    animation: spin 1s linear infinite;
                color: #B800C4;
                margin-bottom: 0.5rem;
                }

                @keyframes spin {from {transform: rotate(0deg); } to {transform: rotate(360deg); } }

                .pop-in {animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
                @keyframes popIn {
                    from {opacity: 0; transform: translateY(20px) scale(0.98); }
                to {opacity: 1; transform: translateY(0) scale(1); } 
                }

                @media (max-width: 768px) {
                    .payslips-page-v2 { padding: 1rem; padding-bottom: 5rem; }
                    .payslips-card { padding: 1.25rem; border-radius: 18px; }
                    .filters-row { gap: 0.75rem; margin-bottom: 1.25rem; }
                    .filter-dropdown { min-width: 100%; padding: 0.6rem 1rem; }
                    .desktop-only-table { display: none; }
                    .mobile-cards-view { display: block; }
                }

                .mobile-cards-view { display: none; }
                .payroll-summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.5rem; }
                .summary-item { background: var(--bg-color); padding: 1rem; border-radius: 14px; display: flex; flex-direction: column; gap: 2px; border: 1px solid var(--border-color); }
                .summary-item span { font-size: 0.65rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em; }
                .summary-item strong { font-size: 0.95rem; color: var(--text-primary); font-weight: 800; }
                .deduction-val { color: #ef4444 !important; }
                .summary-item.highlight { background: #fdf4ff; border-color: #fce7f3; }
                .summary-item.highlight strong { color: #B800C4; }

                .list-title { font-size: 1rem; font-weight: 800; color: var(--text-primary); margin-bottom: 1rem; }
                .payslip-mobile-card { background: var(--bg-color); border-radius: 18px; border: 1px solid var(--border-color); overflow: hidden; margin-bottom: 0.85rem; }
                .card-main { padding: 1rem; display: flex; flex-direction: column; gap: 1rem; }
                .month-indicator { display: flex; align-items: center; gap: 0.85rem; }
                .month-indicator h4 { font-size: 0.95rem; font-weight: 800; color: var(--text-primary); margin: 0; }
                .month-indicator span { font-size: 0.7rem; color: var(--text-secondary); font-weight: 600; }
                
                .card-actions-v2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; }
                .btn-mobile-v2 { padding: 0.65rem; border-radius: 10px; font-weight: 700; font-size: 0.85rem; cursor: pointer; border: none; }
                .btn-mobile-v2:first-child { background: #B800C4; color: white; box-shadow: 0 4px 8px rgba(184, 0, 196, 0.15); }
                .btn-mobile-v2:last-child { background: white; color: #B800C4; border: 1px solid #fce7f3; }
                body.dark-mode .btn-mobile-v2:last-child { background: var(--card-bg); border-color: var(--border-color); }

                .card-footer-v2 { padding: 0.75rem 1rem; background: rgba(0,0,0,0.02); border-top: 1px solid var(--border-color); }
                .footer-item { display: flex; justify-content: space-between; align-items: center; }
                .footer-item .lbl { font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); }
                .f-actions { display: flex; gap: 0.5rem; }
                .f-actions button { width: 30px; height: 30px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--card-bg); color: #B800C4; display: flex; align-items: center; justify-content: center; }
            `}</style>
        </div>
    );
};

export default Payslips;
