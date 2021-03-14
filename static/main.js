function checkURL(){
    url = document.getElementById("search-bar").value
    console.log(url)
    axios.get("/getData?url=" + String(url) ).then(resp => {

        resp = resp.data
        // if(resp = "success"){
            console.log("Your listed URL is " + resp)

        // }else{

        // }
    
    });
}
