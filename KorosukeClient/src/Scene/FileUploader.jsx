import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const FileUploader = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [modelPreparing, setModelPreparing] = useState(false);
  const [chatbtn, setChat] = useState(false);

  const fetchCurrentModel = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/currentmodel/');
      console.log("RES", res.data.modelname);
      setChat(res.data.modelname === localStorage.getItem('username'));
    } catch (error) {
      console.error('Error fetching current model:', error);
    }
  };

  const fetchFiles = async () => {
    const username = 'sushil';
    try {
      const response = await axios.get('http://127.0.0.1:8000/files/', {
        params: { username }
      });
      setFiles(response.data.files);
      setChat(false);
      await fetchCurrentModel();
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const formData = new FormData();
    formData.append('file', event.target.files[0]);
    formData.append('username', 'sushil');

    setUploading(true);
    try {
      await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await fetchFiles();
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setUploading(false);
    }
  };

  const handlePrepareModel = async () => {
    setModelPreparing(true);
    const formData = new FormData();
    formData.append('username', 'sushil');
    try {
      const response = await axios.post('http://127.0.0.1:8000/start_model/', formData);
      if (response.status === 200) {
        alert('Model prepared successfully');
      }
    } catch (error) {
      console.error('Error preparing model:', error);
    } finally {
      setModelPreparing(false);
      await fetchCurrentModel();
    }
  };

  const handleDeleteFile = async (filename) => {
    const username = localStorage.getItem('username');
    try {
      await axios.delete(`http://127.0.0.1:8000/delete/${filename}`, {
        params: { username }
      });
      await fetchFiles();
    } catch (error) {
      console.error('Error deleting file:', error);
    }
  };

  useEffect(() => {
    fetchFiles();
    localStorage.setItem('username', "sushil");
  }, []);

  return (
    <div style={styles.container}>
      <input
        type="file"
        onChange={handleFileUpload}
        style={styles.uploadButton}
        disabled={uploading}
      />
      <div style={styles.fileList}>
        {files.length === 0 ? (
          <p style={styles.noFilesText}>No files uploaded yet.</p>
        ) : (
          <ul>
            {files.map((file, index) => (
              <li key={index} style={styles.fileItem}>
                {file}
                <button
                  onClick={() => handleDeleteFile(file)}
                  style={styles.deleteButton}
                >
                  &times;
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      {files.length > 0 && (
        <div style={styles.buttonsContainer}>
          <button
            onClick={handlePrepareModel}
            style={styles.prepareButton}
            disabled={modelPreparing}
          >
            {modelPreparing ? 'Preparing model...' : 'Prepare model'}
          </button>
          {chatbtn && (
            <Link to={"/testchat"}>
              <button style={styles.chatButton}>Chat</button>
            </Link>
          )}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    padding: '20px',
    backgroundImage: 'url("https://source.unsplash.com/1600x900/?technology,dark")', // Classy background image
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    color: '#f1f1f1',
    fontFamily: "'Roboto', sans-serif",
    textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)',
  },
  uploadButton: {
    marginBottom: '20px',
    backgroundColor: 'rgba(42, 42, 45, 0.9)',
    color: '#f1f1f1',
    padding: '12px 24px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '10px',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(10px)',
  },
  fileList: {
    width: '80%',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '12px',
    padding: '15px',
    textAlign: 'left',
    backgroundColor: 'rgba(36, 36, 38, 0.9)',
    color: '#f1f1f1',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)',
    maxHeight: '300px',
    overflowY: 'auto',
    backdropFilter: 'blur(10px)',
  },
  noFilesText: {
    color: '#bbbbbb',
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: '10px',
  },
  fileItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '8px 0',
    borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
  },
  deleteButton: {
    background: 'none',
    border: 'none',
    color: '#ff6961',
    fontSize: '20px',
    cursor: 'pointer',
    transition: 'color 0.3s ease',
  },
  buttonsContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    width: '80%',
    marginTop: '20px',
    gap: '15px',
  },
  prepareButton: {
    padding: '12px 24px',
    backgroundColor: 'rgba(75, 175, 80, 0.9)',
    color: '#ffffff',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '10px',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(10px)',
  },
  chatButton: {
    padding: '12px 24px',
    backgroundColor: 'rgba(0, 140, 186, 0.9)',
    color: '#ffffff',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '10px',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(10px)',
  },
};

// Add hover effects for buttons
styles.uploadButton[':hover'] = {
  backgroundColor: 'rgba(53, 53, 55, 0.95)',
  transform: 'scale(1.05)',
};
styles.deleteButton[':hover'] = {
  color: '#ff4a4a',
};
styles.prepareButton[':hover'] = {
  backgroundColor: 'rgba(69, 160, 73, 0.95)',
  transform: 'translateY(-2px)',
};
styles.chatButton[':hover'] = {
  backgroundColor: 'rgba(0, 122, 165, 0.95)',
  transform: 'translateY(-2px)',
};


export default FileUploader;
