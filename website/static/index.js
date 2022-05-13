// izvor: https://laracasts.com/discuss/channels/laravel/how-to-use-boostrap-modal-to-submit-a-form-outside-of-modal
// anonimna funkcija za submit forme iz modala. Submit button ne radi ako je izvan tijela forme.
$(function () {
  $("#submit-namirnica").on("click", function () {
    $("#add-namirnica-form").submit();
  });
});
