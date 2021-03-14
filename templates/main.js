const axios = require('axios');

function checkURL(){
    axios.get("https://is-it-a-safe-space-data.herokuapp.com/getData?url=" + url).then(resp => {

        console.log(resp.data);
    
    });    
}
