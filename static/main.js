

function checkURL(){
    axios.get("/getData?url=" + document.getElementById("search-bar").value).then(resp => {

        resp = resp.data
        // if(resp = "success"){
            document.write("<p>"+ resp +"</p>")
        // }else{

        // }
    
    });    
}
