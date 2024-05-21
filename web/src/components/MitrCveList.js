import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/MitrCveList.css';
function MitrCveList() {
  const [cveList, setCveList] = useState([]);

  useEffect(() => {
    fetchCveList();
  }, []);

  const fetchCveList = async () => {
    try {
      const response = await axios.get(process.env.REACT_APP_server_mitr_cve_endpoint);
      setCveList(response.data);
    } catch (error) {
      console.error('Error fetching CVE list:', error);
    }
  };

  return (
    <div>
      <ul>
        {cveList.map(cve => (
          <li key={cve.id}>
            <strong>ID:</strong> {cve.id}<br />
            <strong>Published:</strong> {cve.Published}<br />
            <strong>Summary:</strong> {cve.summary}<br />
            <strong>References:</strong>
            <ul>
              {cve.references.map(reference => (
                <li key={reference}>{reference}</li>
              ))}
            </ul>
            <hr />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MitrCveList;