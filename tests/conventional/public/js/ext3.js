// URL Parameters
const url = new URLSearchParams(window.location.search); // or location.search
const urlParam = url.get('param2');
if (urlParam != null) {
    document.getElementById("urlParam").innerHTML = urlParam;
}

document.getElementById("urlParam").innerHTML += " || " + location.search;

// Cookie
document.getElementById("cookie").innerHTML = document.cookie;

// Fragment
document.getElementById("fragment").innerHTML = window.location.hash.substring(1);

// URL & URI
document.getElementById("url").outerHTML = document.URL + " || " + document.documentURI;

// Referrer (but not the header)
console.log(document.referrer);
document.getElementById("refer").insertAdjacentHTML("afterend", document.referrer);