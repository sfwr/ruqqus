// Flag Comment

report_commentModal = function(id) {

  var dropdown = document.getElementById("reportCommentDropdown");
  var reason = dropdown.options[dropdown.selectedIndex].value;

  if (reason == "breaks policy") {
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
  } else {
    document.getElementById("reportCommentButton").onclick = function() {

      this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting comment';
      this.disabled = true;
      post('/api/report/comment/' + id,
        callback = function() {

          document.getElementById("reportCommentFormBefore").classList.add('d-none');
          document.getElementById("reportCommentFormAfter").classList.remove('d-none');
        }
        )
    }
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

report_postModal = function(id) {

  var dropdown = document.getElementById("reportPostDropdown");
  var reason = dropdown.options[dropdown.selectedIndex].value;


  if (reason == "breaks policy") {

    document.getElementById("reportPostButton").onclick = function() {

      this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting post';
      this.disabled = true;
      post('/api/flag/post/' + id,
        callback = function() {

          document.getElementById("reportPostFormBefore").classList.add('d-none');
          document.getElementById("reportPostFormAfter").classList.remove('d-none');
        }
        )
    }
  }
  else {
    document.getElementById("reportPostButton").onclick = function() {

      this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting post';
      this.disabled = true;
      post('/api/report/post/' + id,
        callback = function() {

          document.getElementById("reportPostFormBefore").classList.add('d-none');
          document.getElementById("reportPostFormAfter").classList.remove('d-none');
        }
        )
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