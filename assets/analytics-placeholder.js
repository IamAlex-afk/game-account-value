window.gavTrackEvent = function(name, payload) { /* TODO: self-hosted endpoint */ };

document.addEventListener('click', function(e) {
  var el = e.target.closest('[data-event]');
  if (el) window.gavTrackEvent(el.getAttribute('data-event'), { source: 'page' });
});
