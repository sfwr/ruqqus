// Flag Comment

report_commentModal = function(id, author, board) {

  document.getElementById("comment-author").textContent = author;

  document.getElementById('report-comment-to-guild-dropdown-option').innerHTML= 'This comment is off-topic for +' + board;

    document.getElementById("reportCommentButton").onclick = function() {

      this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting comment';
      this.disabled = true;
      post('/api/flag/comment/' + id,
        callback = function() {

          document.getElementById("reportCommentFormBefore").classList.add('d-none');
          document.getElementById("reportCommentFormAfter").classList.remove('d-none');
        }
        )
    }

};

$('#reportCommentModal').on('hidden.bs.modal', function () {

  var button = document.getElementById("reportCommentButton");

  var beforeModal = document.getElementById("reportCommentFormBefore");
  var afterModal = document.getElementById("reportCommentFormAfter");

  button.innerHTML='Report comment';
  button.disabled= false;
  afterModal.classList.add('d-none');

  if ( beforeModal.classList.contains('d-none') ) {
    beforeModal.classList.remove('d-none');
  }

});


// Flag Submission

report_postModal = function(id, author, board) {

  document.getElementById("post-author").textContent = author;

  document.getElementById('report-post-to-guild-dropdown-option').innerHTML= 'This post is off-topic for +' + board;

    document.getElementById("reportPostButton").onclick = function() {

      this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting post';
      this.disabled = true;

      function post(url, callback, errortext) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        var form = new FormData()
        form.append("formkey", formkey());
	form.append("report_type", document.getElementById("report-type-dropdown").value);
        xhr.withCredentials=true;
        xhr.onload=function() {
          document.getElementById("reportPostFormBefore").classList.add('d-none');
          document.getElementById("reportPostFormAfter").classList.remove('d-none');
        };
        xhr.onerror=function(){alert(errortext)};
        xhr.send(form);
      }

    }
};

$('#reportPostModal').on('hidden.bs.modal', function () {

  var button = document.getElementById("reportPostButton");

  var beforeModal = document.getElementById("reportPostFormBefore");
  var afterModal = document.getElementById("reportPostFormAfter");

  button.innerHTML='Report post';
  button.disabled= false;

  afterModal.classList.add('d-none');

  if ( beforeModal.classList.contains('d-none') ) {
    beforeModal.classList.remove('d-none');
  }

});