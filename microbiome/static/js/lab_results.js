$(function(){
  var results_panel = $('#lab-results-panel');
  var left_table = $('#left_table');

  $('.right-table').on('click', '.view-lab-report', function(){
    var url = $(this).data('url');
    results_panel.show();
    left_table.hide();
    $("#results-space").load(url);
  });

  $("#board-link").on('click', function(){
    results_panel.hide();
    left_table.show();
  });

  $(".update-lab-result").on('click', function(){
    $(this).text('Loading....');
    var url = $(this).data('url');
    $("#x_results").load(url, function(response, textStatus, xhr){
      if(textStatus == "success"){
        $('.update-lab-result').text('Updated!');
      }
    });
  });

});
