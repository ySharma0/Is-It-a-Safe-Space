

function checkURL(){
    url = document.getElementById("search-bar").value
    axios.get("/getData?url=" + url).then(resp => {

        resp = resp.data
        // if(resp = "success"){
            document.write("<p>"+ resp +"</p>")
        // }else{

        // }
    
    });    
}
