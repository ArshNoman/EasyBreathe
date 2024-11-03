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
    console.log(d.substring(16, 18) +":00");
    setTime(d.substring(16, 18) +":00");
  }

  return (
    <div className='container'>
        <div className='sidebar'>
          <div className='headers'>
            <h1>EASYBREATHE</h1>
            <h3>Air Quality Predictions</h3>
          </div>
          <div className='form'>
            <div className='form-group'>
              <label>Date: </label>
              <input type="date" id="selected_date" value = {date} name="date" onChange={(e) => setDate(e.target.value)}/>
            </div>
            <div className='form-group'>
              <label>Time: </label>
              <input type="time" id="selected_time" value = {time} name="date" onChange={(e) => setTime(e.target.value)}/>
            </div>
            <div className='form-group'>
              <button onClick={() => {parseDateAndTime(new Date)}}>Now</button>
            </div>
          </div>
          <PhoneForm/>
        </div>
        <div className='map-container'>
          <MapComponent/>
        </div>
      </div>

  )
};

export default App;
