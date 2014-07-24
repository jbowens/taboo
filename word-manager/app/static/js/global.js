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
      }
    });
    li.remove();
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
  },

  searchFormSubmitted: function(e) {
    e.preventDefault();
    var input = $(this).find('input[name="q"]');
    var q = input.val()
    input.val('')
    $.post('/api/search', {q: q}, function(data) {
      $('.search-results').remove();
      if (data.status == 'ok') {
        if (data.results.length) {
          var ul = document.createElement('ul');
          ul.className = 'search-results';
          for (var i = 0; i < data.results.length; ++i) {
            var wid = data.results[i].wid;

            var li = document.createElement('li');
            $(li).data('wid', wid);
            li.className = 'status-' + data.results[i].status + ' wid-' + wid;

            var wordContainer = document.createElement('div');
            wordContainer.className = 'word';
            wordContainer.innerText = data.results[i].word;
            li.appendChild(wordContainer);

            var wordStatus = document.createElement('div');
            wordStatus.className = 'status';
            wordStatus.innerText = data.results[i].status;
            li.appendChild(wordStatus);

            ul.appendChild(li);

            $(li).click(function(e) {
              e.preventDefault();
              window.location = '/verify-words/' + $(this).data('wid');
            });
          }
          $('#search').append(ul);
        } else {
          var div = document.createElement('div');
          div.className = 'search-results no-results';
          var p = document.createElement('p');
          p.innerText = 'No search results found.';
          div.appendChild(p);
          $('#search').append(div);
        }
      }
    });
  },

  downloadInitiated: function(e) {
    if ($(this).data('disabled')) {
      e.preventDefault();
    } else {
      $(this).html('Generating&hellip;');
      $(this).data('disabled', true);
    }
  },

});

$(document).ready(function(e) {
  wm.init();
  $('.reject-prohibited-word').click(wm.deleteProhibitedWord);
  $('#verifier .approve-btn').click(wm.approveWord);
  $('#verifier .reject-btn').click(wm.rejectWord);
  $('form#add-prohibited').submit(wm.addProhibitedWord);
  $('form#search').submit(wm.searchFormSubmitted);
  $('a#download-export').click(wm.downloadInitiated);
});
