

$(document).ready(function () {
    if ($('#register_all_notification').length && $('#register_specific_notification').length) {
        if ($('#register_all_notification').data('check') == true) {
            $('#register_all_notification').prop('checked', true);
            $('#register_specific_notification').parent().removeClass('d-none');
        }
        if ($('#register_specific_notification').data('check') == true) $('#register_specific_notification').prop('checked', true);
        $('#register_all_notification').on('change', function () {
            if (this.checked) $('#register_specific_notification').parent().removeClass('d-none');
            else $('#register_specific_notification').parent().addClass('d-none');
        });
    }
});
