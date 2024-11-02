import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import "./App.css"
import './styles/default.css'
import './styles/sidebar.css'
import PhoneForm from './components/PhoneForm'
import MapComponent from './components/MapComponent';




const App = () => {
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
              <input type="date" id="selected_date" name="date"/>
            </div>
            <div className='form-group'>
              <button>Today</button>
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

/*

      */