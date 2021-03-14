const axios = require('axios');

function checkURL(){
    axios.get("https://is-it-a-safe-space-data.herokuapp.com/getData?url=" + url).then(resp => {

        resp = resp.data
        if(resp = "success"){
            alert("Your website is a safe space")
        }else{
            
        }
    
    });    
}
