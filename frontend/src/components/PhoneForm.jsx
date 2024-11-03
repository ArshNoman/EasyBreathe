import { useState } from "react";
import "../styles/default.css"
import "../styles/sidebar.css"

function PhoneForm(){

    const [email, setEmail] = useState("");

    function addEmail(){
        console.log("sdfsdf");
        // post request
    }

    return (
        <div className="form phone-form">
            <div className="warnings">
                <h3>Bad Air Quality can lead anything from coughing to major lung issues! </h3>
                <p>message me when it gets bad!</p>
            </div>
            <div className="inputs-group">
                <p className="label">I'm from: </p>
                <select name="city" id="city">
                    <option value="Raleigh">Raleigh</option>
                    <option value="Durham">Durham</option>
                    <option value="Chapel Hill">Chapel Hill</option>
                    <option value="Charlotte">Charlotte</option>
                    <option value="Greensboro">Greensboro</option>
                    <option value="Winston-Salem">Winston-Salem</option>
                    <option value="Fayetteville">Fayetteville</option>
                    <option value="Cary">Cary</option>
                    <option value="Wilmington">Wilmington</option>
                    <option value="High Point">High Point</option>
                    <option value="Concord">Concord</option>
                    <option value="Asheville">Asheville</option>
                    <option value="Greenville">Greenville</option>
                    <option value="Gastonia">Gastonia</option>
                    <option value="Jacksonville">Jacksonville</option>
                    <option value="Huntersville">Huntersville</option>
                    <option value="Apex">Apex</option>
                    <option value="Burlington">Burlington</option>
                    <option value="Kannapolis">Kannapolis</option>
                    <option value="Wake Forest">Wake Forest</option>
                </select>
                <p className="label">Email me at:</p>
                <input type = "email" placeholder = "example@gmail.com"/>
                <button className="phone-btn" onClick={() => {addEmail()}}>SEND ALERTS</button>
            </div>

        </div>
    )
}

export default PhoneForm;
