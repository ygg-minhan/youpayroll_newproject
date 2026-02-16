import React, { useState, useEffect } from 'react';
import { Search, Plus, Book, ChevronRight, Clock, User, Tag, Edit3, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const Wiki = () => {
  const [pages, setPages] = useState([]);
  const [categories, setCategories] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPage, setSelectedPage] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({ title: '', content: '', category: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = {};
      if (token) {
        headers['Authorization'] = `Token ${token}`;
      }

      const [pagesRes, catsRes] = await Promise.all([
        fetch('http://127.0.0.1:8000/api/wiki-pages/', { headers }),
        fetch('http://127.0.0.1:8000/api/wiki-categories/', { headers })
      ]);

      if (!pagesRes.ok || !catsRes.ok) {
        throw new Error('Failed to fetch wiki data');
      }

      const pagesData = await pagesRes.json();
      const catsData = await catsRes.json();

      setPages(Array.isArray(pagesData) ? pagesData : []);
      setCategories(Array.isArray(catsData) ? catsData : []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching wiki data:', error);
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const token = localStorage.getItem('token');
      const url = selectedPage
        ? `http://127.0.0.1:8000/api/wiki-pages/${selectedPage.slug}/`
        : 'http://127.0.0.1:8000/api/wiki-pages/';
      const method = selectedPage ? 'PATCH' : 'POST';

      const headers = {
        'Content-Type': 'application/json'
      };
      if (token) {
        headers['Authorization'] = `Token ${token}`;
      }

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(editData)
      });

      if (response.ok) {
        const savedPage = await response.json();
        await fetchData();
        setSelectedPage(savedPage);
        setIsEditing(false);
      }
    } catch (error) {
      console.error('Error saving page:', error);
    }
  };

  const filteredPages = pages.filter(page =>
    page.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    page.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) return <div className="loading">Loading Wiki...</div>;

  return (
    <div className="wiki-container">
      {/* Sidebar: Categories & Page List */}
      <div className="wiki-sidebar">
        <div className="search-bar">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search wiki..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <button className="create-btn" onClick={() => {
          setSelectedPage(null);
          setEditData({ title: '', content: '', category: categories[0]?.id || '' });
          setIsEditing(true);
        }}>
          <Plus size={18} />
          Create New Page
        </button>

        <div className="category-section">
          <h3>Categories</h3>
          <div className="category-list">
            {categories.map(cat => (
              <div key={cat.id} className="category-item">
                <Tag size={16} />
                <span>{cat.name}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="pages-section">
          <h3>Pages</h3>
          <div className="page-list">
            {filteredPages.map(page => (
              <div
                key={page.id}
                className={`page-item ${selectedPage?.id === page.id ? 'active' : ''}`}
                onClick={() => {
                  setSelectedPage(page);
                  setIsEditing(false);
                }}
              >
                <Book size={16} />
                <span>{page.title}</span>
                <ChevronRight size={14} className="arrow" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="wiki-content">
        {isEditing ? (
          <div className="edit-view">
            <input
              className="title-input"
              value={editData.title}
              onChange={(e) => setEditData({ ...editData, title: e.target.value })}
              placeholder="Page Title"
            />
            <select
              className="category-select"
              value={editData.category}
              onChange={(e) => setEditData({ ...editData, category: e.target.value })}
            >
              <option value="">Select Category</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
            <textarea
              className="content-editor"
              value={editData.content}
              onChange={(e) => setEditData({ ...editData, content: e.target.value })}
              placeholder="Write your documentation here (Markdown supported)..."
            />
            <div className="edit-actions">
              <button className="cancel-btn" onClick={() => setIsEditing(false)}>Cancel</button>
              <button className="save-btn" onClick={handleSave}>Save Documentation</button>
            </div>
          </div>
        ) : selectedPage ? (
          <div className="read-view">
            <div className="page-header">
              <h1>{selectedPage.title}</h1>
              <div className="page-meta">
                <span className="meta-item"><User size={14} /> {selectedPage.author_name}</span>
                <span className="meta-item"><Clock size={14} /> {new Date(selectedPage.updated_at).toLocaleDateString()}</span>
                <span className="meta-item"><Tag size={14} /> {selectedPage.category_name}</span>
                <button className="edit-icon-btn" onClick={() => {
                  setEditData({
                    title: selectedPage.title,
                    content: selectedPage.content,
                    category: selectedPage.category
                  });
                  setIsEditing(true);
                }}>
                  <Edit3 size={18} />
                </button>
              </div>
            </div>
            <div className="markdown-container">
              <ReactMarkdown>{selectedPage.content}</ReactMarkdown>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <Book size={64} className="book-icon" />
            <h2>Welcome to Tech Wiki</h2>
            <p>Select a page from the list or create a new one to get started.</p>
          </div>
        )}
      </div>

      <style>{`
        .wiki-container {
          display: flex;
          height: calc(100vh - 40px);
          gap: 2rem;
          background: #fff;
          border-radius: 1.5rem;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }

        .wiki-sidebar {
          width: 320px;
          border-right: 1px solid #f1f5f9;
          padding: 1.5rem;
          background: #f8fafc;
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .search-bar {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          background: #fff;
          padding: 0.75rem 1rem;
          border-radius: 1rem;
          border: 1px solid #e2e8f0;
        }

        .search-bar input {
          border: none;
          outline: none;
          width: 100%;
          font-size: 0.9rem;
        }

        .create-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          background: #B800C4;
          color: white;
          border: none;
          padding: 0.75rem;
          border-radius: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s;
        }

        .create-btn:hover {
          transform: translateY(-2px);
          background: #9d00a8;
        }

        .category-section h3, .pages-section h3 {
          font-size: 0.75rem;
          text-transform: uppercase;
          color: #94a3b8;
          letter-spacing: 0.05em;
          margin-bottom: 1rem;
        }

        .category-list, .page-list {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .category-item, .page-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem 1rem;
          border-radius: 0.75rem;
          cursor: pointer;
          font-size: 0.9rem;
          color: #475569;
          transition: all 0.2s;
        }

        .page-item:hover {
          background: #fff;
          color: #B800C4;
        }

        .page-item.active {
          background: #fff;
          color: #B800C4;
          box-shadow: 0 4px 12px rgba(184, 0, 196, 0.1);
        }

        .page-item .arrow {
          margin-left: auto;
          opacity: 0;
          transition: opacity 0.2s;
        }

        .page-item:hover .arrow, .page-item.active .arrow {
          opacity: 1;
        }

        .wiki-content {
          flex: 1;
          padding: 3rem;
          overflow-y: auto;
        }

        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #94a3b8;
          text-align: center;
        }

        .book-icon {
          margin-bottom: 1.5rem;
          opacity: 0.2;
        }

        /* Read View Styles */
        .page-header h1 {
          font-size: 2.5rem;
          font-weight: 800;
          color: #1e293b;
          margin-bottom: 1rem;
        }

        .page-meta {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          padding-bottom: 2rem;
          border-bottom: 1px solid #f1f5f9;
          margin-bottom: 2rem;
        }

        .meta-item {
          display: flex;
          align-items: center;
          gap: 0.4rem;
          font-size: 0.85rem;
          color: #64748b;
        }

        .edit-icon-btn {
          margin-left: auto;
          background: none;
          border: none;
          color: #94a3b8;
          cursor: pointer;
          transition: color 0.2s;
        }

        .edit-icon-btn:hover {
          color: #B800C4;
        }

        .markdown-container {
          line-height: 1.8;
          font-size: 1.1rem;
          color: #334155;
        }

        .markdown-container h1, .markdown-container h2, .markdown-container h3 {
          color: #1e293b;
          margin-top: 2rem;
          margin-bottom: 1rem;
        }

        .markdown-container code {
          background: #f1f5f9;
          padding: 0.2rem 0.4rem;
          border-radius: 0.3rem;
          font-family: 'Fira Code', monospace;
          font-size: 0.9em;
        }

        /* Edit View Styles */
        .edit-view {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          height: 100%;
        }

        .title-input {
          font-size: 2rem;
          font-weight: 800;
          border: none;
          border-bottom: 2px solid #f1f5f9;
          outline: none;
          padding-bottom: 0.5rem;
        }

        .category-select {
          padding: 0.75rem;
          border-radius: 0.75rem;
          border: 1px solid #e2e8f0;
          outline: none;
          width: fit-content;
        }

        .content-editor {
          flex: 1;
          border: 1px solid #e2e8f0;
          border-radius: 1rem;
          padding: 1.5rem;
          font-family: inherit;
          font-size: 1.1rem;
          resize: none;
          outline: none;
          min-height: 400px;
        }

        .edit-actions {
          display: flex;
          justify-content: flex-end;
          gap: 1rem;
        }

        .save-btn {
          background: #B800C4;
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 0.75rem;
          font-weight: 600;
          cursor: pointer;
        }

        .cancel-btn {
          background: #f1f5f9;
          color: #64748b;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 0.75rem;
          font-weight: 600;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
};

export default Wiki;
