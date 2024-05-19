import React, { useState } from 'react';
import CveList from './components/CveList';
import VMwareList from './components/VMwareList';
import './css/App.css'

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
        <button onClick={() => handleOptionChange('VmWare')}>VMware</button>
      </div>
      {selectedOption === 'CVE' ? <CveList /> : <VMwareList />}
    </div>
  );
}

export default App;