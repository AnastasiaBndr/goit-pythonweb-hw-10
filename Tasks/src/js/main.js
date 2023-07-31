import axios from "axios";

axios.get('https://fortnite-api.com/v1/map').then(response=>{
    console.log(response);
}).catch(error=>{console.log(error)});