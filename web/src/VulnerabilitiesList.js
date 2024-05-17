import React, { useState, useEffect } from 'react';
import axios from 'axios';

function VulnerabilitiesList() {
  const [vulnerabilities, setVulnerabilities] = useState([]);

  useEffect(() => {
    fetchVulnerabilities();
  }, []);

  const fetchVulnerabilities = () => {
    axios.get('http://localhost:9000/api/cve')
      .then(response => {
        if (response.data && response.data.vulnerabilities) {
          const sortedVulnerabilities = response.data.vulnerabilities.sort((a, b) => {
            return new Date(b.cve.lastModified) - new Date(a.cve.lastModified);
          });
          setVulnerabilities(sortedVulnerabilities);
        } else {
          console.error('No vulnerabilities data found');
        }
      })
      .catch(error => {
        console.error('Error fetching vulnerabilities:', error);
      });
  };

  return (
    <div className="vulnerabilities-list">
      <h2>CVE</h2>
      {vulnerabilities.map((vulnerability, index) => (
        <div key={index}>
          <h3>CVE ID: {vulnerability.cve.id}</h3>
          <p>Published: {vulnerability.cve.published}</p>
          <p>Last Modified: {vulnerability.cve.lastModified}</p>
          <p>Vulnerability Status: {vulnerability.cve.vulnStatus}</p>
          <p>Description: {vulnerability.cve.descriptions[0].value}</p>
        </div>
      ))}
    </div>
  );
}

export default VulnerabilitiesList;