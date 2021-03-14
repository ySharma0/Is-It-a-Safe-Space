

function checkURL(){
    url = document.getElementById("search-bar").value
    console.log(String(url))

    axios.get("/getData?url=" + (String(url)).then(resp => {

        resp = resp.data
        // if(resp = "success"){
            console.log("<p>"+ resp +"</p>")

        // }else{

        // }
    
    });    
}
