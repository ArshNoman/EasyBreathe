import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import "./App.css"
import './styles/default.css'
import './styles/sidebar.css'
import PhoneForm from './components/PhoneForm'
import MapComponent from './components/MapComponent';

const App = () => {

  const [date, setDate] = useState("0000-00-00");
  const [time, setTime] = useState("");

  useEffect(() => {
    console.log(`Updated Date: ${date}, Updated Time: ${time}`);
  }, [date, time])

  function update(isDate, value){
    if(isDate == 1){
      setDate(value);
    }else if (isDate == 0){
      setTime(value);
    }
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
              <input type="date" id="selected_date" value = {date} name="date" onChange={(e) => setDate(e.target.value)}/>
            </div>
            <div className='form-group'>
              <label>Time: </label>
              <input type="time" id="selected_time" value = {time} name="time" onChange={(e) => update(0, e.target.value)}/>
            </div>
            <div className='form-group'>
              <button onClick={() => {parseDateAndTime(new Date)}}>Now</button>
            </div>
          </div>
          <PhoneForm/>
        </div>
        <div className='map-container'>
          <MapComponent
            date = {date}
            time = {time}
          />
        </div>
      </div>
  )
};

export default App;
