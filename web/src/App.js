import React, { useState } from 'react';
import CveList from './components/CveList';
import VMwareList from './components/VMwareList';
import MitrCveList from './components/MitrCveList'; // Добавлен импорт компонента MitrCveList
import './css/App.css';

function App() {
  const [selectedOption, setSelectedOption] = useState('CVE');

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  return (
    <div className="app">
      <h1>Недавние уязвимости:</h1>
      <div className="buttons">
        <button onClick={() => handleOptionChange('CVE')}>NVD CVE</button>
        <button onClick={() => handleOptionChange('VmWare')}>VMware CVE</button>
        <button onClick={() => handleOptionChange('MitrCve')}>MITRE CVE</button> 
      </div>
      {selectedOption === 'CVE' ? <CveList /> : null}
      {selectedOption === 'VmWare' ? <VMwareList /> : null}
      {selectedOption === 'MitrCve' ? <MitrCveList /> : null} 
    </div>
  );
}

export default App;