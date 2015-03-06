
window.setInterval(function () {
  $.ajax({
      url: "/socialnetwork/get-posts/" + $("#last_post_num").val() ,
      dataType : "html",
      data: $(this).serialize(),
      success: function(data) {
        $(".post_stream").prepend(data);

        // Update last post value
        last1 = $("#last").val();
        $("#last_post_num").val(last1);

        // Add comment functionality to new post, then eliminate new post class
        comment();
        $(".new_comment_submit").removeClass("new_comment_submit");

        console.log("YES");
      },
      error: function(data) {
          console.log("No new");

          last1 = $("#last").val()
          $("#last_post_num").val(last1)

      },
  });
}, 5000);


// POST comments
$(document).ready(function() {
    $('.comment_submit').submit(function(e) {
      e.preventDefault();
      myself = $(this);
      console.log(myself)
      $.ajax({
              type: "POST",
              dataType: "html",
              url: $(this).attr('action'),
              data: $(this).serialize(),
              success: function(data) {
                  myself.before(data);
                  console.log("YES");
                  $('input[type=text]').val(''); 
              },
              error: function(data) {
                  console.log("NO");
              },
          });
    return false;
    });

});

// add comment posting functionality to new, ajax-loaded posts
function comment() {
  $('.new_comment_submit').submit(function(e) {

    e.preventDefault();
    myself = $(this);
    console.log(myself)
    $.ajax({
            type: "POST",
            dataType: "html",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                myself.before(data);
                console.log("YES");
            },
            error: function(data) {
                console.log("NO");
            },
        });
  return false;
  });
}
