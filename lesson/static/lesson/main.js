var prevfaq = "";
    function faqclick(faq) {
        var info = document.getElementById(faq);
       
        if (info.style.maxHeight != "300px") { //Checks if paragraph tag is open
            if (prevfaq != "") { //Checks if another faq tab is open, closes if it is
                var prev = document.getElementById(prevfaq);
                prev.style.WebkitTransform = "perspective(400) rotate3d(1,0,0,-90deg)";
                prev.style.maxHeight = "0px";}
               
            info.style.WebkitTransform = "perspective(400) rotate3d(0,0,0,0)";
            info.style.maxHeight = "300px";
            prevfaq = faq;}
        else { //If paragraph tag is closed (No faq paragraphs are visible)
            info.style.WebkitTransform = "perspective(400) rotate3d(1,0,0,-90deg)";
            info.style.maxHeight = "0px";
            prevfaq = "";}
    }
	
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}
function expandAdvanced() {
  document.getElementById("dropdown-advanced-id").classList.toggle("show");
  document.getElementById("dropdown-advanced-id").classList.toggle("content-show");
  document.getElementById("dropped").classList.toggle("button-edit");
}