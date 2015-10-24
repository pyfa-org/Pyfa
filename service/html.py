# HTML is stored here as frankly I'm not sure how loading a file would work with
# our current zipfile packaging (and I'm too lazy to find out)

HTML = '''
<!DOCTYPE html>
<html>
<body>
Done. Please close this window.
<script type="text/javascript">
function extractFromHash(name, hash) {
    var match = hash.match(new RegExp(name + "=([^&]+)"));
    return !!match && match[1];
}

var hash = window.location.hash;
var token = extractFromHash("access_token", hash);

if (token){
    var redirect = window.location.origin.concat('/?', window.location.hash.substr(1));
    window.location = redirect;
}
else {
    console.log("do nothing");
}
</script>
</body>
</html>
'''
