(function () {
  var ref = document.referrer;
  if (ref && ref.indexOf('/game-account-value/') !== -1) {
    document.getElementById('backLink').href = ref;
  }
})();
