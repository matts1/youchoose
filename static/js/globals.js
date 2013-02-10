var navitems = $('nav a.first');
var url = document.URL.replace(new RegExp(".*?://[^/]*"), "");
//port://as many non slashes as you can match
for (var i = 0; i < navitems.length; i++) {
    var link = $(navitems[i]).attr('href');
    if (url.match(new RegExp("^" + link))) {
        $(navitems[i]).css('background-color', '#F57218');
    }
}
