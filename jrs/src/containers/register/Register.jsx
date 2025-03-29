import React from 'react'
import './register.css';
import { useState } from 'react';

const Register = () => {

  const [formData, setFormData] = useState({});
  const [tableData, setTableData] = useState([]);

  async function submitForm() {
    const response = await fetch('http://127.0.0.1:5000/ipc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    const json = await response.json();
    const ipcData = json.ipc;
    setTableData(ipcData);
  }
  function handleClick(event) {
    event.preventDefault();
    console.log('Button clicked');
    submitForm();
  }

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  }

  function renderTableData() {
    return (
      <tbody class="table_body">
        {tableData.map((innerList, index) => (
          <tr key={index}>
            <td class="table_data">{innerList[0]}</td>
            <td class="table_data">{innerList[1]}</td>
          </tr>
        ))}
      </tbody>
    );
  }

  return (
    <div className='reg_title'>
      <div className='reg_title_header'></div>
      <h1 className="gradient__text">Violation Of IPC Section</h1>

      <div className="jrs__header-content__input">
        <input type="text" placeholder="Case Detail" name="description" onChange={handleChange} />
        <a href="/register"><button onClick={handleClick} type="button" id='detail_button'>Detail</button></a>
      </div>
      <table className='ipc_table'>
        <thead class="table-header">
          <tr>
            <th class="header__item">Section Number</th>
            <th class="header__item">Description</th>
          </tr>
        </thead>
        {renderTableData()}
      </table>
    </div>


  )
}

export default Register

