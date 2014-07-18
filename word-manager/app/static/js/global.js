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

  addProhibitedWord: function(e) {
    e.preventDefault();
    var new_pword = $('#new-pword').val();
    var wid = wm.getWid();
    $.post('/api/add-prohibited', {wid: wid, word: new_pword}, function(data) {
      if (data.status == 'ok' && data.pwid) {
        $('#new-pword').val('');
        var newli = document.createElement('li');
        $(newli).data('pwid', data.pwid);
        var span = document.createElement('span');
        span.className = 'fa fa-ban reject-prohibited-word';
        $(span).click(wm.deleteProhibitedWord);
        newli.appendChild(span);
        newli.appendChild(document.createTextNode(' ' + new_pword));
        $('ul.prohibited-words').append(newli);
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
    var wid = wm.getWid();
    $.post('/api/reject', {wid: wid}, function() {
      location.reload();
    });
  }

});

$(document).ready(function(e) {
  wm.init();
  $('.reject-prohibited-word').click(wm.deleteProhibitedWord);
  $('#verifier .approve-btn').click(wm.approveWord);
  $('#verifier .reject-btn').click(wm.rejectWord);
  $('form#add-prohibited').submit(wm.addProhibitedWord);
});
