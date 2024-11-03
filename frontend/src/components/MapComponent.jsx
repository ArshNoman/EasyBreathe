import 'leaflet/dist/leaflet.css';

import { MapContainer, TileLayer, Popup, Marker, SVGOverlay } from 'react-leaflet'

function MapComponent(props){

  const predictions = props.predictions;

  const bigLocations = [ { name: "Raleigh", position: { lat: 35.7796, lng: -78.6382 } }, { name: "Durham", position: { lat: 35.9940, lng: -78.8986 } }, { name: "Chapel Hill", position: { lat: 35.9132, lng: -79.0558 } }];
  const smallLocations =  [ { name: "Charlotte", lat: 35.2271, lng: -80.8431 }, { name: "Greensboro", lat: 36.0726, lng: -79.7920 }, { name: "Winston-Salem", lat: 36.0999, lng: -80.2442 }, { name: "Fayetteville", lat: 35.0527, lng: -78.8784 }, { name: "Cary", lat: 35.7915, lng: -78.7811 }, { name: "Wilmington", lat: 34.2257, lng: -77.9447 }, { name: "High Point", lat: 35.9557, lng: -80.0053 }, { name: "Concord", lat: 35.4088, lng: -80.5795 }, { name: "Asheville", lat: 35.5951, lng: -82.5515 }, { name: "Greenville", lat: 35.6127, lng: -77.3664 }, { name: "Gastonia", lat: 35.2621, lng: -81.1873 }, { name: "Jacksonville", lat: 34.7541, lng: -77.4302 }, { name: "Huntersville", lat: 35.4107, lng: -80.8428 }, { name: "Apex", lat: 35.7327, lng: -78.8503 }, { name: "Burlington", lat: 36.0957, lng: -79.4378 }, { name: "Kannapolis", lat: 35.4874, lng: -80.6217 }, { name: "Wake Forest", lat: 35.9799, lng: -78.5097 }  ];
  const position = {lat: 61.2176, lng: -149.8997};
  return (
    <MapContainer style={{ height: '100vh' }} center={[36, -79]} zoom={9} scrollWheelZoom={false}>
    <TileLayer
   url='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
   maxZoom= {20}
   subdomains={['mt1','mt2','mt3']}
/>
      {smallLocations.map((elem, index) => { return <SVGOverlay key = {index} attributes={{ stroke: '#2D6CDF' }} bounds={[[elem.lat, elem.lng], [elem.lat + 0.05, elem.lng + 0.25]]}> <text x="25%" y="65%" stroke={"red"}> {elem.name}</text></SVGOverlay>})}
      {bigLocations.map((elem, index) => { return <SVGOverlay key = {index} attributes={{ stroke: 'red' }} bounds={[[elem.position.lat, elem.position.lng], [elem.position.lat + 0.05, elem.position.lng + 0.25]]}> <text x="25%" y="65%" stroke={"red"}> {elem.name}</text></SVGOverlay>})}
      {bigLocations.map((elem, index) =>  {return <Marker position={[elem.position.lat, elem.position.lng]}> <Popup> {elem.name} </Popup></Marker>})}
      {smallLocations.map((elem, index) =>  {return <Marker position={[elem.lat, elem.lng]}> <Popup> {elem.name} </Popup></Marker>})}
    </MapContainer>
  );
};

export default MapComponent;

