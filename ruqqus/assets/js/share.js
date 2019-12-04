// Share Comment

share_commentModal = function(url, snippet) {

document.getElementById("share-modal-title").innerHTML = "Share comment";

document.getElementById("twitter-share").href = "http://twitter.com/share?text=" + snippet + "&url=" + url + "&hashtags=#MakeARuqqus";

document.getElementById("fb-share").href = "https://www.facebook.com/sharer/sharer.php?u=" + url + "&t=" + snippet;

document.getElementById("reddit-share").href = "http://www.reddit.com/submit?url=" + url + "&title=" + snippet;

document.getElementById("whatsapp-share").href = "https://api.whatsapp.com/send?text=" + url;

document.getElementById("telegram-share").href = "https://telegram.me/share/url?url=" + url + "&text=" + snippet;

document.getElementById("sms-share").href = "sms://?body=" + url;

document.getElementById("clipboard-link").value = url;

};

// Share Submission

share_postModal = function(url, title) {

document.getElementById("share-modal-title").innerHTML = "Share post";

document.getElementById("twitter-share").href = "http://twitter.com/share?text=" + title + "&url=" + url + "&hashtags=#MakeARuqqus";

document.getElementById("fb-share").href = "https://www.facebook.com/sharer/sharer.php?u=" + url + "&t=" + title;

document.getElementById("reddit-share").href = "http://www.reddit.com/submit?url=" + url + "&title=" + title;

document.getElementById("whatsapp-share").href = "https://api.whatsapp.com/send?text=" + url;

document.getElementById("telegram-share").href = "https://telegram.me/share/url?url=" + url + "&text=" + title;

document.getElementById("sms-share").href = "sms://?body=" + url;

document.getElementById("clipboard-link").value = url;

};

var clipboard = new ClipboardJS('.share-modal-link');
  clipboard.on('success', function(e) {

    document.getElementById("clipboard-link").innerHTML = '<span class="text-success">Copied!</span>';
    console.log(e);
  });
  clipboard.on('error', function(e) {

    document.getElementById("clipboard-link").innerHTML = '<span class="text-success">Copy failed...</span>';
    console.log(e);
});