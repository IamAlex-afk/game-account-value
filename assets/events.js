// Event timeline status: "in N days" / "Live now" / "Finished", computed in
// the visitor's browser from each entry's data-start / data-end (or
// data-month) — nothing is fetched or sent. Labels come from the list's
// data-l-* attributes (localized per page), English as fallback. Past
// entries are dimmed and moved to the end so the next event is first.
(function () {
  var DAY = 864e5;
  function at(d, end) { var t = new Date(d + (end ? "T23:59:59" : "T00:00:00")); return isNaN(t) ? null : t; }
  document.addEventListener("DOMContentLoaded", function () {
    var now = new Date();
    document.querySelectorAll(".ev-list").forEach(function (list) {
      var L = {
        days: list.getAttribute("data-l-days") || "In {n} days",
        tomorrow: list.getAttribute("data-l-tomorrow") || "Tomorrow",
        live: list.getAttribute("data-l-live") || "Live now",
        month: list.getAttribute("data-l-month") || "This month",
        done: list.getAttribute("data-l-done") || "Finished"
      };
      var past = [];
      list.querySelectorAll(".ev").forEach(function (li) {
        var out = li.querySelector(".ev-count");
        var start = null, end = null;
        if (li.dataset.start) { start = at(li.dataset.start); end = at(li.dataset.end || li.dataset.start, true); }
        else if (/^\d{4}-\d{2}$/.test(li.dataset.month || "")) {
          var p = li.dataset.month.split("-");
          start = new Date(+p[0], +p[1] - 1, 1); end = new Date(+p[0], +p[1], 0, 23, 59, 59);
        }
        if (!start || !end) return;
        var label, cls;
        if (now > end) { label = L.done; cls = "ev-done"; past.push(li); }
        else if (now >= start) { label = li.dataset.month ? L.month : L.live; cls = "ev-live"; }
        else if (li.dataset.month) { return; }   // month known, day not: no fake countdown
        else {
          var n = Math.ceil((start - now) / DAY);
          label = n === 1 ? L.tomorrow : L.days.replace("{n}", n); cls = "ev-soon";
        }
        li.classList.add(cls);
        if (out) out.textContent = label;
      });
      past.forEach(function (li) { list.appendChild(li); });
    });
  });
})();
