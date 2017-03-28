var alertTime = 2000;

// JS PARA DEJAR EL VIDEO FLOTANTE CON RESPECTO AL TOP

// $(window).scroll(function (){
//   if ($(this).scrollTop() > 127.75) {
//       $('.content').addClass('fixed-content');
//       $('.playlist').addClass('fixed-playlist');
//     } else {
//       $('.content').removeClass('fixed-content');
//       $('.playlist').removeClass('fixed-playlist');
//     }
// });

$(window).resize(function() {
  var more = document.getElementById("js-navigation-more");
  if ($(more).length > 0) {
    var windowWidth = $(window).width();
    var moreLeftSideToPageLeftSide = $(more).offset().left;
    var moreLeftSideToPageRightSide = windowWidth - moreLeftSideToPageLeftSide;

    if (moreLeftSideToPageRightSide < 330) {
      $("#js-navigation-more .submenu .submenu").removeClass("fly-out-right");
      $("#js-navigation-more .submenu .submenu").addClass("fly-out-left");
    }

    if (moreLeftSideToPageRightSide > 330) {
      $("#js-navigation-more .submenu .submenu").removeClass("fly-out-left");
      $("#js-navigation-more .submenu .submenu").addClass("fly-out-right");
    }
  }
});

$(document).ready(function() {
  var menuToggle = $("#js-mobile-menu").unbind();
  $("#js-navigation-menu").removeClass("show");

  menuToggle.on("click", function(e) {
    e.preventDefault();
    $("#js-navigation-menu").slideToggle(function(){
      if($("#js-navigation-menu").is(":hidden")) {
        $("#js-navigation-menu").removeAttr("style");
      }
    });
  });

  $('.suggestions .button-suggestions').click(function() {
    $('.suggestions .url').show();
    $('.video-options').hide();
    $('#suggest-form').find('input[type=text]').focus();
  });

  $('.suggestions .button-report').click(function() {
    $('.suggestions .report').show();
    $('.video-options').hide();
    $('#report-form').find('input[type=text]').focus();
  });

  $('.close-suggestions').click(function() {
    $('.suggestions .url').hide();
    $('.suggestions .report').hide();
    $('.video-options').show();
  });

  $('.button-responsive').click(function() {
    $('.nav-responsive').toggle();
    //$(this).removeClass('.fa-angle-down')
    //$('.fa').toggleClass('.fa-angle-down .fa-angle-up');
  });

  $('.player li a').click(function() {
    $(this).toggleClass('active');
  });

  $('.player li #play').click(function() {
    $(this).hide();
    $('.player li #pause').show();
  });

  $('.player li #pause').click(function() {
    $(this).hide();
    $('.player li #play').show();
  });

  // $('.search-input').click(function (e) {
  //   $('.search-bar').css('display', 'block');
  // });

  $(document).click(function() {
    $('.search-bar').css('display', 'inline-block');
    $('#expander-content-1').hide();
    $('#expander-content-2').hide();
  });

  $('.search-input').click(function(e){
      $('.search-bar').css('background', '#fff');
      $('.search-bar').css('display', 'block');
      e.stopPropagation();
  });

  // Expander


  $('#expander-button-1').click(function(e) {
    $('#expander-content-1').toggle();
    $('#expander-content-2').hide();
    e.stopPropagation();
  });

  $('#expander-button-2').click(function(e) {
    $('#expander-content-2').toggle();
    $('#expander-content-1').hide();
    e.stopPropagation();
  });


  $('#avatar-edit').click(function() {
    var image_form = $('#id_avatar');
    image_form.trigger('click');
    });

    $('#id_avatar').change(function(){
      var image_div = $('#avatar-image');
      if (this.files && this.files[0]) {
        var file = this.files[0];
        var img = document.createElement('img');
        var reader = new FileReader();
        reader.onload = function (e) {
          $(image_div).css('background-image', 'url("' + e.target.result + '")');
        }
        // reader.readAsDataURL(file);
        reader.readAsDataURL(this.files[0]);
      }
    });

  setTimeout(function() {
      $('.alert-onload').each(function(i, obj) {
        $(this).fadeOut();
      });
  }, alertTime);

  if($("input[name='q']").val()){
    $("input[name='q']").focus().val($("input[name='q']").val());
  }

});


function createAlert(text, alertType) {
  var alert = $('#alert-template').clone();
  alert.addClass('alert-' + alertType)
  alert.find('.alert-text').html(text);
  alert.show();
  alert.appendTo('#messages');
  setTimeout(function() {
    alert.fadeOut('fast', function() {
      alert.remove();
    });
  }, alertTime);
};

function scrollTo(elemId) {
  $('html, body').animate({
      scrollTop: $(elemId).offset().top - 25
  }, 50);
};
