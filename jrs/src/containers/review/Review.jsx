import React from 'react'
import './review.css';
import { useState } from 'react';

const Review = () => {

  const [formData, setFormData] = useState({});
  const [tableData, setTableData] = useState([]);

  async function submitForm() {
    const response = await fetch('http://127.0.0.1:5000/cases', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    const json = await response.json();
    const caseData = json.cases;
    setTableData(caseData);
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
            <td class="table_data">{innerList[2]}</td>
            <td class="table_data">{innerList[3]}</td>
          </tr>
        ))}
      </tbody>
    );
  }


  return (
    <div className='review_title'>
      <h1 className="gradient__text" >Recommendation Of Similar Cases</h1>


      <div className="jrs__header-content__input">
        <input type="email" placeholder="Case Date" name="date" onChange={handleChange} />
      </div>

      <div className="jrs__header-content__input">
        <input type="email" placeholder="Case Detail" name="text" onChange={handleChange} />
        <a href="/register"><button type="button" onClick={handleClick}>Detail</button></a>
      </div>
      <table className='case_table'>
        <thead class="table-header">
          <tr>
            <th class="header__item">Case Name</th>
            <th class="header__item">Winning Party</th>
            <th class="header__item">Arguments</th>
            <th class="header__item">Case Description</th>
          </tr>
        </thead>
        {renderTableData()}
      </table>


    </div>
  )
}

export default Review
