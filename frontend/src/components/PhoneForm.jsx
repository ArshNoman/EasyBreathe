import "../styles/default.css"
import "../styles/sidebar.css"

function PhoneForm(){
    return (
        <div className="form phone-form">
            <div className="warnings">
                <h3>Bad Air Quality can lead anything from coughing to major lung issues! </h3>
                <p>message me when it gets bad!</p>
            </div>
            <div className="inputs-group">
                <input type = "email" placeholder = "example@gmail.com"/>
                <button className="phone-btn">SEND ALERTS</button>
            </div>
        </div>
    )
}

export default PhoneForm;