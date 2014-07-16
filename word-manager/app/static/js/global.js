var wm = wm || {};

$.extend(wm, {

  init: function() {

  },

  deleteProhibitedWord: function(e) {
    var li = $(this).closest('li');
    var pwid = li.data('pwid');
    $.post('/api/remove-prohibited', {pwid: pwid}, function(data) {
      if (data.status == 'ok') {
        li.remove();
      }
    });
  }

});

$(document).ready(function(e) {
  wm.init();
  $('.reject-prohibited-word').click(wm.deleteProhibitedWord);
});
