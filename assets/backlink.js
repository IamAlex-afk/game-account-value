(function () {
  var ref = document.referrer;
  if (ref && ref.indexOf(location.origin) === 0) {
    document.getElementById('backLink').href = ref;
  }
})();
