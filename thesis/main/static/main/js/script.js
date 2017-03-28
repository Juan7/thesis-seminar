$(document).ready(function() {
  $('.date-display').click(function() {
    $('.date-edit').toggle();
  });

  $('.expand').click(function() {
    $(this).closest('tr').find('.details').toggle();
  });

  $('.expander-button-1').click(function() {
    $('.expander-content-1').toggle();
  });
});


/**
 * picker
 */

var startDate,
 endDate,
 updateStartDate = function() {
     startPicker.setStartRange(startDate);
     endPicker.setStartRange(startDate);
     endPicker.setMinDate(startDate);
 },
 updateEndDate = function() {
     startPicker.setEndRange(endDate);
     startPicker.setMaxDate(endDate);
     endPicker.setEndRange(endDate);
 },
 startPicker = new Pikaday({
     field: document.getElementById('id_start_date'),
     minDate: new Date(2015, 0, 1),
     maxDate: new Date(2020, 12, 31),
     showDaysInNextAndPreviousMonths: true,
     onSelect: function() {
         startDate = this.getDate();
         updateStartDate();
     }
 }),
 endPicker = new Pikaday({
     field: document.getElementById('id_end_date'),
     minDate: new Date(2015, 0, 1),
     maxDate: new Date(2020, 12, 31),
     showDaysInNextAndPreviousMonths: true,
     onSelect: function() {
         endDate = this.getDate();
         updateEndDate();
     }
 }),
 _startDate = startPicker.getDate(),
 _endDate = endPicker.getDate();

if (_startDate) {
   startDate = _startDate;
   updateStartDate();
}

if (_endDate) {
   endDate = _endDate;
   updateEndDate();
}


Chart.defaults.global.defaultFontFamily = "'Verdana', sans-serif";
Chart.defaults.global.legend.display = false;
Chart.defaults.global.elements.line.tension = 0;
Chart.defaults.global.hover.mode = 'x-axis';
Chart.defaults.global.tooltips.mode = 'x-axis';
Chart.defaults.global.tooltips.titleFontStyle = 'normal';
Chart.defaults.global.tooltips.bodyFontStyle = 'bold';


function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

function intcomma(x, decimals) {
    decimals = decimals || 2;
    return round(x, decimals).toFixed(decimals).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// Popup javascript bid form

// function showMessageBox (obj){
//   console.log(obj);
//   $(".confirm").attr("href",  obj.attr("href") );
// };

// $(function() {
//   $(".confirm").click(function(event){
//      $('#bid-form').submit();
//   });
// })

$(function() {
  $(".popup-link").click(function(event){
      $(".popup").addClass("is-open");
      $(".popup-fadescreen").addClass("is-open");
      event.preventDefault();
      var message = $(".popup").find("p.font-semi-bold");
      var bid_value = parseFloat($("#id_bid").val()).toFixed(4);
      message.text('Do you want to change this bid to ' + bid_value +'?')
  });

  $(".cancel").click(function(event) {
    $(".popup-fadescreen").removeClass("is-open");
  });
});
