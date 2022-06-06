// izvor: https://laracasts.com/discuss/channels/laravel/how-to-use-boostrap-modal-to-submit-a-form-outside-of-modal
// anonimna funkcija za submit forme iz modala. Submit button ne radi ako je izvan tijela forme.

// $(function () {
//   $("#submit-namirnica").on("click", function () {
//     $("#add-namirnica-form").submit();
//   });
// });

function izbrisiNam(namId) {
  fetch("/namirnice/izbrisi-nam", {
    method: "DELETE",
    // konverzija js objekta u json kako bih mogao to poslati serveru
    body: JSON.stringify({ namId: namId }),
  }).then((_res) => {
    window.location.href = "/namirnice";
  });
}

function setMjerna(mjernaJed) {
  var jedinicaMj = document.getElementById("mjernaJed");
  jedinicaMj.setAttribute("value", `${mjernaJed}`);
}

function tableToJSON(table) {
  var obj = {};
  var row,
    rows = table.rows;
  for (var i = 0, iLen = rows.length; i < iLen; i++) {
    row = rows[i];
    obj[row.cells[0].textContent] = row.cells[1].textContent;
  }
  return JSON.stringify(obj);
}

// console.log(tableToJSON(document.getElementById('t0')));
