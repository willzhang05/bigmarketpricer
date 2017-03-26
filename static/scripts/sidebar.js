var mb = document.querySelector("#nav-button"),
    sb = document.querySelector("#sidebar"),
    wr = document.querySelector("#wrapper");

mb.addEventListener("click", function(){toggleSidebar(true)}, false);
wr.addEventListener("click", function(){toggleSidebar(false)}, false);
mb.addEventListener("touchleave", function(){toggleSidebar(true)}, false);
wr.addEventListener("touchleave", function(){toggleSidebar(false)}, false);
sb.style.disabled = true;


function toggleSidebar(toggleOpenAllowed) {
    if((sb.style.right == "" || sb.style.right == "-200px") && toggleOpenAllowed) {
        sb.style.disabled = false;
        sb.style.right = "0px";
    } else {
        sb.style.disabled = true;
        sb.style.right = "-200px";
    }
}

