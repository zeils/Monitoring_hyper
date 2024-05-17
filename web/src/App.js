import React, { useState } from 'react';
import VulnerabilitiesList from './VulnerabilitiesList';
import VMwareList from './VMwareList';

function App() {
  const [selectedOption, setSelectedOption] = useState('CVE');

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  return (
    <div className="app">
      <h1>Недавние уязвимости:</h1>
      <div className="buttons">
        <button onClick={() => handleOptionChange('CVE')}>CVE</button>
        <button onClick={() => handleOptionChange('VmWare')}>VmWare</button>
      </div>
      {selectedOption === 'CVE' ? <VulnerabilitiesList /> : <VMwareList />}
    </div>
  );
}

export default App;