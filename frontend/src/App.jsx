import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import "./App.css"
import './styles/default.css'
import './styles/sidebar.css'
import PhoneForm from './components/PhoneForm'
import MapComponent from './components/MapComponent';

const App = () => {

  const [date, setDate] = useState("0-0-0");
  const [time, setTime] = useState("");
  const [predictions, setPredictions] = useState(getPredictions)

  async function update(isDate, value){
    if(isDate == 1){
      setDate(value);
    }else if (isDate == 2){
      setTime(value);
    }

    // send in get request here
    setPredictions(getPredictions);
    console.log(data);
  }

  function parseDateAndTime(d){
    d = "" + d;
    let day = d.substring(8, 10);
    let y = d.substring(11, 15);
    let mString = d.substring(4, 7);
    let m = "";
    if(mString == "Nov"){
      m = "11"
    }
    setDate(y + "-" + m + "-" + day);
    setTime(d.substring(16, 18) +":00");

    update(3, "");
  }

  async function getPredictions(){
    let cities = ['Apex','Asheville','Burlington','Cary', 'Concord', 'Chapel Hill', 'Charlotte', 'Durham', 'Fayetteville', 'Greensboro', 'Gastonia', 'Greenville', 'High Point', 'Huntersville', 'Jacksonville', 'Kannapolis', 'Raleigh', 'Wake Forest', 'Wilmington', 'Winston-Salem'];
    let data = [];

    for (let i = 0; i < cities.length; i++) {
        let response = await fetch(`http://127.0.0.1:5000?city=${cities[i]}&time=${date}`); // Use backticks and fix the URL parameters
        data[i] = { city: cities[i], prediction: await response.json() }; // Use object syntax correctly
    }

    return data;
  }

  return (
    <div className='container'>
        <div className='sidebar'>
          <div className='headers'>
            <h1>EASY BREATHE</h1>
            <h3>Air Quality Predictions</h3>
          </div>
          <div className='form'>
            <div className='form-group'>
              <label>Date: </label>
              <input type="date" id="selected_date" value = {date} name="date" onChange={(e) => update(1, (e.target.value))}/>
            </div>
            <div className='form-group'>
              <label>Time: </label>
              <input type="time" id="selected_time" value = {time} name="date" onChange={(e) => update(0, (e.target.value))}/>
            </div>
            <div className='form-group'>
              <button onClick={() => {parseDateAndTime(new Date)}}>Now</button>
            </div>
          </div>
          <PhoneForm/>
        </div>
        <div className='map-container'>
          <MapComponent
            predictions = {predictions}
            date = {date}
          />
        </div>
      </div>
  )
};

export default App;
