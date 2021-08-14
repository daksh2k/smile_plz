  get_log_list()
  get_summary()
  function togglelist(){
    var cntnr = $(".log-list-container")
    var btn   = $(".log-list-show")
    if(cntnr[0].style.display==="block"){
      cntnr.hide()
      btn[0].textContent = "Show All Logs"
    }
    else{
      cntnr.show()
      btn[0].textContent = "Hide Logs"
    }
  }
  function get_summary(){
    $.ajax({url: "/log_summary",
           headers:{"logdate": $("h1").text()},
           success: (res) => $(".row").prepend(res)
         });
    }
  function get_log_list(){
    $.ajax({url: "/log_all_list",
           success: (res) => {
            $(".log-list-container").append(res);
            for (const file of $(".list-group-item")){
              if(file.children[0].text.split(' ')[1] == $("h1").text().split(' ')[1]){
                file.classList.add("active")
              }
            } 
          }
        });
  }