import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/VMwareList.css';

function VMwareList() {
  const [htmlContent, setHtmlContent] = useState('');

  useEffect(() => {
    fetchHtmlContent();
  }, []);

  const fetchHtmlContent = async () => {
    try {
      const response = await axios.get(process.env.REACT_APP_server_vmware_cve_endpoint);
      setHtmlContent(response.data);
    } catch (error) {
      console.error('Error fetching HTML content:', error);
    }
  };

  return (
    <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
  );
}

export default VMwareList;