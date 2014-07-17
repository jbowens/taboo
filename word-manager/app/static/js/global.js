var wm = wm || {};

$.extend(wm, {

  init: function() {

  },

  getWid: function() {
    var wid = $('#verifier').data('wid');
    return wid;
  },

  deleteProhibitedWord: function(e) {
    var li = $(this).closest('li');
    var pwid = li.data('pwid');
    $.post('/api/remove-prohibited', {pwid: pwid}, function(data) {
      if (data.status == 'ok') {
        li.remove();
      }
    });
  },

  approveWord: function(e) {
    var wid = wm.getWid();
    $.post('/api/approve', {wid: wid}, function() {
      location.reload();
    });
  },

  rejectWord: function(e) {
  }

});

$(document).ready(function(e) {
  wm.init();
  $('.reject-prohibited-word').click(wm.deleteProhibitedWord);
  $('#verifier .approve-btn').click(wm.approveWord);
  $('#verifier .reject-btn').click(wm.rejectWord);
});
