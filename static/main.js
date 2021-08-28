// Get summary of the todays tweets.
(function get_summary(){
  $.ajax({url: "/log_summary",
         headers:{"logdate": $("h1").text()},
         success: (res) => {
           $(".row").prepend(res)
           updateScrollButtons()
          }
       });
  })();

// Get list of all logs present. 
(function get_log_list(){
  $.ajax({url: "/log_all_list",
         success: (res) => {
          $(".log-list-container").append(res);
          $(".list-group-item").each( function (){
            if(this.children[0].text.split(' ')[1] == $("h1").text().split(' ')[1]){
              $(this).addClass("active")
            }
          })
        }
      });
})();

/* Add event listener for long press on arrow buttons
Credits- https://github.com/john-doherty/long-press-event */
$(".s-up").on('long-press',(evt) => {
  evt.preventDefault() 
  scrollToTop()
});
$(".s-down").on('long-press',(evt) => {
  evt.preventDefault() 
  scrollToBottom()
});

// Add Event Listener for right click on arrow buttons (easier on desktop)
$(".s-up").on('contextmenu',(evt) => {
  evt.preventDefault() 
  scrollToTop()
});
$(".s-down").on('contextmenu', (evt) => {
  evt.preventDefault() 
  scrollToBottom()
});

// Hide scroll buttons according to scroll position
$(document).on("scroll",updateScrollButtons)

// Scroll to the top of the document
function scrollToTop(){
  $([document.documentElement, document.body]).animate({
    scrollTop: 0
  }, 800,"linear");
}

// Scroll to the bottom of the document
function scrollToBottom(){
  $([document.documentElement, document.body]).animate({
    scrollTop: $(document).height()
  }, 800,"linear");
}

// Hiding scroll buttons when at the top or at the bottom
function updateScrollButtons(){
  const docHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
  const currLoc = document.documentElement.scrollTop || document.body.scrollTop;
  if (currLoc< 400)
    $(".s-up").hide(200);
  else
    $(".s-up").show(200);
  if(docHeight-currLoc < docHeight/15)
    $(".s-down").hide(200);
  else
    $(".s-down").show(200);  
}

// For Showing the log list on button press
function togglelist(){
  var cntnr = $(".log-list-container")
  var btn   = $(".log-list-show")
  if(cntnr.css('display')==="block"){
    cntnr.hide()
    btn[0].textContent = "Show All Logs"
  }
  else{
    cntnr.show()
    btn[0].textContent = "Hide Logs"
  }
}

//  Scroll to the next session based on current session in viewport
//  on arrow down button press 
function scrollNext()  {
  const topmin = [];
  $(".cols").each( function() {
    const rect = this.getBoundingClientRect();
    topmin.push(Math.abs(rect.top))
  })
  var idno = topmin.indexOf(Math.min(...topmin))+1
  var eleclass = ".ses-"+ idno
  if ( idno < topmin.length ){
      $([document.documentElement, document.body]).animate({
          scrollTop: $(eleclass).offset().top - 35
    }, 250);
  }
  else
    scrollToBottom()
 }

//  Scroll to the session before based on current session in viewport
//  on arrow up button press 
function scrollBefore(){
  const topmin = [];
  $(".cols").each( function() {
    const rect = this.getBoundingClientRect();
    topmin.push(Math.abs(rect.top))
  })
  var idno = topmin.indexOf(Math.min(...topmin))-1
  var eleclass = ".ses-"+ idno
  if(idno>=0){
    $([document.documentElement, document.body]).animate({
      scrollTop: $(eleclass).offset().top - 35
    }, 250);
  }
  else
    scrollToTop()
}